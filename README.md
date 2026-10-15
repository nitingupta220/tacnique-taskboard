# TaskBoard — Project Management App

React 18, Vite and TypeScript frontend; Django REST Framework/JWT backend; PostgreSQL database. Both task comments and project activity are implemented, together with real Airtable export.

## Submission links

- Screen recording: **TODO — add your actual Loom or equivalent URL here.** The recording must narrate your thinking and keep the terminal visible. A placeholder does not satisfy submission.
- Airtable screenshot or read-only share link: **TODO — attach the actual screenshot or link showing exported tasks.** Saved real API responses prove two exports; no Airtable screenshot/share link was found.
- [Full compliance checklist and blockers](COMPLIANCE_AUDIT.md)
- [Chronological redacted terminal evidence](TERMINAL_LOG.md)
- [Original prioritized review](REVIEW.md), [rollback design](design_notes.md), [security findings](security_notes.md)

The original brief recovered from `84cb1a6:ASSIGNMENT.md` asks for `pyairtable`. The later explicit user instruction selected the official **Airtable npm package** instead. Django invokes that SDK server side. The current npm-package requirement is satisfied by `airtable@0.12.2`; it has not been replaced with a Python SDK. The original rubric wording remains a documented difference.

## Environment configuration

Create the root `.env` next to this README with mode `0600`. `.env` and `.env.example` are intentionally ignored, so a fresh clone may not have an example file. Enter actual secrets only in the ignored server file. Never put them in frontend files, `VITE_*` variables, chat, terminal output, or commits.

```dotenv
POSTGRES_DB=taskboard
POSTGRES_USER=taskboard
POSTGRES_PASSWORD=<unique-random-database-password>
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=<unique-long-random-server-secret>
DJANGO_ENV=development
DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
# Optional for a separately hosted browser client; leave empty with the Vite proxy:
DJANGO_CORS_ALLOWED_ORIGINS=
AIRTABLE_API_KEY=<personal-access-token>
AIRTABLE_BASE_ID=<base-id>
AIRTABLE_TABLE_NAME=Tasks
# Optional if node is not on the backend PATH:
# AIRTABLE_NODE_BINARY=/absolute/path/to/node
```

| Variable | Purpose |
| --- | --- |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` | Manual Django PostgreSQL connection. Pytest needs permission to create a separate test database. |
| `DJANGO_SECRET_KEY` | Required private Django/JWT secret, at least 50 characters; missing, weak and development keys prevent startup. Generate it using the helper below. |
| `DJANGO_ENV` | `development` for local HTTP or `production` to enforce production startup/transport checks. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated backend hostnames. Production requires explicit hosts without wildcards. |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Optional comma-separated browser origins; defaults empty. Same-origin Vite proxy needs no CORS override. |
| `DEBUG` | Defaults `false`; production refuses `true`. |
| `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_NAME` | Backend-only Airtable credentials/table, required for real export. |
| `AIRTABLE_NODE_BINARY` | Optional backend Node executable; defaults to `node`. |
| `API_TARGET` | Vite proxy URL; defaults to `http://localhost:8000`. Contains no Airtable secret. |

Generate a signing key without displaying its value:

```bash
python3 bin/generate-signing-key
```

The helper creates/replaces an absent or placeholder key in the ignored root `.env`, preserves other credentials and uses mode `0600`. It leaves an existing key unchanged unless you explicitly run `python3 bin/generate-signing-key --rotate`. Rotation invalidates existing JWTs; restart the backend and sign in again. There is no public fallback or old-key grace period. Do not reuse keys between environments.

Django loads the root `.env` without overriding deployed environment values. Compose requires database settings and the signing key from that environment/file; it passes Airtable settings only to the backend. Before a production deployment use a trusted host, fresh secrets from your secret manager, `DJANGO_ENV=production`, `DEBUG=false`, explicit hosts and a random database password of at least 16 characters. Production enables HTTPS redirects, secure cookies and one-year HSTS including subdomains/preload; deploy only with correctly configured TLS and ownership of the affected domain/subdomains. The supplied Compose stack is a loopback-bound development stack, not a production deployment. `manage.py check --deploy --fail-level WARNING` validates Django settings, not infrastructure or secret provenance.

**Incident follow-up:** the potentially exposed Airtable token has not yet been revoked; the user will rotate it manually on a trusted device and reduce it to record read/write scopes. Real exports are currently paused by an empty backend runtime key override. After replacing the root `.env` token, restart the backend without that override before testing. Repository cleanup and signing-key rotation do not establish workstation eradication or revoke an Airtable token.

## Docker setup

Requires Docker Compose v2. Ports 5432, 8000 and 3000 must be free for a fresh stack.

```bash
git clone <repo-url>
cd q-taskboard
# Configure the ignored root .env first.
docker compose up --build -d
docker compose exec backend python manage.py migrate

# ONLY for a brand-new, isolated database:
# docker compose exec backend python manage.py seed

# Verification
docker compose exec backend python -m pytest
docker compose exec --workdir /app/airtable backend node --test
docker compose exec frontend npm test
docker compose exec frontend npm run build
docker compose exec backend python manage.py migrate --check
docker compose exec backend python manage.py makemigrations --check --dry-run
```

Docker frontend: `http://localhost:3000`; API: `http://localhost:8000`. **Do not rerun seed on the existing review/demo database.** `bin/setup` also runs seed automatically; use the explicit steps here to preserve existing data. No seed command was run during the final audit. Docker instructions were reviewed against configuration; a new Docker image build was not performed during this audit.

## Manual setup

Requires Python 3.12+, a trusted Node.js 22.9+ installation with npm 11.6.4+, and PostgreSQL 15+ running with the configured database/user.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
npm --prefix backend/airtable ci --ignore-scripts
npm --prefix frontend ci --ignore-scripts
python3 bin/generate-signing-key
# Configure the root .env before starting Django.
cd backend
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

In a second terminal, from the repository root:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1
```

## Tests, production build, and migrations

From the repository root with the virtualenv active and PostgreSQL configured:

```bash
(cd backend && python -m pytest -v --tb=short)
(cd backend/airtable && node --test)
(cd frontend && npm test)
(cd frontend && npm run build)
(cd backend && python manage.py migrate --check)
(cd backend && python manage.py makemigrations --check --dry-run)
(cd backend && python manage.py check)
```

Pytest uses `taskboard.testing`, generates a temporary signing key, disables dotenv loading and clears real Airtable settings. For a manual test run, export the five `POSTGRES_*` connection settings in the backend test terminal (they are not loaded from `.env` by pytest); the database role must be able to create a test database. Compose already supplies these settings. Pytest creates that isolated PostgreSQL test database and applies migrations there. Airtable tests use fake settings and a local HTTP server; they do not export to the real base. The frontend build emits `frontend/dist`; it does not establish that Django or Compose are production-ready.

This workstation's global npm CLI was found truncated during incident investigation. Verification used the integrity-verified Node toolchain under `/tmp/taskboard-security/toolchain` and the verified npm 11.6.4 CLI under `/tmp/taskboard-hardening/npm11`, with sandboxed build/test processes and real credentials excluded. These temporary tools are local verification aids, not a prerequisite for a fresh clone. Use a trusted installed runtime or Docker on a clean host. The frontend now uses ESM configuration. A dependency-refresh attempt with npm 10.9.3 hit an internal resolver error; use the verified npm 11.6.4 toolchain used for the successful refresh. Build/test commands receive no real Airtable credentials. Tailwind 4 requires Safari 16.4+, Chrome 111+ or Firefox 128+.

## Current inspection runtime

The already-running inspection instance uses frontend `http://127.0.0.1:3000`, backend `http://127.0.0.1:8001`, PostgreSQL host port `55432`, and database `taskboard_inspection`. For that backend, the frontend proxy setting is `API_TARGET=http://127.0.0.1:8001`. These differ from fresh Docker defaults; avoid starting another stack on occupied ports. Both servers are running after the signing-key/dependency changes. Sign in again because previous JWTs were invalidated. The running backend intentionally returns HTTP 503 for exports until the potentially exposed Airtable token is replaced and its empty runtime override is removed.

Demo records are in separate non-seed projects. Activity demo: `/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d`. All original seed rows and pre-existing audit comments remain unchanged. Existing activity was not backfilled.

## Project structure

- `backend/taskboard/settings.py` and `urls.py`: environment/database/JWT settings and API routing.
- `backend/users/`: user model, password-based login/registration, JWT issuance and current-user API.
- `backend/projects/models.py`: projects, role memberships, tasks, append-only comment API storage, and activity events; schema changes are under `migrations/`.
- `backend/projects/views.py`, `serializers.py`, `urls.py`: project-scoped authorization, task search/writes, comments, activity, and export endpoint.
- `backend/projects/airtable_export.py` and `backend/airtable/exporter.mjs`: server-only Django-to-Node bridge and official SDK batching/upserts/retries.
- `frontend/src/pages/ProjectPage.tsx`: Kanban board, export trigger, and recent activity. `components/TaskDetail.tsx`, `TaskComments.tsx`, `ProjectActivity.tsx`, and `ExportButton.tsx` contain the existing UI flows.
- `frontend/src/lib/api-client.ts`: authenticated API requests and browser session storage. Tests live in `backend/projects/test_*.py`, `backend/projects/tests.py`, `backend/users/tests.py`, `backend/airtable/exporter.test.mjs`, and `frontend/src/tests/`.

## AI tool conversation tracking

The supplied `.git-hooks/pre-commit` copies supported project-local AI conversation files into `.ai-conversations/` when that hook directory is configured and executable. The audit found no `core.hooksPath` and no captured conversation directory, so automatic capture cannot be claimed for the existing commits. `bin/setup` configures hooks but also seeds the database. To configure hooks separately on a fresh checkout, use `git config core.hooksPath .git-hooks` and ensure the hook is executable. Review any captured content for secrets before committing. The actual recording link is still required above.

## Seed Data

These are public local demo fixtures; do not provision production accounts from this database. All seeded user passwords are: `password123`

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
POSTGRES_PASSWORD=<unique-random-database-password>
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

The Django service invokes a small server-side Node process using the **official `airtable` npm package**, installed in `backend/airtable`. Node 22.9+ must be on the backend PATH; `AIRTABLE_NODE_BINARY` can select another executable. Docker includes Node and the package. No additional service or local export state is required.

Exports support up to 1,000 tasks, read Airtable records in pages of 100, and write batches of 10 with Airtable `performUpsert` keyed by `Task ID`. Repeated exports update the same records, including after an ambiguous network failure. Existing duplicate Task IDs are reported as failures for those tasks. Unrelated rows and extra Airtable columns are preserved; exports do not delete remote rows or change local tasks.

Calls are spaced by at least 250 ms. Transient connection errors, HTTP 500/502/503/504, and rate limits get at most two retries. Backoff is 500 ms then 1 second for server/network errors, or 30 then 60 seconds for rate limits; the SDK's automatic rate-limit retries are disabled. A 120-second budget bounds the export. Permanent failures have no backoff retry. Rejected multi-record batches (413/422) are split into smaller diagnostic batches to isolate invalid records, then other tasks continue; a rejected singleton is not retried. Global credential/schema errors stop further API calls and report remaining tasks as failed. Failed or uncertain tasks can safely be exported again.

Run `python -m pytest` from `backend`, `node --test` from `backend/airtable`, and `npm test` from `frontend`. Automated tests use fake credentials and a local HTTP server, never the configured real base. There is no `backend/projects/airtable_mock.py` in this checkout; the integration uses the server-side SDK bridge and its tests.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 6, TypeScript 5 (strict) |
| Routing | React Router 7 |
| Data fetching | TanStack Query 5 |
| Styling | Tailwind CSS 4 |
| Frontend tests | Vitest 4 + Testing Library |
| Backend | Django 5, Django REST Framework 3 |
| Auth | djangorestframework-simplejwt (JWT, 30-day tokens) |
| ORM | Django ORM |
| Database | PostgreSQL 16 |
| Backend tests | pytest-django |
| Container | Docker + docker-compose |

## Final verification

JWT impersonation is fixed in `b5a444b`; the same live forged request changes from HTTP 200 to 401 after signing-key rotation, and a fresh legitimate login still works. Dependency remediation is separate in `e480e07`. Final results: **98 backend + 36 frontend + 12 Airtable SDK tests = 146 passing**, production TypeScript/Vite build passed, all migrations applied, no model drift, and a production-mode Django deployment check passed with warnings treated as failures using disposable configuration. Fresh npm audits report zero vulnerabilities for both projects; OSV reports no findings for the 27 installed Python packages. These scans do not certify the host or a production deployment.

The retained real Airtable responses show **7 created, then 0 created / 7 updated**; remote rows remain **3 → 10 → 10**, with the same seven Airtable record IDs and one row per stable task UUID. They were rechecked against saved snapshots without new external calls. A future replacement token has not been tested because revocation/rotation is still pending. The current backend pauses exports with HTTP 503 until that follow-up is complete.

Original seed rows, all existing audit comments and demo activity are unchanged by hardening. Commits remain separate and nothing has been pushed. The recording and Airtable visual-proof placeholders above are for the user to complete; original setup/initial-test transcripts, workstation eradication and assignment timing remain explicitly unverified in the compliance checklist.
