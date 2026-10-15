import { afterEach, describe, expect, it, vi } from "vitest";
import { useState } from "react";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { TaskComments } from "@/components/TaskComments";
import { TaskDetail } from "@/components/TaskDetail";
import type { ApiComment, ApiTask, Role } from "@/types";

const author = { id: "member-1", name: "A Member", email: "member@example.test" };
const earlier: ApiComment = { id: "comment-1", body: "Earlier discussion", author, createdAt: "2026-10-15T09:00:00Z" };
const later: ApiComment = { id: "comment-2", body: "Later discussion", author, createdAt: "2026-10-15T09:05:00Z" };
const response = (data: unknown, status = 200) => new Response(JSON.stringify(data), { status });

function wrapper({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } }));
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

function renderComments(role?: Role) {
  return render(<TaskComments taskId="task-1" role={role} />, { wrapper });
}

afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
});

describe("<TaskComments />", () => {
  it("displays server ordering, author, body, and semantic timestamps without edit/delete controls", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ comments: [earlier, later] })));
    renderComments("member");
    await screen.findByText(earlier.body);
    const rows = screen.getAllByRole("listitem");
    expect(rows[0]).toHaveTextContent(earlier.body);
    expect(rows[1]).toHaveTextContent(later.body);
    expect(within(rows[0]).getByText(author.name)).toBeInTheDocument();
    expect(rows[0].querySelector("time")).toHaveAttribute("datetime", earlier.createdAt);
    expect(rows[0].querySelector("time")).not.toBeEmptyDOMElement();
    expect(screen.queryByRole("button", { name: /edit|delete/i })).not.toBeInTheDocument();
  });

  it.each(["admin", "member"] as const)("allows a project %s to compose", async role => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ comments: [] })));
    renderComments(role);
    await screen.findByText("no comments yet");
    expect(screen.getByRole("textbox", { name: "new comment" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "post comment" })).toBeDisabled();
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "  \n " } });
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it.each(["viewer", undefined] as const)("keeps role %s read-only", async role => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ comments: [earlier] })));
    renderComments(role);
    await screen.findByText(earlier.body);
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "post comment" })).not.toBeInTheDocument();
  });

  it("posts only the body, prevents double submissions, and refreshes the chronological thread", async () => {
    let finish!: (value: Response) => void;
    let posted = false;
    const fetch = vi.fn((path: RequestInfo | URL, options?: RequestInit) => {
      expect(path).toBe("/api/tasks/task-1/comments");
      if (options?.method === "POST") return new Promise<Response>(resolve => { finish = resolve; });
      return Promise.resolve(response({ comments: posted ? [earlier, later] : [earlier] }));
    });
    vi.stubGlobal("fetch", fetch);
    renderComments("member");
    await screen.findByText(earlier.body);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "  Later discussion  " } });
    fireEvent.click(screen.getByRole("button", { name: "post comment" }));
    await waitFor(() => expect(screen.getByRole("button")).toBeDisabled());
    const post = fetch.mock.calls.find(([, options]) => options?.method === "POST")!;
    expect(JSON.parse(post[1]!.body as string)).toEqual({ body: "Later discussion" });
    posted = true;
    finish(response({ comment: later }, 201));
    await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(2));
    expect(screen.getByRole("textbox")).toHaveValue("");
    expect(screen.getAllByRole("listitem")[1]).toHaveTextContent(later.body);
    expect(fetch.mock.calls.filter(([, options]) => options?.method === "POST")).toHaveLength(1);
  });

  it("preserves a draft and displays the server's permission error", async () => {
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(response({ comments: [] }))
      .mockResolvedValueOnce(response({ error: "viewers cannot post comments" }, 403)));
    renderComments("member");
    await screen.findByText("no comments yet");
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "Keep this draft" } });
    fireEvent.click(screen.getByRole("button", { name: "post comment" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("viewers cannot post comments");
    expect(screen.getByRole("textbox")).toHaveValue("Keep this draft");
    expect(screen.getByRole("button")).toBeEnabled();
  });

  it("shows a load error instead of a misleading empty thread", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ error: "forbidden" }, 403)));
    renderComments("member");
    expect(await screen.findByRole("alert")).toHaveTextContent("forbidden");
    expect(screen.queryByText("no comments yet")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "post comment" })).not.toBeInTheDocument();
  });

  it("renders comment text literally without interpreting HTML", async () => {
    const body = '<img src=x onerror="alert(1)">';
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ comments: [{ ...earlier, body }] })));
    const { container } = renderComments("viewer");
    expect(await screen.findByText(body)).toBeInTheDocument();
    expect(container.querySelector("img")).toBeNull();
  });

  it("keeps comments from different tasks in separate query entries", async () => {
    vi.stubGlobal("fetch", vi.fn((path: string) => Promise.resolve(response({
      comments: path.includes("task-1/") ? [earlier] : [later],
    }))));
    const { rerender } = renderComments("viewer");
    await screen.findByText(earlier.body);
    rerender(<TaskComments taskId="task-2" role="viewer" />);
    await screen.findByText(later.body);
    expect(screen.queryByText(earlier.body)).not.toBeInTheDocument();
  });

  it("does not reuse another signed-in user's cached comment thread", async () => {
    localStorage.setItem("taskboard_user", JSON.stringify(author));
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(response({ comments: [earlier] }))
      .mockResolvedValueOnce(response({ error: "forbidden" }, 403)));
    const { rerender } = renderComments("member");
    await screen.findByText(earlier.body);
    localStorage.setItem("taskboard_user", JSON.stringify({ ...author, id: "outsider" }));
    rerender(<TaskComments taskId="task-1" />);
    expect(screen.queryByText(earlier.body)).not.toBeInTheDocument();
    expect(await screen.findByRole("alert")).toHaveTextContent("forbidden");
    expect(screen.queryByText(earlier.body)).not.toBeInTheDocument();
  });

  it("mounts in the existing task dialog and derives the comment role from project membership", async () => {
    localStorage.setItem("taskboard_user", JSON.stringify(author));
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response({ comments: [earlier] })));
    const task: ApiTask = { id: "task-1", projectId: "project-1", title: "Task discussion", description: null,
      status: "todo", assigneeId: null, createdById: author.id, position: 0, createdAt: earlier.createdAt, updatedAt: earlier.createdAt };
    render(<TaskDetail task={task} projectId="project-1" members={[{ id: "membership-1", user: author, role: "viewer" }]} onClose={vi.fn()} />, { wrapper });
    const comments = screen.getByRole("region", { name: "comments" });
    expect(await within(comments).findByText(earlier.body)).toBeInTheDocument();
    expect(within(comments).queryByRole("textbox")).not.toBeInTheDocument();
  });
});
