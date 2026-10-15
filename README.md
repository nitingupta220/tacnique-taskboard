# TaskBoard — Project Management App

A fullstack project management app for managing projects, tasks, and team members.

**Tech Stack:** React 18 + Vite + TypeScript (frontend) · Django 5 + Django REST Framework + SimpleJWT (backend) · PostgreSQL 16

## Quick Setup (Docker — Recommended)

```bash
# Clone and enter the repo
git clone <repo-url> && cd q-taskboard

# Start all services
docker-compose up --build

# In a separate terminal, run migrations and seed
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed

# Run the test suites
docker-compose exec backend python -m pytest          # Django tests
docker-compose exec backend node --test airtable      # Airtable SDK tests
docker-compose exec frontend npm test                 # React tests

# The app is now running at http://localhost:3000
# Backend API at http://localhost:8000
```

## Manual Setup (without Docker)

Requires: Python 3.12+, Node.js 20+, PostgreSQL 15+

```bash
chmod +x bin/setup
./bin/setup

# Or manually:

# Backend
cd backend
pip install -r requirements.txt
npm --prefix airtable ci --ignore-scripts
# Create ../.env with the environment settings below, or copy your local .env.example.
python manage.py migrate
python manage.py seed
python -m pytest
node --test airtable

# Frontend
cd ../frontend
npm install
npm test
npm run dev
```

## AI Tool Conversation Tracking

**This repository is configured to automatically capture your AI coding tool conversation history with each git commit.** This includes conversations from Claude Code, Cursor, Aider, Continue.dev, Cody, Cline, and Windsurf.

This is part of the Ajackus evaluation process. We evaluate how you collaborate with AI tools — your prompting strategy, how you break down problems, and how you review AI suggestions. The captured conversations help us understand your workflow.

**How it works:**
- A pre-commit git hook runs automatically before each commit
- It copies conversation files from AI tool directories (e.g., `.claude/`, `.cursor/`) into `.ai-conversations/`
- These files are staged and included in your commit
- You don't need to do anything — it happens automatically

**What's captured:** Only AI tool conversation logs stored in the project directory. No system files, browsing history, or anything outside this repository.

**If you prefer a tool that doesn't store local conversations** (like browser-based ChatGPT), the screen recording will capture your interactions instead. No additional action needed from you.

## Seed Data

All user passwords are: `password123`

| Email | Role |
|-------|------|
| meera@taskboard.dev | admin on Q3 Launch & Internal Tools, member on Onboarding |
| arjun@taskboard.dev | admin on Onboarding, member on Q3 Launch |
| kavya@example.com | member on Q3 Launch |
| dev@example.com | viewer on Q3 Launch |
| lina@example.com | member on Onboarding |

## Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"meera@taskboard.dev","password":"password123"}'

# Use the returned token
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/projects
```

## API Endpoints

### Auth
- `POST /api/auth/register` — Create account
- `POST /api/auth/login` — Sign in, get JWT
- `GET /api/users/me` — Current user (authenticated)

### Projects
- `GET /api/projects` — List projects you're a member of (authenticated)
- `POST /api/projects` — Create a project (authenticated; creator becomes admin)
- `GET /api/projects/:id` — Project detail with tasks and members (authenticated)
- `PATCH /api/projects/:id` — Update project (admin only)
- `DELETE /api/projects/:id` — Delete project (admin only)

### Tasks
- `GET /api/projects/:id/tasks` — List tasks in a project; supports `?q=` search (authenticated)
- `POST /api/projects/:id/tasks` — Create a task (admin or member)
- `PATCH /api/tasks/:id` — Update a task (project admin or member)
- `DELETE /api/tasks/:id` — Delete a task (admin or member)

### Task comments
- `GET /api/tasks/:id/comments` — Read a task's comments (project admin, member, or viewer)
- `POST /api/tasks/:id/comments` — Append a comment (project admin or member)

Open a task to see its comments below the existing task controls. The thread shows each author's name, comment body, and local timestamp, oldest first. Admins and members can post; viewers see a read-only thread. Comment text is rendered as plain text.

Post JSON such as `{"body":"Ready for review."}`. Bodies must contain 1–5,000 characters after trimming. The server assigns the UUID, authenticated author, and timestamp; those fields cannot be supplied to edit an existing comment. Responses use `{"comments":[...]}` for reads and `{"comment":{...}}` with HTTP 201 for posts. Each comment contains `id`, `author` (`id`, `name`, `email`), `body`, and `createdAt`.

Comments are append-only through the API: there are no comment edit/delete routes. Threads are scoped to the task's project membership, with stable ordering by `created_at` then UUID. Tasks and projects with comments return HTTP 409 on deletion to preserve history; deleting a task without comments continues to work normally. Browser comment caches are scoped to both the signed-in user and task.

Apply the new table migration with `cd backend && python manage.py migrate`. No seed command or seed-data changes are required. Permission, ordering, immutability, and isolation tests are in `backend/projects/test_comments.py`; UI tests are in `frontend/src/tests/TaskComments.test.tsx`.

### Export
- `POST /api/projects/:id/export` — Export tasks to Airtable (admin or member)

### Project activity
- `GET /api/projects/:id/activity` — Latest 50 project events, newest first (project admin, member, or viewer)

The project detail page shows task creation, status changes, assignee changes, and new comments with the actor, change details, and local timestamp. Events are generated by the backend in the same database transaction as the operation. Failed writes roll back together; unchanged values do not produce extra events. The feed refreshes after task creation, updates, and comment posting. Existing tasks and comments are not backfilled. Apply migrations without running the seed command. See [design_notes.md](design_notes.md) for the rollback and retention decisions.

## Airtable Export

Enter credentials in the **root `.env`** (next to this README), then restart the backend. Both `.env` and the local `.env.example` are ignored by Git. Django loads this file without overriding existing environment variables. Docker Compose passes the Airtable settings only to the backend. Never put credentials in `VITE_*` variables or frontend files.

```dotenv
POSTGRES_DB=taskboard
POSTGRES_USER=taskboard
POSTGRES_PASSWORD=taskboard
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
AIRTABLE_API_KEY=<personal-access-token>
AIRTABLE_BASE_ID=<base-id>
AIRTABLE_TABLE_NAME=Tasks
```

The token needs `data.records:read` and `data.records:write` access to the configured base. Configure these editable fields in its target table:

| Field | Airtable type |
|-------|--------------|
| Task ID | Single line text (stable Taskboard UUID, used for upserts) |
| Project ID | Single line text or Long text |
| Title | Single line text |
| Task Description | Long text |
| Status | Single line text |
| Assignee | Single line text |
| Position | Number (integer) |

An existing AI-generated `Description` field can remain; the exporter writes to `Task Description`. Schema changes are a setup step, not part of an export. Do not use a computed or AI field for exported values.

Project admins and members see **export to Airtable** on the project detail page; viewers cannot export. `POST /api/projects/:id/export` checks membership and loads tasks directly from PostgreSQL. It ignores client-supplied task data. A successful request returns, for example:

```json
{"total":3,"created":1,"updated":1,"failed":1,"failures":[{"taskId":"<uuid>","title":"Example task","error":"Airtable rejected the field values. Check the table schema and task."}]}
```

The Django service invokes a small server-side Node process using the **official `airtable` npm package**, installed in `backend/airtable`. Node 20+ must be on the backend PATH; `AIRTABLE_NODE_BINARY` can select another executable. Docker includes Node and the package. No additional service or local export state is required.

Exports support up to 1,000 tasks, read Airtable records in pages of 100, and write batches of 10 with Airtable `performUpsert` keyed by `Task ID`. Repeated exports update the same records, including after an ambiguous network failure. Existing duplicate Task IDs are reported as failures for those tasks. Unrelated rows and extra Airtable columns are preserved; exports do not delete remote rows or change local tasks.

Calls are spaced by at least 250 ms. Transient connection errors, HTTP 500/502/503/504, and rate limits get at most two retries. Backoff is 500 ms then 1 second for server/network errors, or 30 then 60 seconds for rate limits; the SDK's automatic rate-limit retries are disabled. A 120-second budget bounds the export. Permanent failures have no backoff retry. Rejected multi-record batches (413/422) are split into smaller diagnostic batches to isolate invalid records, then other tasks continue; a rejected singleton is not retried. Global credential/schema errors stop further API calls and report remaining tasks as failed. Failed or uncertain tasks can safely be exported again.

Run `python -m pytest` from `backend`, `node --test` from `backend/airtable`, and `npm test` from `frontend`. Automated tests use fake credentials and a local HTTP server, never the configured real base. `backend/projects/airtable_mock.py` is a legacy test double and is not used by the integration.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, TypeScript 5 (strict) |
| Routing | React Router 6 |
| Data fetching | TanStack Query 5 |
| Styling | Tailwind CSS 3 |
| Frontend tests | Vitest 2 + Testing Library |
| Backend | Django 5, Django REST Framework 3 |
| Auth | djangorestframework-simplejwt (JWT, 30-day tokens) |
| ORM | Django ORM |
| Database | PostgreSQL 16 |
| Backend tests | pytest-django |
| Container | Docker + docker-compose |
