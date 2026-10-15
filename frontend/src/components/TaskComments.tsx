import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch, getStoredUser } from "@/lib/api-client";
import type { ApiComment, Role } from "@/types";

export function TaskComments({ taskId, projectId, role }: { taskId: string; projectId: string; role?: Role }) {
  const [body, setBody] = useState("");
  const queryClient = useQueryClient();
  const queryKey = ["task-comments", getStoredUser()?.id, taskId];
  const comments = useQuery({
    queryKey,
    queryFn: () => apiFetch<{ comments: ApiComment[] }>(`/api/tasks/${taskId}/comments`),
  });
  const postComment = useMutation({
    mutationFn: () => apiFetch<{ comment: ApiComment }>(`/api/tasks/${taskId}/comments`, {
      method: "POST",
      body: JSON.stringify({ body: body.trim() }),
    }),
    onSuccess: async () => {
      setBody("");
      await Promise.all([
        queryClient.invalidateQueries({ queryKey }),
        queryClient.invalidateQueries({ queryKey: ["project-activity", projectId] }),
      ]);
    },
  });
  const canPost = role === "admin" || role === "member";

  return (
    <section aria-label="comments" className="mt-6 pt-5 border-t border-border">
      <h3 className="text-sm font-medium mb-3">comments</h3>
      {comments.isPending && <p className="text-sm text-muted">loading comments…</p>}
      {comments.error && <p role="alert" className="text-sm text-red-400">{comments.error.message}</p>}
      {comments.data && !comments.error && (
        <>
          {comments.data.comments.length === 0 && <p className="text-sm text-muted">no comments yet</p>}
          <ol aria-label="task comments" className="space-y-4">
            {comments.data.comments.map(comment => (
              <li key={comment.id} className="rounded-md border border-border bg-bg p-3">
                <div className="flex flex-wrap items-center justify-between gap-2 text-xs mb-2">
                  <span className="font-medium">{comment.author.name}</span>
                  <time dateTime={comment.createdAt} className="text-muted">
                    {new Date(comment.createdAt).toLocaleString()}
                  </time>
                </div>
                <p className="text-sm whitespace-pre-wrap break-words">{comment.body}</p>
              </li>
            ))}
          </ol>
          {canPost ? (
            <form className="mt-4" onSubmit={event => {
              event.preventDefault();
              if (body.trim() && !postComment.isPending) postComment.mutate();
            }}>
              <label className="block text-xs text-muted">
                new comment
                <textarea
                  value={body}
                  onChange={event => setBody(event.target.value)}
                  rows={3}
                  maxLength={5000}
                  disabled={postComment.isPending}
                  required
                  className="mt-1 block w-full rounded-md bg-bg border border-border px-3 py-2 text-sm text-white focus:border-accent focus:outline-none disabled:opacity-50"
                />
              </label>
              <p className="text-xs text-muted mt-2">Comments are permanent once posted.</p>
              {postComment.error && <p role="alert" className="text-sm text-red-400 mt-2">{postComment.error.message}</p>}
              <button
                type="submit"
                disabled={!body.trim() || postComment.isPending}
                className="mt-3 bg-accent hover:bg-indigo-500 text-white text-sm rounded-md px-4 py-2 disabled:opacity-50"
              >
                {postComment.isPending ? "posting…" : "post comment"}
              </button>
            </form>
          ) : <p className="text-xs text-muted mt-4">You have read-only access to comments.</p>}
        </>
      )}
    </section>
  );
}
