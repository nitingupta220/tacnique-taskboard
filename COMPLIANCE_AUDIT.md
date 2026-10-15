# Final assignment compliance audit

Corrected 2026-10-15 against the [supplied original assignment](https://docs.google.com/document/d/1Fj4td9MZYZyEH59_IrQGTmNQ9CKTq9OuN8RM6r7gha0/edit), retrieved as text and read in full. The legacy `84cb1a6:ASSIGNMENT.md` differs and is not the authoritative rubric. Code verification covers feature HEAD `88b21fe`, JWT fix `b5a444b`, and dependency fix `e480e07`; recording-link baseline `b60463b` is published. These later corrections change documentation/filenames only. Seed data and existing audit comments are not modified.

**Feature implementation, JWT remediation, dependency checks, all 146 tests, production frontend build and migration checks pass at the last code verification.** Genuine original setup/test captures have now been recovered, and both actual submission links are included and checked. The recording has narration and covers the main stages, but a verified browser-only interval fails literal terminal visibility throughout; its trims prevent certifying uninterrupted coverage. Its duration also exceeds the 90–100 minute timebox. The user last confirmed Airtable token rotation is pending; real export calls remain paused. Workstation eradication and other credential/session remediation are unverified. These limits prevent an unconditional submission/production-ready claim.

The verified public-key impersonation is fixed: the identical live forged request now returns 401 instead of 200, while legitimate login works. Permission tests therefore no longer rely on an identity signed by a public default. The repository security checks pass; broader incident closure remains pending.

## Setup and baseline inspection

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| Inspect backend, frontend, models, APIs, authentication and authorization | PASS | Current source reviewed; README maps important files. Historical review identifies the original task authorization defect. |
| Identify project structure, tests and Airtable-related code | PASS | README structure/test/SDK sections; backend API and SDK plus frontend suites inspected. |
| Read README, start locally, application accessible | PASS | Original running instance is established by historical curl/browser captures; audit HTTP checks confirm frontend 200 and unauthenticated API 401. |
| Preserve original setup output | PASS with capture limits | TERMINAL_LOG sections 1–2 now contain actual 08:14–08:30 UTC tool captures, source timestamps/line numbers and output hashes: virtualenv/install, Node/ICU failure, Docker pull failure, migrations and startup. No historical code or seed command was rerun. |
| Run initial tests and record passing/failing results | PASS with capture limits | Original backend: 15 DB setup errors, then 15 passes on isolated PostgreSQL. Original frontend: runner missing, then 6 passes/1 failed suite (DOM peer missing), then 9 passes; original build type errors also preserved. The original tool truncated the 6,158-line backend failure trace; its retained diagnostic/summary is labeled an excerpt. |
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
| Explain rollback decision | PASS | [DESIGN_NOTES.md](DESIGN_NOTES.md); operation and all event rows roll back together to avoid missing/partial history. |
| Authorization/order/event/rollback tests | PASS | `backend/projects/test_activity.py`, `frontend/src/tests/ProjectActivity.test.tsx`; equivalent UUID no-op regression also passes. |
| API/UI evidence and separate commit | PASS | Eight persisted demo events, viewer browser/API read, `88b21fe`. No historical seed/comment backfill. |

## Part 3c — required Airtable integration

| Requirement | Result | Evidence / limitation |
| --- | --- | --- |
| Project-page export button, Django server endpoint, all project tasks | PASS | ExportButton, ExportView and server-side task query; ignores client-supplied task lists. |
| Admin/member only; viewer/non-member/anonymous denied | PASS | Backend/frontend authorization tests and actual HTTP 403/401 captures. |
| Official npm package for real API calls | PASS | The supplied original expressly requires official `airtable` npm. `backend/airtable/package.json` pins 0.12.2; exporter.mjs imports/constructs that client and calls its makeRequest server side. This meets the rubric directly; no Python substitution, exception or assessor approval is needed. |
| Up to 1,000 tasks, batching/pagination | PASS | 10-record writes, 100-record read pages, 1,000-task SDK and API limit tests. |
| Stable-ID idempotency | PASS | Task ID upsert; ambiguous committed-write retry and duplicate-ID tests. |
| Bounded exponential transient retries; no permanent retries | PASS | Three total attempts, exponential waits/deadline, SDK unbounded 429 retries disabled; tests pass. |
| Isolate bad records, continue remaining export, useful counts | PASS | Rejected batches split diagnostically; permanent singleton failure is not retried; created/updated/failed returned; partial-failure tests pass. Global credential/schema failures stop useless calls and report remaining failures. |
| Credentials server side in ignored environment; no committed credentials | PASS for inspected material | Both env files ignored/untracked, root env mode 0600; configured Airtable token/base ID and new private signing key absent from reachable Git objects and inspected source/assets/docs. This does not establish absence of incident exfiltration. |
| Real connection and two actual exports without duplicates | PASS | Preserved actual HTTP responses: first 7 created, second 0 created/7 updated; remote rows 3→10→10, same seven record IDs, one row per stable task ID; fields and unrelated rows independently rechecked from original snapshots. Retained responses/snapshots rechecked locally after hardening; no new external calls. Replacement-token testing awaits manual rotation. |
| Open Airtable and preserve screenshot or share link | PASS | [Actual shared view](https://airtable.com/appC1ADL6s1JlxKAP/shrz8aTLD3nTVjoVk) opened in the browser without login (HTTP 200). Tasks grid shows all seven original exported stable IDs, five additional distinct IDs and three blank-ID rows: 15 total, 12 unique task IDs. Current visual evidence is separate from the historical two-export snapshots; no export/write occurred during this check. A separate screenshot is optional because the original allows a share link. |
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
| All backend/frontend/SDK tests run at final code verification | PASS | 98 backend + 36 frontend + 12 SDK = **146 passing**, zero final failures. |
| Production frontend build and database migrations | PASS | TypeScript/Vite build passed; all migrations applied; migrate --check, makemigrations --check --dry-run, and normal Django check pass. Production-mode deploy check also passes with warnings treated as failures; it uses disposable config, not actual production credentials. |
| Review/design/security documents checked | PASS | Historical/current claims distinguished, categories/links corrected, rollback rationale and remaining risks retained. |
| Terminal evidence required order with credentials redacted | PASS with capture limits | Canonical TERMINAL_LOG.md: recovered setup → original initial failures/passes → bug proof → same-request fix proof → real Airtable exports → comments/activity demos → final tests, followed by dated audit corrections. The actual shared view is also linked at the export stage. The original backend failure traceback is explicitly truncated. Credentials/wrapped wire traces stay private; only the user-authorized public share URL identifies the base. |
| README setup/tests/env/actual submission links | PASS | Fresh Docker/manual steps, environment variables, isolated tests, seeding caution, inspection ports and official SDK; actual Loom/Airtable links replace both placeholders. Links to canonical DESIGN_NOTES.md resolve. |
| Actual recording link, playback and narration | PASS | Public [Loom recording](https://www.loom.com/share/5daf18e351574c57b6d9ce1c2878feaf); H.264 video/AAC audio verified, 1,107 caption cues and sampled frames cover cloning through final 146-test narration. Method and limits below. |
| Entire session with terminal visible throughout | FAIL / continuity not verified | At playback 00:09:15 the Airtable website fills the screen and the terminal is not visible. Loom reports 118 trimmed ranges totaling 251.649 seconds. Sampled inspection cannot prove all remaining intervals are complete or credential-free. Do not describe this as an uncut continuous recording. |
| Full commit history, separate changes, seed integrity, no squash | PASS | Original linear history retained: `70f2bd9` → `75e6d4a` → `1c87642` → `21988bd` → `88b21fe` → `b5a444b` → `e480e07` → `be02241` docs → `b60463b` recording link. No history rewriting. Unsafe original loader remains in older revisions; do not execute them. |
| Documentation committed and published | PASS in the final published correction | This separate documentation correction follows published baseline `b60463b`. Normal master-to-origin/master publication, local/remote HEAD equality and clean status are verified after creating the correction commit; its SHA is reported at delivery. No environment, application/test or seed files are included. |
| Optional repository AI-conversation hook | NOT AN ORIGINAL REQUIREMENT | Not verified for existing commits. The supplied original requires a screen recording, not an AI-conversation archive; absence of hook capture is not an assignment blocker. Recovered evidence copies selected original tool responses only, not conversation text. |
| Original 90–100 minute timebox | FAIL | Loom reports source duration 03:19:54.795 and playable duration 03:15:43.146, both greater than 100 minutes. The recording includes an incident investigation and both optional features; no timing exception has been established. |
| Submit within 24 hours of receipt | NOT VERIFIED | Assignment receipt timestamp was not supplied. Recording creation date alone does not establish receipt or submission time. |

A fresh Docker image build, Airtable PAT revocation, production deployment and host eradication were not performed or attested. The public Airtable shared-view UI was reviewed as documented above; no authenticated base edit or export was performed. The local application signing key was rotated; these are distinct actions. The advisory scan covers installed Python packages and both npm projects as of this check, not the entire host/container operating system. Terminal evidence records actual command outputs, the npm resolver failure and uv recovery for a virtualenv without pip. The original setup/initial-test evidence was recovered from original tool captures, not recreated with new runs. No application tests/build were rerun for this documentation-only correction; the last 146-test/build/migration results remain tied to their actual code verification.

## Recording verification

The public Loom link opens without signing in; the title is “TaskBoard Security Fixes and Airtable Export.” Media inspection confirms H.264 video at up to 1728×1080 and AAC audio. The actual captions contain 1,107 cues from the opening clone/setup narration through the final spoken 146-test/build/migration summary. Main stage markers: 00:00 setup; 00:20:48 review; 00:37:40 SQL fix; 00:51:22 Airtable; 01:56:26 comments; 02:18:06 activity; 03:14:51 final security/submission discussion. These markers describe recording content, not independent proof that each spoken claim is correct.

Verification used actual caption text, stream metadata and sampled decoded frames, including 00:00:15 (clone terminal), 00:09:15 (browser-only Airtable homepage), and 03:15:00 (terminal with final verification/documentation results). Most sampled frames show the terminal, but the browser-only frame disproves literal terminal visibility throughout. The source duration is 11,994.795 seconds and playback is 11,743.146 seconds; 118 trim ranges account for 251.649 seconds. Their reason is not established, and an uncut source was not provided. Continuous coverage and complete secret absence cannot be certified from samples. Raw captions, frames and signed media URLs are kept outside Git; no signed playback credentials are included in submission documents.

## Remaining follow-ups, in priority order

1. Revoke the potentially exposed Airtable token on a trusted device, configure a replacement with only base record read/write permissions, and investigate the workstation/other exposed sessions. Existing historical exports and the current public shared view do not verify rotation or host remediation. Remove the empty backend key override only after trusted configuration.
2. Address or disclose the recording's browser-only interval and trimmed coverage, and seek the assessor's decision on the exceeded timebox. Do not fabricate an uninterrupted original session or retrospectively claim it met 100 minutes. The 24-hour deadline remains unverified without the receipt time.
3. Both actual deliverable links are present. Keep the public shared view and recording accessible to reviewers; an additional screenshot is optional. The delivery check confirms publication of this separate documentation correction without rewriting history.
4. Validate trusted production TLS, hosts and secret-manager settings before deployment. The supplied Compose file remains a development stack. The original complete backend failure traceback cannot be recovered beyond the tool's retained truncated output; that limitation remains explicit.
