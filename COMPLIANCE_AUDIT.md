# Final assignment compliance audit

Finalized 2026-10-15 after feature HEAD `88b21fe`, JWT fix `b5a444b`, and dependency fix `e480e07`. Baseline brief: `git show 84cb1a6:ASSIGNMENT.md`; later explicit user requirements take precedence. Fixes and final documentation are committed separately, with no squash, history rewrite or push. Seed data and existing audit comments remain unchanged.

**Feature implementation, JWT remediation, dependency checks, all 146 tests, production frontend build and migration checks pass.** The actual recording/Airtable screenshot are intentionally left as user-supplied placeholders. Original setup/initial-test transcripts are missing from retained evidence; they have not been fabricated. The user will manually rotate the potentially exposed Airtable token; real API testing is paused until then. Workstation eradication and other credential/session remediation are unverified. These external incident and submission follow-ups prevent claiming complete submission/production readiness.

The verified public-key impersonation is fixed: the identical live forged request now returns 401 instead of 200, while legitimate login works. Permission tests therefore no longer rely on an identity signed by a public default. The repository security checks pass; broader incident closure remains pending.

## Setup and baseline inspection

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| Inspect backend, frontend, models, APIs, authentication and authorization | PASS | Current source reviewed; README maps important files. Historical review identifies the original task authorization defect. |
| Identify project structure, tests and Airtable-related code | PASS | README structure/test/SDK sections; backend API and SDK plus frontend suites inspected. |
| Read README, start locally, application accessible | PASS | Original running instance is established by historical curl/browser captures; audit HTTP checks confirm frontend 200 and unauthenticated API 401. |
| Preserve original setup output | FAIL | No original setup transcript was found in retained evidence. Current topology/checks are labeled as current, not invented initial output. |
| Run initial tests and record passing/failing results | FAIL (evidence gap) | No complete initial pre-change backend/frontend test output was found. SQL regression red/green logs and later suites are retained but are not relabeled as the initial suite. |
| Original seed and existing audit comments unchanged | PASS | Every original row/column compared by ID with the original private snapshot; all four pre-existing comments also unchanged. Seed source and initial migrations are unchanged. |

## Part 1 — review

| Requirement | Result | Evidence |
| --- | --- | --- |
| Top four genuine issues prioritized by business impact | PASS | REVIEW: SQL injection, task PATCH authorization, unintended unassignment, placeholder export. All four were originally verified; current remediation status is separate. |
| File/line, allowed category, severity, impact, 2–3 sentence description, recommended fix | PASS | Historical line references are explicitly tied to reviewed commit `5f58e52`; export category normalized to Architecture. |
| At least one real curl bug proof and response | PASS | E07 in TERMINAL_LOG: viewer SQL search returns all 12 tasks including forbidden project data. |
| No speculative vulnerability claims | PASS with scope limits | Historical write probes used a separate rollback database; security findings distinguish direct verification from advisory/configuration risk. |

## Part 2 — highest-priority SQL fix

| Requirement | Result | Evidence |
| --- | --- | --- |
| Replace unsafe interpolation with parameter binding/ORM | PASS | Commit `70f2bd9`, bound project/search values in task search. |
| Preserve normal search/API behavior and project isolation | PASS | SQL-shaped strings, case-insensitive title/description, quote, wildcard, ordering, empty-query and non-member regressions pass. |
| Regression tests and existing backend tests | PASS | Final backend suite: 98 passing, including SQL regressions. |
| Exact before/after curl and corrected response | PASS | Original `before.request.txt` and `after.request.txt` are byte-identical; before HTTP 200/12 tasks, after HTTP 200/0 tasks. Submission copies redact authorization only. |
| Separate meaningful commit | PASS | `70f2bd9`; no history rewriting. |

## Part 3a — comments

| Requirement | Result | Evidence |
| --- | --- | --- |
| Chronological task comments with author/body/time | PASS | Stable oldest-first ordering; task comment API/UI and ordering tests. |
| Admins/members post, viewers read, outsiders denied by Django | PASS | Role/anonymous/isolation tests and live curl captures. |
| Append-only: no editing/deletion | PASS | No mutation routes; collection 405/detail 404; parent deletion with comments returns 409. Immutability tests pass. |
| Existing task UI and backend architecture | PASS | TaskDetail mounts TaskComments using existing API client, styling and query patterns. |
| Tests for permissions/order/immutability | PASS | `backend/projects/test_comments.py`, `frontend/src/tests/TaskComments.test.tsx`. |
| API and UI demo, evidence and separate commit | PASS | Retained real API and browser text evidence; separate non-seed demo project; `21988bd`. |

## Part 3b — activity

| Requirement | Result | Evidence |
| --- | --- | --- |
| Task creation, status/assignee changes, comment additions | PASS | All four event types verified twice through real API/UI demos; automated event/no-op tests. |
| Store actor, action, timestamp, project and relevant change details | PASS | Activity model and read-only serialization, saved task/title and before/after snapshots. |
| Project detail feed, newest first, project members only | PASS | Latest 50 events, deterministic ties, project/user cache isolation, all membership roles read; outsider/anonymous denied. |
| Transactions consistent with original write | PASS | `transaction.atomic()` and task row lock; real PostgreSQL rollback tests for creation, combined update and comment insert failure. |
| Explain rollback decision | PASS | design_notes.md; operation and all event rows roll back together to avoid missing/partial history. |
| Authorization/order/event/rollback tests | PASS | `backend/projects/test_activity.py`, `frontend/src/tests/ProjectActivity.test.tsx`; equivalent UUID no-op regression also passes. |
| API/UI evidence and separate commit | PASS | Eight persisted demo events, viewer browser/API read, `88b21fe`. No historical seed/comment backfill. |

## Part 3c — required Airtable integration

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| Project-page export button, Django server endpoint, all project tasks | PASS | ExportButton, ExportView and server-side task query; ignores client-supplied task lists. |
| Admin/member only; viewer/non-member/anonymous denied | PASS | Backend/frontend authorization tests and actual HTTP 403/401 captures. |
| Official npm package for real API calls | PASS (user override) | `airtable@0.12.2` imports/constructs the official client in the server-side Node bridge and makes real calls through its makeRequest. Current explicit npm requirement is satisfied; no Python SDK substitution. The original pyairtable rubric wording remains a disclosed difference. |
| Up to 1,000 tasks, batching/pagination | PASS | 10-record writes, 100-record read pages, 1,000-task SDK and API limit tests. |
| Stable-ID idempotency | PASS | Task ID upsert; ambiguous committed-write retry and duplicate-ID tests. |
| Bounded exponential transient retries; no permanent retries | PASS | Three total attempts, exponential waits/deadline, SDK unbounded 429 retries disabled; tests pass. |
| Isolate bad records, continue remaining export, useful counts | PASS | Rejected batches split diagnostically; permanent singleton failure is not retried; created/updated/failed returned; partial-failure tests pass. Global credential/schema failures stop useless calls and report remaining failures. |
| Credentials server side in ignored environment; no committed credentials | PASS for inspected material | Both env files ignored/untracked, root env mode 0600; configured Airtable token/base ID and new private signing key absent from reachable Git objects and inspected source/assets/docs. This does not establish absence of incident exfiltration. |
| Real connection and two actual exports without duplicates | PASS | Preserved actual HTTP responses: first 7 created, second 0 created/7 updated; remote rows 3→10→10, same seven record IDs, one row per stable task ID; fields and unrelated rows independently rechecked from original snapshots. Retained responses/snapshots rechecked locally after hardening; no new external calls. Replacement-token testing awaits manual rotation. |
| Open Airtable and preserve screenshot or share link | FAIL (submission evidence gap) | No actual Airtable screenshot/share link exists in retained artifacts. API evidence does not establish that a person opened the base UI. README has a clearly marked placeholder. |
| Automated authorization/idempotency/retry/partial-failure tests; separate commit | PASS | 12 SDK tests and backend/frontend export coverage; `75e6d4a`. |

## Security incident follow-up

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| Determine loader behavior, origin and impact without executing it | PASS | security_notes.md: static decoding and Git origin, inert samples private; no malicious historical code executed during investigation/audit. |
| Restore legitimate PostCSS, inspect related scripts/dependencies | PASS | `1c87642` removed the loader; `e480e07` legitimately replaces the v3 plugin with @tailwindcss/postcss for Tailwind 4. New clean config hash is in security_notes.md; historical hashes retained. Related source/archive verification recorded. |
| Assess environment/credential exposure | PASS for assessment; remediation incomplete | Arbitrary downstream code could read credentials. Exfiltration cannot be ruled out; rotation and workstation persistence investigation are not verified complete. |
| Build/tests, document remediation, separate security commit | PASS | Historical checkpoint plus final fresh suites/build; `1c87642`. |
| JWT impersonation and production configuration | PASS for repository | `b5a444b`: same live forged request 200→401; both public keys rejected; legitimate login/GET 200. Private signing key rotated locally, production rejects debug/wildcards/weak DB password, security middleware/CORS/HTTPS checks enabled. Production-mode deploy check has zero warnings using disposable config. No production deployment is claimed. |
| Dependency vulnerabilities | PASS for checked advisories | `e480e07`: frontend and SDK npm audits both zero; OSV scan of all 27 installed Python distributions has no findings. Vite/Vitest/Router/Tailwind and pytest upgraded; all tests/build and browser comparison pass. |
| External credential/host incident closure | PENDING USER / EXTERNAL | User confirmed Airtable PAT is not yet revoked; will rotate manually. Exports are paused (503) with an empty runtime override. Workstation persistence, other credentials/sessions, damaged global npm and trusted-host restoration remain unverified. Repository cleanup does not prove secret safety. |

## Final verification and submission

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| All backend/frontend/SDK tests freshly run | PASS | 98 backend + 36 frontend + 12 SDK = **146 passing**, zero final failures. |
| Production frontend build and database migrations | PASS | TypeScript/Vite build passed; all migrations applied; migrate --check, makemigrations --check --dry-run, and normal Django check pass. Production-mode deploy check also passes with warnings treated as failures; it uses disposable config, not actual production credentials. |
| Review/design/security documents checked | PASS | Historical/current claims distinguished, categories/links corrected, rollback rationale and remaining risks retained. |
| Terminal evidence required order with all credentials redacted | PASS for structure/redaction; historical gaps remain | Canonical filename TERMINAL_LOG.md. Setup → initial tests → bug proof → fix proof → Airtable/security checkpoint → comments/activity demos → final audit/tests. Missing original setup/initial-test output is explicit. Intact tokens/passwords/base identifiers redacted; 26 wrapped wire trace blocks omitted, separately captured request/response retained. Private originals remain outside Git. |
| README setup/tests/env/recording placeholder | PASS | Updated fresh Docker/manual steps, environment variables, isolated-test commands, seeding caution, current ports/runtime, SDK override, real-link placeholders. |
| Actual screen recording with narration/terminal visible | FAIL | No actual link or recording evidence; original brief says submissions without it are not evaluated. Placeholder alone is insufficient. |
| Full commit history, separate changes, seed integrity, no squash/push | PASS | `70f2bd9` → `75e6d4a` → `1c87642` → `21988bd` → `88b21fe` → `b5a444b` → `e480e07` → separate submission-documentation commit. No push or history rewriting. Unsafe original loader remains in older revisions; do not execute them. |
| Submission files committed separately | PASS in final documentation commit | README, REVIEW, design_notes, security_notes, TERMINAL_LOG and this checklist are included together after the separate JWT and dependency commits. Credential scans and whitespace/link checks completed before staging; final clean status is checked after the commit. No env or seed files included. |
| AI conversation capture | NOT VERIFIED for existing commits | Hook supplied but not configured; no .ai-conversations directory. No transcript was invented or copied from unrelated sessions. |
| Original 90–100 minute timebox / 24-hour deadline | NOT VERIFIED / timing concern | Preserved review-to-activity evidence already spans more than 100 minutes; an incident investigation intervened. No assignment receipt time or recording establishes the deadline/session timing. Do not claim timing compliance. |

A full fresh Docker image build, current live Airtable UI review, Airtable PAT revocation, production deployment and host eradication were not performed or attested. The local application signing key was rotated; these are distinct actions. The advisory scan covers installed Python packages and both npm projects as of this check, not the entire host/container operating system. Terminal evidence records actual command outputs, the npm resolver failure and uv recovery for a virtualenv without pip; no missing transcript was recreated.

## Remaining follow-ups, in priority order

1. Revoke the potentially exposed Airtable token on a trusted device; configure a replacement with only base record read/write permissions. Investigate the affected workstation and other exposed credentials/sessions. Restart the backend without the empty-key override only after trusted configuration. Existing two-export evidence is valid historical evidence, not a test of that future token.
2. Add the actual narrated screen-recording URL and Airtable screenshot/share link to the explicit README placeholders. No placeholder is presented as completed evidence.
3. Recover original setup/initial-test output if available; otherwise retain the honest evidence gap. Assignment timing and earlier AI-conversation capture cannot be attested retroactively.
4. Use a trusted deployment environment and validate actual production TLS, hostnames and secret-manager configuration before deployment. The supplied Compose file remains a development stack.
