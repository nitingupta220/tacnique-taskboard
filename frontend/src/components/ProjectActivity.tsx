import { useQuery } from "@tanstack/react-query";
import { apiFetch, getStoredUser } from "@/lib/api-client";
import type { ApiActivity } from "@/types";
import { STATUS_LABELS } from "@/types";

function describeActivity(activity: ApiActivity) {
  switch (activity.action) {
    case "task_created": return "created a task";
    case "status_changed":
      return `changed status from ${STATUS_LABELS[activity.details.from]} to ${STATUS_LABELS[activity.details.to]}`;
    case "assignee_changed":
      return `changed assignee from ${activity.details.from?.name ?? "unassigned"} to ${activity.details.to?.name ?? "unassigned"}`;
    case "comment_added": return "added a comment";
  }
}

export function ProjectActivity({ projectId }: { projectId: string }) {
  const activities = useQuery({
    queryKey: ["project-activity", projectId, getStoredUser()?.id],
    queryFn: () => apiFetch<{ activities: ApiActivity[] }>(`/api/projects/${projectId}/activity`),
  });

  return (
    <section aria-label="recent activity" className="mt-10">
      <h2 className="text-sm font-medium mb-3">recent activity</h2>
      {activities.isPending && <p className="text-sm text-muted">loading activity…</p>}
      {activities.error && <p role="alert" className="text-sm text-red-400">{activities.error.message}</p>}
      {activities.data && !activities.error && (
        <>
          {activities.data.activities.length === 0 && <p className="text-sm text-muted">no activity yet</p>}
          <ol aria-label="project activity" className="bg-surface border border-border rounded-lg divide-y divide-border">
            {activities.data.activities.map(activity => (
              <li key={activity.id} className="px-4 py-3 text-sm">
                <p><span className="font-medium">{activity.actor.name}</span> {describeActivity(activity)}</p>
                <p className="mt-1 break-words">{activity.details.taskTitle}</p>
                {activity.action === "comment_added" && (
                  <p className="mt-2 whitespace-pre-wrap break-words text-muted">{activity.details.body}</p>
                )}
                <time dateTime={activity.createdAt} className="block text-xs text-muted mt-2">
                  {new Date(activity.createdAt).toLocaleString()}
                </time>
              </li>
            ))}
          </ol>
          <p className="text-xs text-muted mt-2">Latest 50 events, newest first.</p>
        </>
      )}
    </section>
  );
}
