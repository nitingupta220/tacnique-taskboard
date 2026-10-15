import { afterEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ExportButton } from "@/components/ExportButton";
import type { ExportResult, Role } from "@/types";

function renderButton(role?: Role) {
  const client = new QueryClient({ defaultOptions: { mutations: { retry: false } } });
  return render(<QueryClientProvider client={client}><ExportButton projectId="project-1" role={role} /></QueryClientProvider>);
}

afterEach(() => vi.unstubAllGlobals());

describe("<ExportButton />", () => {
  it.each(["admin", "member"] as const)("allows a project %s to export", role => {
    renderButton(role);
    expect(screen.getByRole("button", { name: "export to Airtable" })).toBeEnabled();
  });

  it.each(["viewer", undefined] as const)("hides export for role %s", role => {
    renderButton(role);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("disables duplicate submissions and displays partial export counts and failures", async () => {
    let complete!: (response: Response) => void;
    const fetch = vi.fn((_path: RequestInfo | URL, _options?: RequestInit) => new Promise<Response>(resolve => { complete = resolve; }));
    vi.stubGlobal("fetch", fetch);
    renderButton("member");
    fireEvent.click(screen.getByRole("button"));
    await waitFor(() => expect(screen.getByRole("button")).toBeDisabled());
    const result: ExportResult = { total: 3, created: 1, updated: 1, failed: 1,
      failures: [{ taskId: "task-3", title: "Rejected task", error: "Check field values." }] };
    complete(new Response(JSON.stringify(result), { status: 200 }));
    expect(await screen.findByRole("status")).toHaveTextContent("1 created · 1 updated · 1 failed");
    expect(screen.getByText("Rejected task: Check field values.")).toBeInTheDocument();
    expect(screen.getByRole("button")).toBeEnabled();
    expect(fetch).toHaveBeenCalledOnce();
    expect(fetch.mock.calls[0][0]).toBe("/api/projects/project-1/export");
    expect(fetch.mock.calls[0][1]).toMatchObject({ method: "POST" });
  });

  it("shows a server error and allows the user to try again", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ error: "Export unavailable." }), { status: 503 })));
    renderButton("admin");
    fireEvent.click(screen.getByRole("button"));
    expect(await screen.findByRole("alert")).toHaveTextContent("Export unavailable.");
    expect(screen.getByRole("button")).toBeEnabled();
  });
});
