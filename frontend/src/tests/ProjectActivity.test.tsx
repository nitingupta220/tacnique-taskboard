import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { ProjectActivity } from "@/components/ProjectActivity";
import { TaskComments } from "@/components/TaskComments";
import { TaskDetail } from "@/components/TaskDetail";
import ProjectPage from "@/pages/ProjectPage";
import type { ApiActivity, ApiTask } from "@/types";

const actor = { id: "member-1", name: "A Member", email: "member@example.test" };
const base = { projectId: "project-1", actor, createdAt: "2026-10-15T10:00:00Z" };
const taskDetails = { taskId: "task-1", taskTitle: "Release checklist" };
const events: ApiActivity[] = [
  { ...base, id: "event-4", action: "comment_added", details: { ...taskDetails, commentId: "comment-1", body: "Ready for review" } },
  { ...base, id: "event-3", action: "assignee_changed", details: { ...taskDetails, from: null, to: actor } },
  { ...base, id: "event-2", action: "status_changed", details: { ...taskDetails, from: "todo", to: "in_progress" } },
  { ...base, id: "event-1", action: "task_created", details: { ...taskDetails, status: "todo", assignee: null } },
];
const task: ApiTask = { id: "task-1", projectId: "project-1", title: "Release checklist", description: null,
  status: "todo", assigneeId: null, createdById: actor.id, position: 0, createdAt: base.createdAt, updatedAt: base.createdAt };
const response = (data: unknown, status = 200) => new Response(JSON.stringify(data), { status });
function wrapper({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } }));
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
});

describe("<ProjectActivity />", () => {
  it("shows all event types in server order with actor, details, and semantic time", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ activities: events })));
    render(<ProjectActivity projectId="project-1" />, { wrapper });
    await screen.findByText("Ready for review");
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(4);
    expect(rows[0]).toHaveTextContent("A Member added a comment");
    expect(rows[1]).toHaveTextContent("changed assignee from unassigned to A Member");
    expect(rows[2]).toHaveTextContent("changed status from To do to In progress");
    expect(rows[3]).toHaveTextContent("created a task");
    expect(rows[0]).toHaveTextContent(taskDetails.taskTitle);
    expect(rows[0].querySelector("time")).toHaveAttribute("datetime", base.createdAt);
    expect(rows[0].querySelector("time")).not.toBeEmptyDOMElement();
  });

  it("renders unassignment and comment text safely", async () => {
    const body = '<img src=x onerror="alert(1)">';
    const unassigned: ApiActivity = { ...base, id: "unassign", action: "assignee_changed", details: { ...taskDetails, from: actor, to: null } };
    const comment: ApiActivity = { ...base, id: "comment", action: "comment_added", details: { ...taskDetails, commentId: "comment", body } };
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ activities: [unassigned, comment] })));
    const { container } = render(<ProjectActivity projectId="project-1" />, { wrapper });
    expect(await screen.findByText(body)).toBeInTheDocument();
    expect(screen.getByText(/changed assignee from A Member to unassigned/)).toBeInTheDocument();
    expect(container.querySelector("img")).toBeNull();
  });

  it("shows a loading state then an empty feed", async () => {
    let finish!: (value: Response) => void;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(resolve => { finish = resolve; })));
    render(<ProjectActivity projectId="project-1" />, { wrapper });
    expect(screen.getByText("loading activity…")).toBeInTheDocument();
    finish(response({ activities: [] }));
    expect(await screen.findByText("no activity yet")).toBeInTheDocument();
  });

  it("shows authorization errors without displaying an empty feed", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ error: "forbidden" }, 403)));
    render(<ProjectActivity projectId="project-1" />, { wrapper });
    expect(await screen.findByRole("alert")).toHaveTextContent("forbidden");
    expect(screen.queryByText("no activity yet")).not.toBeInTheDocument();
  });

  it("keeps project caches separate", async () => {
    vi.stubGlobal("fetch", vi.fn((path: string) => Promise.resolve(response({ activities: path.includes("project-1/") ? events : [] }))));
    const { rerender } = render(<ProjectActivity projectId="project-1" />, { wrapper });
    await screen.findByText("Ready for review");
    rerender(<ProjectActivity projectId="project-2" />);
    expect(await screen.findByText("no activity yet")).toBeInTheDocument();
    expect(screen.queryByText("Ready for review")).not.toBeInTheDocument();
  });

  it("does not reuse a previous user's cached feed", async () => {
    localStorage.setItem("taskboard_user", JSON.stringify(actor));
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(response({ activities: events }))
      .mockResolvedValueOnce(response({ error: "forbidden" }, 403)));
    const { rerender } = render(<ProjectActivity projectId="project-1" />, { wrapper });
    await screen.findByText("Ready for review");
    localStorage.setItem("taskboard_user", JSON.stringify({ ...actor, id: "outsider" }));
    rerender(<ProjectActivity projectId="project-1" />);
    expect(screen.queryByText("Ready for review")).not.toBeInTheDocument();
    expect(await screen.findByRole("alert")).toHaveTextContent("forbidden");
  });

  it("refreshes the mounted feed when a comment is posted", async () => {
    let posted = false;
    vi.stubGlobal("fetch", vi.fn((path: string, options?: RequestInit) => {
      if (options?.method === "POST") {
        posted = true;
        return Promise.resolve(response({ comment: { id: "comment-1", body: "Ready for review", author: actor, createdAt: base.createdAt } }, 201));
      }
      if (path.endsWith("/activity")) return Promise.resolve(response({ activities: posted ? [events[0]] : [] }));
      return Promise.resolve(response({ comments: [] }));
    }));
    render(<><ProjectActivity projectId="project-1" /><TaskComments taskId="task-1" projectId="project-1" role="member" /></>, { wrapper });
    await screen.findByText("no activity yet");
    await screen.findByRole("textbox", { name: "new comment" });
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "Ready for review" } });
    fireEvent.click(screen.getByRole("button", { name: "post comment" }));
    const feed = screen.getByRole("region", { name: "recent activity" });
    expect(await within(feed).findByText("Ready for review")).toBeInTheDocument();
  });

  it("refreshes activity after a task update and preserves the server's nested assignee", async () => {
    let updated = false;
    const fetch = vi.fn((path: string, options?: RequestInit) => {
      if (options?.method === "PATCH") {
        expect(JSON.parse(options.body as string).assigneeId).toBe(actor.id);
        updated = true;
        return Promise.resolve(response({ task }));
      }
      if (path.endsWith("/activity")) return Promise.resolve(response({ activities: updated ? [events[2]] : [] }));
      return Promise.resolve(response({ comments: [] }));
    });
    vi.stubGlobal("fetch", fetch);
    render(<><ProjectActivity projectId="project-1" /><TaskDetail task={{ ...task, assignee: actor }} projectId="project-1"
      members={[{ id: "membership", user: actor, role: "member" }]} onClose={vi.fn()} /></>, { wrapper });
    await screen.findByText("no activity yet");
    expect(screen.getByRole("combobox", { name: "assignee" })).toHaveValue(actor.id);
    fireEvent.change(screen.getByRole("combobox", { name: "status" }), { target: { value: "in_progress" } });
    fireEvent.click(screen.getByRole("button", { name: "save" }));
    expect(await screen.findByText(/changed status from To do to In progress/)).toBeInTheDocument();
  });

  it("mounts on the project page and refreshes after creating a task", async () => {
    localStorage.setItem("taskboard_token", "test-only");
    localStorage.setItem("taskboard_user", JSON.stringify(actor));
    let created = false;
    vi.stubGlobal("fetch", vi.fn((path: string, options?: RequestInit) => {
      if (options?.method === "POST") { created = true; return Promise.resolve(response({ task }, 201)); }
      if (path.endsWith("/activity")) return Promise.resolve(response({ activities: created ? [events[3]] : [] }));
      return Promise.resolve(response({ project: { id: "project-1", name: "Project", description: null,
        owner: actor, memberships: [{ id: "membership", user: actor, role: "member" }], tasks: created ? [task] : [] } }));
    }));
    render(<MemoryRouter initialEntries={["/projects/project-1"]}><Routes><Route path="/projects/:id" element={<ProjectPage />} /></Routes></MemoryRouter>, { wrapper });
    await screen.findByText("no activity yet");
    fireEvent.change(screen.getByPlaceholderText("task title"), { target: { value: task.title } });
    fireEvent.click(screen.getByRole("button", { name: "add" }));
    const feed = screen.getByRole("region", { name: "recent activity" });
    expect(await within(feed).findByText(/created a task/)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByPlaceholderText("task title")).toHaveValue(""));
  });
});
