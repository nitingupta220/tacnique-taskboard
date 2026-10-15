# Taskboard focused code review

Reviewed commit: `5f58e52` on 2026-10-15. Scope: task-update authorization, task search, and the four verified issues with the greatest business impact found in this review. At that review stage, no fixes, application/test source changes, seed changes, or commits were made. All file/line references below refer to that reviewed commit; later edits moved those lines. Use `git show 5f58e52:<path>` to inspect the historical locations.

The existing seeded application runs at `http://127.0.0.1:3000`, with its backend at `http://127.0.0.1:8001` and database `taskboard_inspection` on PostgreSQL port `55432`. Actual curl commands, complete HTTP responses, and browser observations are preserved in [TERMINAL_LOG.md](TERMINAL_LOG.md), evidence IDs E01–E20 and B01–B04. Credential-bearing raw wire traces are omitted from the submission copy; original captures remain private.

| Rank | Finding | Category | Severity | Business impact |
|---|---|---|---|---|
| 1 | Task-search SQL injection exposes other projects' tasks | Security: SQL injection, CWE-89 | High / P1 | A viewer can retrieve private task contents and identifiers across projects. |
| 2 | Task PATCH omits project membership and role authorization | Security: missing object authorization, CWE-862 | High / P1 | An authenticated non-member or viewer can change a task's status and other editable fields. |
| 3 | Editing an assigned task generates an unintended unassignment | Data Integrity: API contract mismatch | Medium / P2 | Ordinary task edits can remove ownership and disrupt accountability. |
| 4 | Airtable export is a placeholder that returns success without exporting | Architecture: missing integration | Medium / P2 | The documented export workflow transfers no tasks, including for nonempty projects. |

P1 means prioritize for correction; P2 means schedule after the security boundaries are restored. SQL injection ranks first because the lowest permitted project role can discover private task contents and IDs without already knowing a private task UUID. Those IDs also satisfy the prerequisite for finding 2. These are project boundaries; no organization/tenant model was assumed.

**1. Task-search SQL injection exposes other projects' tasks**

- **References:** [backend/projects/views.py:104–123](backend/projects/views.py#L104), especially string interpolation at lines 113–120.
- **Description:** The endpoint checks membership in the URL's project, then inserts `q` directly into an SQL string. The payload `') OR TRUE -- ` closes the search expression and makes the overall WHERE condition true, bypassing the project filter.
- **Verified impact:** Seeded `dev@example.com` is only a viewer on Q3 Launch. Its normal task listing returns seven tasks; direct access to Onboarding's tasks returns 403. The injected Q3 search returns 200 with all 12 tasks, including five Onboarding tasks. This exposes descriptions, status, assignee/creator IDs, task UUIDs, and timestamps from a forbidden project.
- **Evidence:** E01–E07 on the original running backend, with no database-writing payload. E03 establishes the caller's role; E05 establishes the forbidden boundary; E07 contains the successful exploit.
- **Recommended fix:** Preserve the project filter and express search using Django ORM `Q` conditions with `icontains`, or bind search values as SQL parameters. Never interpolate request input into SQL. Add regression coverage for quotes and SQL-shaped search terms, asserting that every returned task belongs to the requested project.

Replay template, using the viewer token returned by E01 or a fresh login as `dev@example.com` with the public seed password documented in README:

```bash
curl --http1.1 --noproxy '*' --include --get \
  --header "Authorization: Bearer ${VIEWER_TOKEN}" \
  --data-urlencode "q=') OR TRUE -- " \
  'http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks'
```

The actual captured request and HTTP response are in E07. Credentials are now redacted; raw wire traces containing wrapped token fragments are omitted from the submission log. Original byte counts/digests describe the original private capture. The replay template above is not presented as the original capture.

| Actual request as the same viewer | Actual response |
|---|---|
| Q3 tasks, without search | HTTP 200; seven Q3 tasks |
| Onboarding tasks directly | HTTP 403; `{"error":"forbidden"}` |
| Q3 search for `review-no-match-20261015` | HTTP 200; `{"tasks":[]}` |
| Q3 search for `') OR TRUE -- ` | HTTP 200; 12 tasks, including five forbidden Onboarding tasks |

Forbidden project ID: `eb475492-eb0b-4660-9d90-9f9d603ec069`. One leaked example is task `19ad52e0-9d81-4a9b-927b-06d69f740065`, “Wireframe new welcome screens.” The complete leaked records are preserved after E07. No claims about password extraction, arbitrary database writes, remote execution, or production exploitation were inferred from this read-only proof.

**2. Task PATCH omits project membership and role authorization**

- **References:** [backend/projects/views.py:164–185](backend/projects/views.py#L164). Compare the membership/role checks in DELETE at [lines 187–197](backend/projects/views.py#L187); global [IsAuthenticated at settings.py:42–48](backend/taskboard/settings.py#L42) authenticates the caller but does not authorize the target task.
- **Description:** PATCH retrieves a task by UUID and applies updates without calling `_get_membership` or `_can_edit_tasks`. The task UUID is the only object-level prerequisite once the caller has a valid account.
- **Verified impact:** A review-only non-member gets 403 for the target project, then PATCHes its task from `todo` to `done` and receives 200 with the updated task. A review-only viewer also receives 200 for the same update while DELETE correctly returns 403. This confirms both missing project isolation and missing viewer restrictions. Other accepted editable fields are title, description, and assignee; only status changes were used to demonstrate this authorization bypass.
- **Evidence:** E10–E18. These are real HTTP requests to the same unmodified Django views on port 8002, using a separate disposable database and a transaction boundary that rolls back every request. They were not sent as writes to the seeded backend. Task serialization reads back the updated database row before rollback; subsequent reads confirm the original status and assignment remain intact.
- **Recommended fix:** Resolve the task's project and require an appropriate membership and `admin`/`member` role before any mutation or task response. Apply one consistent object-authorization policy across create, update, and delete. Cover unauthenticated users, non-members, viewers, members, and admins, including unchanged task contents after rejected requests.

**3. Editing an assigned task generates an unintended unassignment**

- **References:** [backend/projects/serializers.py:8–25](backend/projects/serializers.py#L8); [frontend/src/types/index.ts:10–21](frontend/src/types/index.ts#L10); [frontend/src/components/TaskDetail.tsx:19](frontend/src/components/TaskDetail.tsx#L19) and [lines 45–52](frontend/src/components/TaskDetail.tsx#L45); [backend/projects/views.py:180–185](backend/projects/views.py#L180).
- **Description:** The API returns `assignee_id`; the editor reads `task.assigneeId`. No response mapping supplies the camelCase property. The editor therefore initializes the existing assignee to an empty string and always submits `assigneeId: null` on Save unless the user reselects someone.
- **Verified impact:** On the seeded board, “Finalize launch date with marketing” shows Meera Iyer on its card, but opening the editor shows “unassigned” selected. The seeded editor was canceled without saving. In the disposable database, submitting the unchanged payload generated by that code returns 200 with both `assignee_id` and `assignee` null for a previously assigned task. That update was rolled back.
- **Evidence:** B01–B04 show the actual UI mismatch. E18–E20 verify the assignment-clearing request and response separately. E19 is a curl replay of the payload derived from the editor's observed initial state and `onSave` code, not a captured browser Save request.
- **Recommended fix:** Adopt one response-field convention or map API responses at the boundary before constructing frontend state. Initialize the editor from the actual assignee and avoid sending assignment changes when the field is untouched. Add an API-to-editor regression check proving that changing only a title preserves the existing assignee.

**4. Airtable export is a placeholder that returns success without exporting**

- **References:** [backend/projects/views.py:234–243](backend/projects/views.py#L234); the promised behavior is in [README.md:113–126](README.md#L113). `pyairtable` is listed in [backend/requirements.txt:6](backend/requirements.txt#L6).
- **Description:** After permission checks, the endpoint only serializes local tasks and returns `{'exported': 0, 'tasks': ...}`. It never constructs an Airtable client, reads Airtable configuration, or performs an external write. The README's referenced `backend/projects/airtable_mock.py` is also absent.
- **Verified impact:** An authenticated admin exporting Q3 Launch receives HTTP 200, seven local task records, and `exported: 0`. The documented transfer cannot occur through this implementation, regardless of whether credentials are supplied. Consumers treating HTTP 200 as completion can proceed without the expected Airtable data.
- **Evidence:** E08–E09 on the original seeded backend plus inspection of the complete view. No Airtable write was attempted; this is an unimplemented code path, not a verified Airtable-service or credential failure.
- **Recommended fix:** Implement the configured Airtable integration with an explicit field mapping, correct exported counts, and surfaced configuration/API failures. Until implemented, return an explicit unsupported response rather than HTTP 200 for a nonempty export. Cover success, missing configuration, external failures, and denied roles with an isolated API double.

**Seed preservation and review limits**

The primary seeded database was only read. All write-based checks used `taskboard_review_probe_20261015`, created empty with new review-only fixtures. A temporary external WSGI wrapper added transaction rollback around the existing views; it did not add permission checks or modify application source. Full fixture-row comparisons, including `updated_at`, confirmed rollback. The temporary listener and database were removed after verification.

Every row and column of the primary `users`, `projects`, `memberships`, and `tasks` tables was compared before and after the review. The complete canonical snapshots are equal, including timestamps and assignments. Both SHA256 values are:

```text
8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe
```

Seed counts remain five users, three projects, eight memberships, and 12 tasks. The seeded app stays available on ports 3000/8001. At the end of that review stage, only `REVIEW.md` and `TERMINAL_LOG.md` were added to the working tree; no bugs were fixed and no commit was created. This is a focused review, not an exhaustive security audit.

## Final audit status — 2026-10-15

The four original findings remain valid historical review evidence; they are not four open issues in the final application.

| Original finding | Current status | Fix / current reference |
| --- | --- | --- |
| Search SQL injection | Resolved | `70f2bd9`; parameter binding in `backend/projects/views.py` task search; SQL regression suite passes. Same exploit payload returned no tasks after the fix. |
| Missing task PATCH authorization | Resolved | `88b21fe`; `backend/projects/views.py:196` now enforces project membership and admin/member role. API tests and live denied-write evidence cover viewers and outsiders. |
| Unintended unassignment | Resolved for the task editor | `88b21fe`; `frontend/src/components/TaskDetail.tsx:20` initializes from the server's nested assignee. Frontend regression verifies the submitted assignment is preserved. The broader snake_case/camelCase DTO mismatch remains technical debt. |
| Placeholder Airtable export | Resolved | `75e6d4a`; real server-side official npm SDK, batching/upsert/retries/results; two real exports independently verified. Original brief's `pyairtable` choice was explicitly overridden by the user's npm requirement. |

The later verified development-key JWT forgery was fixed in `b5a444b`: an identical live forged request changed from HTTP 200 to 401 after private signing-key rotation, while fresh login still succeeds. Dependency remediation in `e480e07` passes all 146 tests and fresh audits (zero npm/installed-Python findings). Remaining workstation/credential incident follow-up is documented in [security_notes.md](security_notes.md). Submission gaps are in [COMPLIANCE_AUDIT.md](COMPLIANCE_AUDIT.md). The original four issues were not reprioritized or replaced after their fixes.
