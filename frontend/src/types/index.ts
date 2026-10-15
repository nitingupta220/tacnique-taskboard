export type Role = "admin" | "member" | "viewer";
export type ExportResult = {
  total: number;
  created: number;
  updated: number;
  failed: number;
  failures: { taskId: string; title: string; error: string }[];
};
export type TaskStatus = "todo" | "in_progress" | "review" | "done";

export type ApiUser = {
  id: string;
  email: string;
  name: string;
};

export type ApiComment = {
  id: string;
  author: ApiUser;
  body: string;
  createdAt: string;
};

type ActivityTask = { taskId: string; taskTitle: string };
type ActivityAssignee = { id: string; name: string } | null;
export type ApiActivity = {
  id: string;
  projectId: string;
  actor: ApiUser;
  createdAt: string;
} & (
  | { action: "task_created"; details: ActivityTask & { status: TaskStatus; assignee: ActivityAssignee } }
  | { action: "status_changed"; details: ActivityTask & { from: TaskStatus; to: TaskStatus } }
  | { action: "assignee_changed"; details: ActivityTask & { from: ActivityAssignee; to: ActivityAssignee } }
  | { action: "comment_added"; details: ActivityTask & { commentId: string; body: string } }
);

export type ApiTask = {
  id: string;
  projectId: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  assigneeId: string | null;
  createdById: string;
  position: number;
  createdAt: string;
  updatedAt: string;
  assignee?: ApiUser | null;
};

export type ApiProjectMember = {
  id: string;
  role: Role;
  user: ApiUser;
};

export type ApiProjectDetail = {
  id: string;
  name: string;
  description: string | null;
  ownerId: string;
  owner: ApiUser;
  memberships: ApiProjectMember[];
  tasks: ApiTask[];
  createdAt: string;
  updatedAt: string;
};

export const STATUS_LABELS: Record<TaskStatus, string> = {
  todo: "To do",
  in_progress: "In progress",
  review: "In review",
  done: "Done",
};

export const STATUS_ORDER: TaskStatus[] = ["todo", "in_progress", "review", "done"];
