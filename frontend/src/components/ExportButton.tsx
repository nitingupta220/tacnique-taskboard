import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api-client";
import type { ExportResult, Role } from "@/types";

export function ExportButton({ projectId, role }: { projectId: string; role?: Role }) {
  const exportTasks = useMutation({
    mutationFn: () => apiFetch<ExportResult>(`/api/projects/${projectId}/export`, { method: "POST" }),
  });
  if (role !== "admin" && role !== "member") return null;

  return (
    <div className="max-w-sm text-right">
      <button
        type="button"
        onClick={() => exportTasks.mutate()}
        disabled={exportTasks.isPending}
        className="bg-accent hover:bg-indigo-500 text-white text-sm rounded-md px-4 py-2 disabled:opacity-50"
      >
        {exportTasks.isPending ? "exporting…" : "export to Airtable"}
      </button>
      {exportTasks.error && <p role="alert" className="text-sm text-red-400 mt-2">{exportTasks.error.message}</p>}
      {exportTasks.data && !exportTasks.isPending && (
        <div className="mt-2 text-sm">
          <p role="status">{exportTasks.data.created} created · {exportTasks.data.updated} updated · {exportTasks.data.failed} failed</p>
          {exportTasks.data.failures.length > 0 && (
            <ul className="text-red-400 mt-2 text-left space-y-1">
              {exportTasks.data.failures.slice(0, 5).map(failure => (
                <li key={failure.taskId}>{failure.title}: {failure.error}</li>
              ))}
              {exportTasks.data.failures.length > 5 && <li>and {exportTasks.data.failures.length - 5} more failed tasks</li>}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
