# Taskboard terminal evidence — final compilation

Originally compiled 2026-10-15T11:24:53.108804+00:00 at feature HEAD `88b21fe`; updated after security hardening at source HEAD `e480e07`, then corrected against the supplied original assignment after recording-link commit `b60463b`. Original setup/test captures have now been recovered into sections 1–2; later historical statements that they were missing describe earlier searches. Earlier checkpoint results remain historical; the final hardening results below supersede their open JWT/dependency findings. This is an ordered compilation of retained real captures, not a newly invented continuous terminal session. Original capture dates are retained. Required order: setup → initial tests → bug proof → fix proof → real Airtable export → comments/activity demos → final audit/tests. The intervening PostCSS investigation remains between export and comments, where it occurred.

Credential handling: tokens, passwords and configured base identifiers are redacted. Raw curl wire traces split credentials across fixed-width lines, so those 26 trace blocks are omitted; separately captured requests and HTTP responses remain. Original Content-Length/byte-count/SHA values describe the private original captures, not the redacted text. Historical statements about an unchanged raw prefix/local-only log describe those earlier checkpoints, before this final redaction/reordering. The final filename is normalized to `TERMINAL_LOG.md`; originals remain outside the repository in a mode-0700 directory.

Original pre-audit log SHA-256: `d66e387760fd5f2aa95635857ba3f4b86d7a74f6629fa4520b1056bd513b3cee`. No credential value is printed here. The raw original is not a submission file.

## 1. Original setup output and issues

Recovered on 2026-10-15 from the original local tool-execution log `rollout-2026-10-15T13-38-49-01a13e9b-5358-7f33-b922-0c65ce5fe070.jsonl`, selecting only setup/test commands and their actual responses from 08:14–08:30 UTC. Source line numbers below refer to that private JSONL. No historical commands, dependencies, infected config, migrations or seed operations were rerun to recover these captures. No conversation text has been copied. Passwords are redacted; terminal color escapes are removed. Setup and tests originally ran concurrently, so their UTC timestamps overlap across these required sections.

### Python environment creation

Original command at 2026-10-15T08:14:46.063Z; working directory `repository root`. Captures: 2026-10-15T08:14:47.297Z (source line 52).

```bash
uv venv --python /usr/local/bin/python3.12 .venv && uv pip install --python .venv/bin/python -r backend/requirements.txt
```



```text
Using CPython 3.12.11 interpreter at: /usr/local/opt/python@3.12/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

SHA-256 of the retained original output chunks before redaction: `677ac3d163f5e9657e53cc9a266fefecbba9403ab8aa2138d73aefae803d2fb0`.

The same install completed with exit 0, captured at 2026-10-15T08:15:05.248Z (source line 61; that wrapper also contains an unrelated truncated skill read, excluded here):

```text
Resolved 26 packages in 1.98s
Downloading django (7.9MiB)
Downloading pygments (1.2MiB)
Downloading psycopg2-binary (3.6MiB)
Downloading pydantic-core (2.1MiB)
 Downloaded pydantic-core
 Downloaded psycopg2-binary
 Downloaded pygments
 Downloaded django
Prepared 20 packages in 4.03s
Installed 26 packages in 426ms
 + annotated-types==0.8.0
 + asgiref==3.12.1
 + certifi==2026.7.22
 + charset-normalizer==3.5.2
 + django==5.2.18
 + django-cors-headers==4.9.0
 + djangorestframework==3.18.3
 + djangorestframework-simplejwt==5.5.1
 + idna==3.20
 + inflection==0.5.1
 + iniconfig==2.3.1
 + packaging==26.3
 + pluggy==1.6.0
 + psycopg2-binary==2.9.13
 + pyairtable==2.3.7
 + pydantic==2.14.1
 + pydantic-core==2.50.1
 + pygments==2.21.0
 + pyjwt==2.15.1
 + pytest==8.4.2
 + pytest-django==4.14.0
 + requests==2.34.2
 + sqlparse==0.6.0
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 + urllib3==2.8.0
```

Retained dependency-output SHA-256: `81495daf473494db01d39d329d6e7f90fd2cbe165cb714bb79bc203608e548f2`. The historical `pyairtable` dependency was present in the starter; it is not the original assignment's SDK requirement.

### Initial Node/npm failure

Original command at 2026-10-15T08:14:46.063Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:14:47.297Z (source line 52).

```bash
npm install --no-package-lock --no-audit --no-fund
```

Exit 134: the system Node binary could not load ICU. This is a genuine original setup failure.

```text
dyld[36334]: Library not loaded: '/usr/local/opt/icu4c/lib/libicui18n.74.dylib'
  Referenced from: '/usr/local/Cellar/node/22.6.0/bin/node'
  Reason: tried: '/usr/local/opt/icu4c/lib/libicui18n.74.dylib' (no such file), '/usr/local/lib/libicui18n.74.dylib' (no such file), '/usr/lib/libicui18n.74.dylib' (no such file), '/usr/local/Cellar/icu4c@78/78.3/lib/libicui18n.74.dylib' (no such file), '/usr/local/lib/libicui18n.74.dylib' (no such file), '/usr/lib/libicui18n.74.dylib' (no such file)
```

SHA-256 of the retained original output chunks before redaction: `110918ec9a532f6d96ce8a9109901e24c5baafdd5f98d76d6186f3964a893b2e`.

### Frontend dependencies installed using the available Node runtime

Original command at 2026-10-15T08:16:30.270Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:17:56.696Z (source line 148).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
npm install --no-package-lock --no-audit --no-fund
```

The original command selected the existing NVM Node 22.20.0 runtime. Exit 0; a missing DOM peer dependency still affected the first completed frontend suite below.

```text
added 234 packages in 1m
```

SHA-256 of the retained original output chunks before redaction: `8f582f9453eacdefd82c521b710ad61325d7df4fe97c8bf5d3b52fcb486c523b`.

### Original frontend server startup

Original command at 2026-10-15T08:18:07.833Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:18:30.805Z (source line 162).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
npm run dev -- --host 127.0.0.1 --strictPort
```

Original server startup output; the proxy was subsequently pointed to the inspection backend on port 8001.

```text
> taskboard-frontend@1.0.0 dev
> vite --host 127.0.0.1 --strictPort

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

  VITE v5.4.21  ready in 4523 ms

  ➜  Local:   http://127.0.0.1:3000/
```

SHA-256 of the retained original output chunks before redaction: `1709e0b3a2a3bb116f2134415a505626454c2ed06ff03993b71c2eae7e10e150`.

### PostgreSQL image pull failed

Original command at 2026-10-15T08:18:44.602Z; working directory `repository root`. Captures: 2026-10-15T08:19:06.698Z (source line 175); 2026-10-15T08:20:09.813Z (source line 195).

```bash
docker run --name taskboard-inspection-db-20261015 --label taskboard.purpose=read-only-codebase-inspection --memory=256m -d -p 127.0.0.1:55432:5432 -e POSTGRES_DB=taskboard_inspection -e POSTGRES_USER=taskboard -e POSTGRES_PASSWORD=<REDACTED> postgres:16-alpine
```

Exit 125: Docker Hub request timeout. A new postgres:16-alpine image was not obtained.

```text
Unable to find image 'postgres:16-alpine' locally
docker: Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers).
See 'docker run --help'.
```

SHA-256 of the retained original output chunks before redaction: `3275ed0c9c3c8ee9357817c61f6881e2e63d79fc5975f38cd2ad9ed909934328`.

The original setup then reused the already-cached PostgreSQL image `9cfa957fae1d` in a separate loopback-bound container; actual migration output below identifies it as PostgreSQL **17.6**, rather than the Compose default 16. Existing application databases were not reseeded during setup. The first `pg_isready` probe preceded readiness; migrations subsequently succeeded.

### Isolated database and initial migrations

Original command at 2026-10-15T08:21:37.313Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/backend`. Captures: 2026-10-15T08:22:04.406Z (source line 238).

```bash
docker exec taskboard-inspection-db-20261015 pg_isready -U taskboard -d taskboard_inspection; docker exec taskboard-inspection-db-20261015 postgres --version; POSTGRES_DB=taskboard_inspection POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python manage.py migrate --noinput && POSTGRES_DB=taskboard_inspection POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python -m pytest -v --tb=short
```

Only the migration/setup portion of this combined command output is shown here; its pytest continuation is in section 2. All 16 original migrations applied successfully.

```text
/var/run/postgresql:5432 - no response
postgres (PostgreSQL) 17.6 (Debian 17.6-1.pgdg12+1)
Operations to perform:
  Apply all migrations: auth, contenttypes, projects, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying users.0001_initial... OK
  Applying projects.0001_initial... OK
```

SHA-256 of the retained original output chunks before redaction: `93db05d23cb3137f2df757fa50db52428efeb6c01ac7d2d07924f63b0f25c47f`.

### Original backend startup and accessibility

Original command at 2026-10-15T08:21:59.319Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/backend`. Captures: 2026-10-15T08:22:34.503Z (source line 245).

```bash
POSTGRES_DB=taskboard_inspection POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python manage.py runserver 127.0.0.1:8001 --noreload
```

Original retained server access lines. Subsequent health requests in source line 255 returned HTTP 200 through both the backend and frontend proxy; login verification follows the authorized seed load below.

```text
[15/Oct/2026 08:22:31] "GET /api/health HTTP/1.1" 200 12
[15/Oct/2026 08:22:31] "GET /api/health HTTP/1.1" 200 12
```

SHA-256 of the retained original output chunks before redaction: `f391b2803e9a4cfb98b40e66aeb75a48c256a178eabbdf6ce5b1d24637d5f14a`.

The workstation also had `legacy-peer-deps=true` in its npm configuration and a zero-byte global npm `lib/cli.js`. The initial frontend peer installation was repaired with a separately unpacked npm 10.9.3 and `--legacy-peer-deps=false`; this did not fix the global npm installation. Later trusted-toolchain/security remediation is recorded at its actual checkpoint below. Current runtime ports remain 55432/8001/3000; fresh Compose defaults are 5432/8000/3000.

## 2. Original initial test runs

These are the original pre-feature/pre-fix runs, not the later SQL regression or final 146-test suite. Backend errors were database setup errors; frontend failures included missing tooling/dependencies. No application or test source was changed to obtain the successful baseline runs.

### First backend attempt: 15 setup errors

Original command at 2026-10-15T08:15:17.681Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/backend`. Captures: 2026-10-15T08:16:04.418Z (source line 92); 2026-10-15T08:16:21.506Z (source line 101); 2026-10-15T08:16:31.499Z (source line 110).

```bash
../.venv/bin/python manage.py check; ../.venv/bin/python -m pytest -v
```

Exit 1. `manage.py check` passed, but PostgreSQL was not listening on the default localhost:5432. The capture itself was truncated by the original tool (75,322 original tokens / 6,158 lines); the excerpt preserves the real error and all 15 error-summary entries. A complete original traceback is not available.

```text
System check identified no issues (0 silenced).
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 15 items

projects/tests.py::TestProjects::test_create_project ERROR               [  6%]

[Retained diagnostic excerpt; original tool output was already truncated from 6,158 lines.]
E       psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
E       connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
E       django.db.utils.OperationalError: connection to server at "localhost" (::1), port 5432 failed: Connection refused
E       connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused


-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR projects/tests.py::TestProjects::test_create_project - django.db.utils....
ERROR projects/tests.py::TestProjects::test_list_only_returns_member_projects
ERROR projects/tests.py::TestProjects::test_get_project_detail - django.db.ut...
ERROR projects/tests.py::TestProjects::test_non_member_cannot_view_project - ...
ERROR projects/tests.py::TestTasks::test_create_task - django.db.utils.Operat...
ERROR projects/tests.py::TestTasks::test_viewers_cannot_create_tasks - django...
ERROR projects/tests.py::TestTasks::test_delete_task_requires_membership - dj...
ERROR users/tests.py::TestRegister::test_creates_user_and_returns_token - dja...
ERROR users/tests.py::TestRegister::test_rejects_short_password - django.db.u...
ERROR users/tests.py::TestRegister::test_rejects_duplicate_email - django.db....
ERROR users/tests.py::TestRegister::test_rejects_missing_name - django.db.uti...
ERROR users/tests.py::TestLogin::test_returns_token_on_valid_credentials - dj...
ERROR users/tests.py::TestLogin::test_rejects_wrong_password - django.db.util...
ERROR users/tests.py::TestLogin::test_rejects_missing_email - django.db.utils...
ERROR users/tests.py::TestLogin::test_rejects_unknown_email - django.db.utils...
======================== 1 warning, 15 errors in 27.16s ========================
```

SHA-256 of the retained original output chunks before redaction: `cbaa609fcabbdfa201234b3fb60d2b5239f4dcbc4a471d4a90b357d2b0158075`.

### First frontend command: test runner unavailable

Original command at 2026-10-15T08:16:13.293Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:16:31.499Z (source line 110).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
npm test
```

Exit 127 while dependencies were still being installed: `vitest` was not yet available.

```text
> taskboard-frontend@1.0.0 test
> vitest run

sh: vitest: command not found
```

SHA-256 of the retained original output chunks before redaction: `b39c181d460ff2f32fa0df5e7f5e4b3e7ef074ab6d28e5857329eb7e3e556f8d`.

### First completed frontend suite: six passes, one failed suite

Original command at 2026-10-15T08:18:07.833Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:18:30.805Z (source line 162); 2026-10-15T08:19:06.698Z (source line 175); 2026-10-15T08:20:09.813Z (source line 195).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
npm test
```

Exit 1. Six schema tests passed; the TaskCard suite could not load because @testing-library/dom was missing. This is one failed suite, not six failed tests.

```text
> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

 ✓ src/tests/schemas.test.ts (6 tests) 22ms
 ❯ src/tests/TaskCard.test.tsx (0 test)

⎯⎯⎯⎯⎯⎯ Failed Suites 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/tests/TaskCard.test.tsx [ src/tests/TaskCard.test.tsx ]
Error: Cannot find module '@testing-library/dom'
Require stack:
- /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/node_modules/@testing-library/react/dist/pure.js
 ❯ Object.<anonymous> node_modules/@testing-library/react/dist/pure.js:46:12

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯

 Test Files  1 failed | 1 passed (2)
      Tests  6 passed (6)
   Start at  13:48:21
   Duration  45.41s (transform 2.65s, setup 16.61s, collect 1.04s, tests 22ms, environment 44.11s, prepare 6.64s)
```

SHA-256 of the retained original output chunks before redaction: `6c83c8f5d7ebeb37a161ffe10d5b3f80eab3e2ae53e5f21f196e5e36330c2a40`.

### Frontend peer-dependency installation recovery

Original command at 2026-10-15T08:22:21.990Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:22:55.326Z (source line 255).

```bash
mkdir -p /tmp/taskboard-npm-10.9.3 && tar -xzf /tmp/taskboard-npm-10.9.3.tgz -C /tmp/taskboard-npm-10.9.3
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
node /tmp/taskboard-npm-10.9.3/package/bin/npm-cli.js install --no-package-lock --no-audit --no-fund --legacy-peer-deps=false
```

Exit 0. This repaired the installed dependency tree with legacy peer handling disabled; it did not edit application/test/seed source.

```text
added 13 packages, removed 1 package, and changed 1 package in 10s
```

SHA-256 of the retained original output chunks before redaction: `87d1e4640c16954ce7b69252115c2ba6a95ab3f8eae346d50dc50e3a85a7934c`.

### Recovered frontend baseline: 9 tests pass

Original command at 2026-10-15T08:23:09.991Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:23:42.343Z (source line 273); 2026-10-15T08:24:01.706Z (source line 288).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
node /tmp/taskboard-npm-10.9.3/package/bin/npm-cli.js test
```

Final exit 0, 2 test files / 9 tests passed. The original output also contains a global-npm subprocess TypeError; it is preserved below, not hidden or described as a clean toolchain. Later static incident analysis investigated the damaged global npm and malicious config.

```text
> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

 ✓ src/tests/schemas.test.ts (6 tests) 8ms
/Users/nitingupta/.nvm/versions/node/v22.20.0/lib/node_modules/npm/bin/npm-cli.js:2
require('../lib/cli.js')(process)
                        ^

TypeError: require(...) is not a function
    at Object.<anonymous> (/Users/nitingupta/.nvm/versions/node/v22.20.0/lib/node_modules/npm/bin/npm-cli.js:2:25)
    at Module._compile (node:internal/modules/cjs/loader:1706:14)
    at Object..js (node:internal/modules/cjs/loader:1839:10)
    at Module.load (node:internal/modules/cjs/loader:1441:32)
    at Function._load (node:internal/modules/cjs/loader:1263:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:237:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49

Node.js v22.20.0
 ✓ src/tests/TaskCard.test.tsx (3 tests) 864ms
   ✓ <TaskCard /> > renders the task title and assignee 334ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 518ms

 Test Files  2 passed (2)
      Tests  9 passed (9)
   Start at  13:53:15
   Duration  21.74s (transform 818ms, setup 2.16s, collect 4.27s, tests 872ms, environment 18.55s, prepare 4.29s)
```

SHA-256 of the retained original output chunks before redaction: `3358cdd51ec1ad976e9c0aea1248072a35eac36485b6ad255e574045a9e0c87e`.

### Recovered backend baseline: 15 tests pass

Original command at 2026-10-15T08:21:37.313Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/backend`. Captures: 2026-10-15T08:22:04.406Z (source line 238); 2026-10-15T08:22:34.503Z (source line 245); 2026-10-15T08:22:55.326Z (source line 255); 2026-10-15T08:23:42.343Z (source line 273); 2026-10-15T08:24:01.706Z (source line 288); 2026-10-15T08:24:17.087Z (source line 295).

```bash
docker exec taskboard-inspection-db-20261015 pg_isready -U taskboard -d taskboard_inspection; docker exec taskboard-inspection-db-20261015 postgres --version; POSTGRES_DB=taskboard_inspection POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python manage.py migrate --noinput && POSTGRES_DB=taskboard_inspection POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python -m pytest -v --tb=short
```

Final exit 0 against the isolated PostgreSQL instance. Poll chunks are joined in their original order; all 15 test results and the final summary are retained.

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 15 items

projects/tests.py::TestProjects::test_create_project PASSED              [  6%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 13%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 20%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 26%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 33%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 40%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 46%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 53%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 60%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 66%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 73%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 80%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 86%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 93%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [100%]

======================== 15 passed in 117.01s (0:01:57) ========================
```

SHA-256 of the retained original output chunks before redaction: `51f3617a976b80c8140037784c57b4e85e61a1b451ef53145ca12cc71a8820d7`.

### Original production-build attempt: type-check failure

Original command at 2026-10-15T08:18:07.833Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend`. Captures: 2026-10-15T08:18:30.805Z (source line 162); 2026-10-15T08:22:04.406Z (source line 238).

```bash
export PATH=/Users/nitingupta/.nvm/versions/node/v22.20.0/bin:$PATH
npm run build
```

Exit 2. This is the original build failure, not the current production-build result. Missing Jest/Node/DOM declarations and Symbol.asyncDispose types blocked TypeScript; subsequent build remediation and final passing build remain at their original later checkpoints.

```text
> taskboard-frontend@1.0.0 build
> tsc && vite build

node_modules/@testing-library/jest-dom/types/jest.d.ts(1,23): error TS2688: Cannot find type definition file for 'jest'.
node_modules/@testing-library/jest-dom/types/jest.d.ts(9,27): error TS2304: Cannot find name 'expect'.
node_modules/@testing-library/jest-dom/types/matchers.d.ts(1,29): error TS7016: Could not find a declaration file for module 'aria-query'. '/Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/node_modules/aria-query/lib/index.js' implicitly has an 'any' type.
  Try `npm i --save-dev @types/aria-query` if it exists or add a new declaration (.d.ts) file containing `declare module 'aria-query';`
node_modules/@testing-library/react/types/index.d.ts(9,8): error TS2307: Cannot find module '@testing-library/dom' or its corresponding type declarations.
node_modules/@testing-library/react/types/index.d.ts(14,15): error TS2307: Cannot find module '@testing-library/dom' or its corresponding type declarations.
node_modules/@vitest/utils/dist/index.d.ts(49,26): error TS2304: Cannot find name 'setImmediate'.
node_modules/@vitest/utils/dist/index.d.ts(50,28): error TS2304: Cannot find name 'clearImmediate'.
node_modules/rollup/dist/rollup.d.ts(1010,10): error TS2550: Property 'asyncDispose' does not exist on type 'SymbolConstructor'. Do you need to change your target library? Try changing the 'lib' compiler option to 'esnext' or later.
node_modules/vite/dist/node/index.d.ts(1,23): error TS2688: Cannot find type definition file for 'node'.
node_modules/vite/dist/node/index.d.ts(6,23): error TS2307: Cannot find module 'node:http' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(7,119): error TS2307: Cannot find module 'node:http' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(8,35): error TS2307: Cannot find module 'node:http2' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(9,21): error TS2307: Cannot find module 'node:fs' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(10,25): error TS2307: Cannot find module 'node:events' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(11,30): error TS2307: Cannot find module 'node:events' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(12,76): error TS2307: Cannot find module 'node:https' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(13,22): error TS2307: Cannot find module 'node:net' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(14,22): error TS2307: Cannot find module 'node:url' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(15,21): error TS2307: Cannot find module 'node:url' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(16,25): error TS2307: Cannot find module 'node:stream' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(17,39): error TS2307: Cannot find module 'node:stream' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(20,38): error TS2307: Cannot find module 'node:tls' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(21,29): error TS2307: Cannot find module 'node:zlib' or its corresponding type declarations.
node_modules/vite/dist/node/index.d.ts(309,35): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vite/dist/node/index.d.ts(391,11): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1014,40): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1084,55): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1102,39): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1119,55): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1137,39): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1154,55): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1172,39): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1189,38): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1201,56): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1210,38): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1222,59): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1237,18): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1237,41): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1242,24): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1242,47): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1247,39): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1247,48): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1278,25): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1309,24): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1309,33): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(1389,20): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(2401,63): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vite/dist/node/index.d.ts(3561,84): error TS2580: Cannot find name 'Buffer'. Do you need to install type definitions for node? Try `npm i --save-dev @types/node`.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(4,26): error TS2307: Cannot find module 'node:stream' or its corresponding type declarations.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(18,23): error TS2307: Cannot find module 'node:fs' or its corresponding type declarations.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(271,10): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(286,19): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(287,18): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(292,45): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(292,90): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(2082,19): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(2645,13): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(2646,14): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/reporters.nr4dxCkA.d.ts(2647,14): error TS2503: Cannot find namespace 'NodeJS'.
node_modules/vitest/dist/chunks/worker.B9FxPCaC.d.ts(1,29): error TS2307: Cannot find module 'node:worker_threads' or its corresponding type declarations.
src/tests/TaskCard.test.tsx(2,18): error TS2305: Module '"@testing-library/react"' has no exported member 'screen'.
src/tests/TaskCard.test.tsx(2,26): error TS2305: Module '"@testing-library/react"' has no exported member 'fireEvent'.
```

SHA-256 of the retained original output chunks before redaction: `bc9bd105c67c97cb88e2a4b619e09845e055fbd5bfc69361298db0c651821021`.

### Authorized original seed load after baseline tests

Original command at 2026-10-15T08:30:06.497Z; working directory `/Users/nitingupta/Desktop/taskboard/q-taskboard/backend`. Captures: 2026-10-15T08:30:24.761Z (source line 389).

```bash
POSTGRES_DB=taskboard_inspection POSTGRES_USER=taskboard POSTGRES_PASSWORD=<REDACTED> POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python manage.py seed
```

The user authorized bringing up seed data after the initial inspection. This historical command completed once at 08:30 UTC; it was not rerun during this recovery. The original fixture password is redacted. Existing seed data and audit comments remain untouched by the documentation correction.

```text
seeding...
seed complete.
login with any of these (password: <REDACTED>):
  meera@taskboard.dev   — admin on Q3 Launch, Internal Tools
  arjun@taskboard.dev   — admin on Onboarding, member on Q3 Launch
  kavya@example.com     — member on Q3 Launch
  dev@example.com       — viewer on Q3 Launch
  lina@example.com      — member on Onboarding
```

SHA-256 of the retained original output chunks before redaction: `1b4b500e0afd3b6cade4e3c7a8be2fe79c2b83ddc6d68360fb91189142bf5888`.

## 3. Original code-review bug proof

Historical reviewed commit: `5f58e52`. This section contains E01–E20 and B01–B04, with credentials redacted and wire-trace blocks omitted. Primary seeded records were read only; write probes used a separate disposable rollback database.

### Historical review capture header

Review target: commit `5f58e52`; 2026-10-15.

Primary running backend: `http://127.0.0.1:8001`, database `taskboard_inspection` on PostgreSQL port `55432`. The seeded database is read-only throughout this review. Write-based verification is isolated in a separate disposable database.

These are actual curl executions, not reconstructed responses. Bearer tokens below belong only to disposable local development accounts.

Initial canonical SHA256 of every row and column in users/projects/memberships/tasks: `8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe`. Initial row counts: users=5, projects=3, memberships=8, tasks=12.

### E01 — Seeded viewer login

UTC: 2026-10-15T08:38:44.079066+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E01.trace.txt --request POST http://127.0.0.1:8001/api/auth/login --header 'Content-Type: application/json' --data-raw '{"email":"dev@example.com","password":"<REDACTED_DEMO_PASSWORD>"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:46 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 388

{"user":{"id":"1764c87c-d25b-46bc-b641-8f93c4f0b55c","email":"dev@example.com","name":"Dev Sharma"},"token":"<REDACTED_JWT>"}
```

Response byte SHA256: `ee23cef0f736731857d4211951d5767f17b17e0f68dd039d63dffc110bf5f93b`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E02 — Confirm viewer identity

UTC: 2026-10-15T08:38:46.606105+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E02.trace.txt --request GET http://127.0.0.1:8001/api/users/me --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:46 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 100

{"user":{"id":"1764c87c-d25b-46bc-b641-8f93c4f0b55c","email":"dev@example.com","name":"Dev Sharma"}}
```

Response byte SHA256: `eda9dff276a09bf35873a6cba4c8be193250be96bdda692188f897559efbf97b`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E03 — Viewer can list only Q3 Launch

UTC: 2026-10-15T08:38:46.730700+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E03.trace.txt --request GET http://127.0.0.1:8001/api/projects --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:46 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 352

{"projects":[{"id":"be9a139e-e9ee-4528-a004-a5318841f256","name":"Q3 Launch","description":"Coordinate the Q3 product launch across engineering, design, and marketing.","role":"viewer","owner":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"taskCount":7,"createdAt":"2026-10-15T08:30:20.796874+00:00"}]}
```

Response byte SHA256: `78fed8257ab14efd54a783c4a91b7ad7f089b6c12906af137887013b8ba34691`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E04 — Normal task listing stays within Q3 Launch

UTC: 2026-10-15T08:38:46.898794+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E04.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 3539

{"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z","assignee":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"}},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z","assignee":null},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}]}
```

Response byte SHA256: `40f35bd500bc455d997f37039c96c1734d79bdc5fa02517a6eaa61b72672ec2d`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E05 — Direct access to Onboarding tasks is forbidden

UTC: 2026-10-15T08:38:47.136932+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E05.trace.txt --request GET http://127.0.0.1:8001/api/projects/eb475492-eb0b-4660-9d90-9f9d603ec069/tasks --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 08:38:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 21

{"error":"forbidden"}
```

Response byte SHA256: `7b11a575d66a1c0eb90fd67f0e08e34a864d6e1d6cdbba8bae73584a54ba58a7`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E06 — Harmless unmatched literal search returns no tasks

UTC: 2026-10-15T08:38:47.304729+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E06.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode q=review-no-match-20261015
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 12

{"tasks":[]}
```

Response byte SHA256: `30a3d98b5816874dec9a620fbc4a003ddb58b04304b5da9c9c92c52938a35ec6`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E07 — SQL injection crosses the project boundary (highest priority)

UTC: 2026-10-15T08:38:47.529225+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E07.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode 'q='"'"') OR TRUE -- '
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 5028

{"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z"},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z"},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z"},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z"},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z"},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z"},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z"},{"id":"62eac9cf-1160-40dd-bad7-680f9d5e7adb","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Map current onboarding funnel","description":"Detail for: Map current onboarding funnel","status":"done","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":0,"created_at":"2026-10-15T08:30:20.953870Z","updated_at":"2026-10-15T08:30:20.953890Z"},{"id":"9bee2f34-e921-4dee-b579-9be34aeb8b14","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Interview 5 recently-onboarded customers","description":"Detail for: Interview 5 recently-onboarded customers","status":"review","assignee_id":"8cca731b-9c2e-4a21-b93c-48033ac2e0b6","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":1,"created_at":"2026-10-15T08:30:20.959202Z","updated_at":"2026-10-15T08:30:20.959225Z"},{"id":"19ad52e0-9d81-4a9b-927b-06d69f740065","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Wireframe new welcome screens","description":"Detail for: Wireframe new welcome screens","status":"in_progress","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":2,"created_at":"2026-10-15T08:30:20.967076Z","updated_at":"2026-10-15T08:30:20.967104Z"},{"id":"ef7fca0b-4d52-47c8-ab38-bf1c5b3fa74a","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Audit current onboarding emails","description":"Detail for: Audit current onboarding emails","status":"todo","assignee_id":"8cca731b-9c2e-4a21-b93c-48033ac2e0b6","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":3,"created_at":"2026-10-15T08:30:21.090206Z","updated_at":"2026-10-15T08:30:21.090244Z"},{"id":"e84cd552-f56d-46c5-9b0e-e17532ffd41b","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Define success metric (TTFV target)","description":"Detail for: Define success metric (TTFV target)","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":4,"created_at":"2026-10-15T08:30:21.116882Z","updated_at":"2026-10-15T08:30:21.116936Z"}]}
```

Response byte SHA256: `3da1373eb12a37dc444030c6222b64596091be2d5c974abe01644e3018f682f2`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`

#### E07 derived evidence

The same viewer receives HTTP 403 for direct Onboarding task access (E05), but receives all 12 tasks through injected Q3 search (E07): 7 Q3 tasks and 5 Onboarding tasks. No INSERT, UPDATE, DELETE, or stacked SQL statement was used.

Leaked Onboarding tasks:

```json
[
  {
    "id": "62eac9cf-1160-40dd-bad7-680f9d5e7adb",
    "project_id": "eb475492-eb0b-4660-9d90-9f9d603ec069",
    "title": "Map current onboarding funnel",
    "description": "Detail for: Map current onboarding funnel",
    "status": "done",
    "assignee_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "created_by_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "position": 0,
    "created_at": "2026-10-15T08:30:20.953870Z",
    "updated_at": "2026-10-15T08:30:20.953890Z"
  },
  {
    "id": "9bee2f34-e921-4dee-b579-9be34aeb8b14",
    "project_id": "eb475492-eb0b-4660-9d90-9f9d603ec069",
    "title": "Interview 5 recently-onboarded customers",
    "description": "Detail for: Interview 5 recently-onboarded customers",
    "status": "review",
    "assignee_id": "8cca731b-9c2e-4a21-b93c-48033ac2e0b6",
    "created_by_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "position": 1,
    "created_at": "2026-10-15T08:30:20.959202Z",
    "updated_at": "2026-10-15T08:30:20.959225Z"
  },
  {
    "id": "19ad52e0-9d81-4a9b-927b-06d69f740065",
    "project_id": "eb475492-eb0b-4660-9d90-9f9d603ec069",
    "title": "Wireframe new welcome screens",
    "description": "Detail for: Wireframe new welcome screens",
    "status": "in_progress",
    "assignee_id": "89e883cc-17b4-46fd-9828-b10243d1c8e2",
    "created_by_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "position": 2,
    "created_at": "2026-10-15T08:30:20.967076Z",
    "updated_at": "2026-10-15T08:30:20.967104Z"
  },
  {
    "id": "ef7fca0b-4d52-47c8-ab38-bf1c5b3fa74a",
    "project_id": "eb475492-eb0b-4660-9d90-9f9d603ec069",
    "title": "Audit current onboarding emails",
    "description": "Detail for: Audit current onboarding emails",
    "status": "todo",
    "assignee_id": "8cca731b-9c2e-4a21-b93c-48033ac2e0b6",
    "created_by_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "position": 3,
    "created_at": "2026-10-15T08:30:21.090206Z",
    "updated_at": "2026-10-15T08:30:21.090244Z"
  },
  {
    "id": "e84cd552-f56d-46c5-9b0e-e17532ffd41b",
    "project_id": "eb475492-eb0b-4660-9d90-9f9d603ec069",
    "title": "Define success metric (TTFV target)",
    "description": "Detail for: Define success metric (TTFV target)",
    "status": "todo",
    "assignee_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "created_by_id": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b",
    "position": 4,
    "created_at": "2026-10-15T08:30:21.116882Z",
    "updated_at": "2026-10-15T08:30:21.116936Z"
  }
]
```


### E08 — Admin login for read-only export verification

UTC: 2026-10-15T08:38:47.690347+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E08.trace.txt --request POST http://127.0.0.1:8001/api/auth/login --header 'Content-Type: application/json' --data-raw '{"email":"meera@taskboard.dev","password":"<REDACTED_DEMO_PASSWORD>"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 392

{"user":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"token":"<REDACTED_JWT>"}
```

Response byte SHA256: `1dec04bf3c42e721a0fd69eb93db9fb022698a534735ce1708ad71fab6966284`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E09 — Export of seven existing tasks returns zero exported

UTC: 2026-10-15T08:38:49.633545+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E09.trace.txt --request POST http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/export --header 'Authorization: Bearer <REDACTED_JWT>' --header 'Content-Type: application/json' --data-raw '{}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:38:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 3552

{"exported":0,"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z","assignee":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"}},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z","assignee":null},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}]}
```

Response byte SHA256: `48359237e0cfb5b84458c7968b00f8b9d759995bcf44ad21d4884bc1602d43a1`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### B01 Assigned task on the seeded board

```bash
/Users/nitingupta/.codex/skills/gstack/browse/dist/browse --headed snapshot -i
```

```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256) ---
--- BEGIN UNTRUSTED EXTERNAL C​ONTENT (source: http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256) ---
  @e1 [link] "TaskBoard"
  @e2 [button] "sign out"
  @e3 [link] "← all projects"
  @e4 [textbox] "task title"
  @e5 [combobox]
    @e6 [option] "todo" [selected]
    @e7 [option] "in_progress"
    @e8 [option] "review"
    @e9 [option] "done"
  @e10 [button] "add"
  @e11 [button] "Prepare customer email blast Kavya Reddy"
  @e12 [button] "Update pricing page copy unassigned"
  @e13 [button] "QA the new signup flow end-to-end Arjun Rao"
  @e14 [button] "Record demo video Kavya Reddy"
  @e15 [button] "Set up analytics dashboards Arjun Rao"
  @e16 [button] "Draft press release Arjun Rao"
  @e17 [button] "Finalize launch date with marketing Meera Iyer"

── cursor-interactive (not in ARIA tree) ──
@c1 [cursor:pointer] "Prepare customer email blast"
@c2 [cursor:pointer] "Kavya Reddy"
@c3 [cursor:pointer] "Kavya Reddy"
@c4 [cursor:pointer] "Update pricing page copy"
@c5 [cursor:pointer] "unassigned"
@c6 [cursor:pointer] "unassigned"
@c7 [cursor:pointer] "QA the new signup flow end-to-end"
@c8 [cursor:pointer] "Arjun Rao"
@c9 [cursor:pointer] "Arjun Rao"
@c10 [cursor:pointer] "Record demo video"
@c11 [cursor:pointer] "Kavya Reddy"
@c12 [cursor:pointer] "Kavya Reddy"
@c13 [cursor:pointer] "Set up analytics dashboards"
@c14 [cursor:pointer] "Arjun Rao"
@c15 [cursor:pointer] "Arjun Rao"
@c16 [cursor:pointer] "Draft press release"
@c17 [cursor:pointer] "Arjun Rao"
@c18 [cursor:pointer] "Arjun Rao"
@c19 [cursor:pointer] "Finalize launch date with marketing"
@c20 [cursor:pointer] "Meera Iyer"
@c21 [cursor:pointer] "Meera Iyer"
--- END UNTRUSTED EXTERNAL C​ONTENT ---
--- END UNTRUSTED EXTERNAL CONTENT ---


```


### B02 Open assigned task without saving

```bash
/Users/nitingupta/.codex/skills/gstack/browse/dist/browse --headed click @e17
```

```text
Clicked @e17 → now at http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256


```


### B03 Existing assignee is incorrectly shown as unassigned

```bash
/Users/nitingupta/.codex/skills/gstack/browse/dist/browse --headed snapshot -i
```

```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256) ---
--- BEGIN UNTRUSTED EXTERNAL C​ONTENT (source: http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256) ---
  @e1 [link] "TaskBoard"
  @e2 [button] "sign out"
  @e3 [link] "← all projects"
  @e4 [textbox] "task title"
  @e5 [combobox]
    @e6 [option] "todo" [selected]
    @e7 [option] "in_progress"
    @e8 [option] "review"
    @e9 [option] "done"
  @e10 [button] "add"
  @e11 [button] "Prepare customer email blast Kavya Reddy"
  @e12 [button] "Update pricing page copy unassigned"
  @e13 [button] "QA the new signup flow end-to-end Arjun Rao"
  @e14 [button] "Record demo video Kavya Reddy"
  @e15 [button] "Set up analytics dashboards Arjun Rao"
  @e16 [button] "Draft press release Arjun Rao"
  @e17 [button] "Finalize launch date with marketing Meera Iyer"
@e18 [button] "✕"
@e19 [textbox] "title": Finalize launch date with marketing
@e20 [textbox] "description": "Detail for: Finalize launch date with marketing"
@e21 [combobox] "status"
  @e22 [option] "To do"
  @e23 [option] "In progress"
  @e24 [option] "In review"
  @e25 [option] "Done" [selected]
@e26 [combobox] "assignee"
  @e27 [option] "unassigned" [selected]
  @e28 [option] "Meera Iyer"
  @e29 [option] "Arjun Rao"
  @e30 [option] "Kavya Reddy"
  @e31 [option] "Dev Sharma"
@e32 [button] "delete task"
@e33 [button] "cancel"
@e34 [button] "save"

── cursor-interactive (not in ARIA tree) ──
@c1 [cursor:pointer] "Prepare customer email blast"
@c2 [cursor:pointer] "Kavya Reddy"
@c3 [cursor:pointer] "Kavya Reddy"
@c4 [cursor:pointer] "Update pricing page copy"
@c5 [cursor:pointer] "unassigned"
@c6 [cursor:pointer] "unassigned"
@c7 [cursor:pointer] "QA the new signup flow end-to-end"
@c8 [cursor:pointer] "Arjun Rao"
@c9 [cursor:pointer] "Arjun Rao"
@c10 [cursor:pointer] "Record demo video"
@c11 [cursor:pointer] "Kavya Reddy"
@c12 [cursor:pointer] "Kavya Reddy"
@c13 [cursor:pointer] "Set up analytics dashboards"
@c14 [cursor:pointer] "Arjun Rao"
@c15 [cursor:pointer] "Arjun Rao"
@c16 [cursor:pointer] "Draft press release"
@c17 [cursor:pointer] "Arjun Rao"
@c18 [cursor:pointer] "Arjun Rao"
@c19 [cursor:pointer] "Finalize launch date with marketing"
@c20 [cursor:pointer] "Meera Iyer"
@c21 [cursor:pointer] "Meera Iyer"
--- END UNTRUSTED EXTERNAL C​ONTENT ---
--- END UNTRUSTED EXTERNAL CONTENT ---


```


### B04 — Close the seeded task without saving

```bash
/Users/nitingupta/.codex/skills/gstack/browse/dist/browse --headed click @e33
```

```text
Clicked @e33 → now at http://127.0.0.1:3000/projects/be9a139e-e9ee-4528-a004-a5318841f256


```

No save or delete button was clicked on the seeded application.

### Disposable write-verification environment

E10–E20 use `http://127.0.0.1:8002` and database `taskboard_review_probe_20261015`. This database was created empty, migrated using the existing migrations, and populated with three review-only users, one project, two memberships, and one task. No seed command or seed rows were used. The main server at port 8001 was not reconfigured.

The same unmodified Django views run behind this temporary WSGI boundary:

```python
class RollbackHandler(WSGIHandler):
    def get_response(self, request):
        with transaction.atomic():
            response = super().get_response(request)
            transaction.set_rollback(True)
            return response
```

The boundary only prevents commits; it does not replace authentication, membership checks, task.save(), serializers, or response codes. HTTP 200 responses below contain the real database state seen by the view before rollback. Post-request SELECTs and full-row comparison verify rollback.

Fixture identifiers:

```json
{
  "database": "taskboard_review_probe_20261015",
  "base": "http://127.0.0.1:8002",
  "project_id": "7eddde71-3491-4f9a-ab97-2dfbf1e91e71",
  "task_id": "9d42df81-4f7c-4c3e-9239-786b80449d80",
  "admin_id": "7731890c-56af-4fc4-8954-a0244a69a887",
  "viewer_id": "89ad57d3-b3b9-44af-baac-d0be4877dda3",
  "outsider_id": "a06b7a66-d69e-438b-8355-59bda867a049",
  "title": "Disposable authorization probe",
  "description": "Review-only fixture; not seed data.",
  "status": "todo",
  "assignee_id": "7731890c-56af-4fc4-8954-a0244a69a887"
}
```


### E10 — Disposable non-member login

UTC: 2026-10-15T08:41:51.927864+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E10.trace.txt --request POST http://127.0.0.1:8002/api/auth/login --header 'Content-Type: application/json' --data-raw '{"email":"review-outsider@example.test","password":"<REDACTED_DEMO_PASSWORD>"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:41:55 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 406

{"user":{"id":"a06b7a66-d69e-438b-8355-59bda867a049","email":"review-outsider@example.test","name":"Review Outsider"},"token":"<REDACTED_JWT>"}
```

Response byte SHA256: `f114fb577977bee133e4e50216219ce1dee91063ed1aec9f4bc71f642db37635`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E11 — Non-member cannot read the target project

UTC: 2026-10-15T08:41:55.222778+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E11.trace.txt --request GET http://127.0.0.1:8002/api/projects/7eddde71-3491-4f9a-ab97-2dfbf1e91e71 --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 403 Forbidden
Date: Thu, 15 Oct 2026 08:41:55 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 21

{"error":"forbidden"}
```

Response byte SHA256: `594d8cfd99cc69cdbadf2f9828d2bdb2c5b35515ad4f4607154f3103e262a887`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E12 — The same non-member can update its task

UTC: 2026-10-15T08:41:55.394016+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E12.trace.txt --request PATCH http://127.0.0.1:8002/api/tasks/9d42df81-4f7c-4c3e-9239-786b80449d80 --header 'Authorization: Bearer <REDACTED_JWT>' --header 'Content-Type: application/json' --data-raw '{"status":"done"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:41:55 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 537

{"task":{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"done","assignee_id":"7731890c-56af-4fc4-8954-a0244a69a887","created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:41:55.565635Z","assignee":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}}}
```

Response byte SHA256: `846e65b2b637e815b7c0d59e1e7956646a07d6a74629317471299b394bc9d698`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E13 — Disposable viewer login

UTC: 2026-10-15T08:41:55.658185+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E13.trace.txt --request POST http://127.0.0.1:8002/api/auth/login --header 'Content-Type: application/json' --data-raw '{"email":"review-viewer@example.test","password":"<REDACTED_DEMO_PASSWORD>"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:41:58 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 402

{"user":{"id":"89ad57d3-b3b9-44af-baac-d0be4877dda3","email":"review-viewer@example.test","name":"Review Viewer"},"token":"<REDACTED_JWT>"}
```

Response byte SHA256: `43a84a6dfd3031c1c0afdc7862e97a092f28eeb35cca6210f0088359b72d1033`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E14 — Verify viewer role on the target project

UTC: 2026-10-15T08:41:58.327588+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E14.trace.txt --request GET http://127.0.0.1:8002/api/projects/7eddde71-3491-4f9a-ab97-2dfbf1e91e71 --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:41:58 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 1294

{"project":{"id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","name":"Disposable review project","description":"Review-only fixture; not seed data.","owner_id":"7731890c-56af-4fc4-8954-a0244a69a887","owner":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"},"memberships":[{"id":"713ab866-5056-48b7-97e7-1f98398181c8","role":"admin","user":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}},{"id":"c38c4c5e-20d8-4a81-9cf2-ad3cdbe643f6","role":"viewer","user":{"id":"89ad57d3-b3b9-44af-baac-d0be4877dda3","email":"review-viewer@example.test","name":"Review Viewer"}}],"tasks":[{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"todo","assignee_id":"7731890c-56af-4fc4-8954-a0244a69a887","created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:40:00.154518Z","assignee":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}}],"created_at":"2026-10-15T08:40:00.111808Z","updated_at":"2026-10-15T08:40:00.111835Z"}}
```

Response byte SHA256: `540cbadcce8c5a4f0943f09219a4ad59bde2ca69f7d55723ae9d791aa24ff5ba`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E15 — Viewer task update also succeeds

UTC: 2026-10-15T08:41:58.615668+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E15.trace.txt --request PATCH http://127.0.0.1:8002/api/tasks/9d42df81-4f7c-4c3e-9239-786b80449d80 --header 'Authorization: Bearer <REDACTED_JWT>' --header 'Content-Type: application/json' --data-raw '{"status":"done"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:41:58 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 537

{"task":{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"done","assignee_id":"7731890c-56af-4fc4-8954-a0244a69a887","created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:41:58.747564Z","assignee":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}}}
```

Response byte SHA256: `bcb9295ee73add2bf1ef08dade89eea099cbdbdc6f37f52b1eeb7ba45140c9ff`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E16 — Viewer task deletion is correctly forbidden

UTC: 2026-10-15T08:41:58.853649+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E16.trace.txt --request DELETE http://127.0.0.1:8002/api/tasks/9d42df81-4f7c-4c3e-9239-786b80449d80 --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 403 Forbidden
Date: Thu, 15 Oct 2026 08:41:59 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 39

{"error":"viewers cannot delete tasks"}
```

Response byte SHA256: `71b014e8c8396c99ce8ec82aa7751d586bedde2f6066136b12b67b9b1e8c8c12`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E17 — Disposable admin login

UTC: 2026-10-15T08:41:59.043552+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E17.trace.txt --request POST http://127.0.0.1:8002/api/auth/login --header 'Content-Type: application/json' --data-raw '{"email":"review-admin@example.test","password":"<REDACTED_DEMO_PASSWORD>"}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:42:01 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 400

{"user":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"},"token":"<REDACTED_JWT>"}
```

Response byte SHA256: `cfce6a0808614e4648a9e2373577109d89958e2c0d120f37dde577a45e5fdcb3`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E18 — Task remains todo and assigned after rolled-back unauthorized requests

UTC: 2026-10-15T08:42:01.631108+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E18.trace.txt --request GET http://127.0.0.1:8002/api/projects/7eddde71-3491-4f9a-ab97-2dfbf1e91e71/tasks --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:42:01 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 540

{"tasks":[{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"todo","assignee_id":"7731890c-56af-4fc4-8954-a0244a69a887","created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:40:00.154518Z","assignee":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}}]}
```

Response byte SHA256: `5fa2045a9c108602cc63e30ccd46cd60118f43081bbf93ab2ae06d80992797c3`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E19 — Unchanged edit-form payload clears an existing assignee

UTC: 2026-10-15T08:42:01.865901+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E19.trace.txt --request PATCH http://127.0.0.1:8002/api/tasks/9d42df81-4f7c-4c3e-9239-786b80449d80 --header 'Authorization: Bearer <REDACTED_JWT>' --header 'Content-Type: application/json' --data-raw '{"title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"todo","assigneeId":null}'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:42:02 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 404

{"task":{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"todo","assignee_id":null,"created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:42:02.048065Z","assignee":null}}
```

Response byte SHA256: `adf7614f7cc6a8464436fee68889deddbe4b7a60545c9b8dcb6bf535d35fcc4a`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


### E20 — Post-rollback read confirms original task and assignment are intact

UTC: 2026-10-15T08:42:02.173247+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E20.trace.txt --request GET http://127.0.0.1:8002/api/projects/7eddde71-3491-4f9a-ab97-2dfbf1e91e71/tasks --header 'Authorization: Bearer <REDACTED_JWT>'
```

Exact HTTP response (`curl --include`, headers and body):

```http
HTTP/1.0 200 OK
Date: Thu, 15 Oct 2026 08:42:02 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 540

{"tasks":[{"id":"9d42df81-4f7c-4c3e-9239-786b80449d80","project_id":"7eddde71-3491-4f9a-ab97-2dfbf1e91e71","title":"Disposable authorization probe","description":"Review-only fixture; not seed data.","status":"todo","assignee_id":"7731890c-56af-4fc4-8954-a0244a69a887","created_by_id":"7731890c-56af-4fc4-8954-a0244a69a887","position":0,"created_at":"2026-10-15T08:40:00.154414Z","updated_at":"2026-10-15T08:40:00.154518Z","assignee":{"id":"7731890c-56af-4fc4-8954-a0244a69a887","email":"review-admin@example.test","name":"Review Admin"}}]}
```

Response byte SHA256: `94b0b25fe33a63a5a6133d6f1c1d1e29b50e123a432a241d625e5885deb4c4eb`

curl wire trace (includes the actual URL-encoded request and headers):

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`


#### Disposable write-probe verification

E11=403 but E12=200 with status=done for the same non-member. E14 proves viewer membership; E15=200 with status=done, while E16 DELETE=403. E18/E20 read status=todo and the original admin assignee after rollback. E19 proves the editor-generated null assignee is accepted and returned as null.

Every field of the disposable task, including updated_at, is identical before and after. Canonical task-row SHA256: `5b388695a9e1a325155951b9ce0bd877b3c0ff2cc34fe806ef69c1a5bd4f3049`.

### Final seed-data integrity check

A separate read-only PostgreSQL connection selected every column of every row from users, projects, memberships, and tasks, ordered by UUID. Each row was serialized with row_to_json, and the full snapshot was canonicalized with sorted JSON keys. The complete before/after snapshots match, including passwords, assignments, status, created_at, and updated_at.

```json
{
  "unchanged": true,
  "sha256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "counts": {
    "users": 5,
    "projects": 3,
    "memberships": 8,
    "tasks": 12
  }
}
```

No application or test source was edited. No seed command ran during this review.

### Temporary probe cleanup

Stopped PID 45875 after verifying its command was the review-owned `/tmp/taskboard-focused-review/serve_existing_probe.py`. Dropped only the review-created database `taskboard_review_probe_20261015`. Database catalog verification confirms the original `taskboard_inspection` remains and the disposable database is gone.

```json
{
  "remaining_taskboard_databases": [
    "taskboard_inspection"
  ],
  "probe_listener_stopped": true
}
```

### Final repository and service check

```text
?? REVIEW.md
?? TERMINAL_log.md
HEAD: 5f58e52
Main frontend API proxy: HTTP 200, {"ok": true}
All seed rows still match the pre-review snapshot after temporary database cleanup.
```

## 4. SQL injection fix: exact before/after proof

The private original request files are byte-identical; the same exploit returned 12 tasks before and zero after. This audit compared those actual files without printing their authorization values.


```json
{
  "sameExactExecutedRequestBytes": true,
  "before": {
    "phase": "before",
    "http_status": 200,
    "task_count": 12,
    "request_sha256": "a04ae70184f3c389a0cd332a6f18a0c060282e0e787fb185e8040ceba864fcd7"
  },
  "after": {
    "phase": "after",
    "http_status": 200,
    "task_count": 0,
    "request_sha256": "a04ae70184f3c389a0cd332a6f18a0c060282e0e787fb185e8040ceba864fcd7"
  }
}
```

### SQL injection fix: before and after evidence

The original E01-E20 and B01-B04 evidence above is preserved verbatim. F01/F02 execute the exact E07 command again, including the same URL, query payload, viewer JWT, headers, curl options, and trace destination. The original trace is backed up before replay.

#### F01 — Before fix: exact E07 replay

UTC: 2026-10-15T08:54:20.451722+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E07.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode 'q='"'"') OR TRUE -- '
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:54:20 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 5028

{"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z"},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z"},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z"},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z"},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z"},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z"},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z"},{"id":"62eac9cf-1160-40dd-bad7-680f9d5e7adb","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Map current onboarding funnel","description":"Detail for: Map current onboarding funnel","status":"done","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":0,"created_at":"2026-10-15T08:30:20.953870Z","updated_at":"2026-10-15T08:30:20.953890Z"},{"id":"9bee2f34-e921-4dee-b579-9be34aeb8b14","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Interview 5 recently-onboarded customers","description":"Detail for: Interview 5 recently-onboarded customers","status":"review","assignee_id":"8cca731b-9c2e-4a21-b93c-48033ac2e0b6","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":1,"created_at":"2026-10-15T08:30:20.959202Z","updated_at":"2026-10-15T08:30:20.959225Z"},{"id":"19ad52e0-9d81-4a9b-927b-06d69f740065","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Wireframe new welcome screens","description":"Detail for: Wireframe new welcome screens","status":"in_progress","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":2,"created_at":"2026-10-15T08:30:20.967076Z","updated_at":"2026-10-15T08:30:20.967104Z"},{"id":"ef7fca0b-4d52-47c8-ab38-bf1c5b3fa74a","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Audit current onboarding emails","description":"Detail for: Audit current onboarding emails","status":"todo","assignee_id":"8cca731b-9c2e-4a21-b93c-48033ac2e0b6","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":3,"created_at":"2026-10-15T08:30:21.090206Z","updated_at":"2026-10-15T08:30:21.090244Z"},{"id":"e84cd552-f56d-46c5-9b0e-e17532ffd41b","project_id":"eb475492-eb0b-4660-9d90-9f9d603ec069","title":"Define success metric (TTFV target)","description":"Detail for: Define success metric (TTFV target)","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","position":4,"created_at":"2026-10-15T08:30:21.116882Z","updated_at":"2026-10-15T08:30:21.116936Z"}]}
```

Response byte SHA256: `6168ed681991414aa5406c96327a6bb344db1c87542b87bb796b5cf0c55c79a1`

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`

#### F02 — After fix: exact E07 replay

UTC: 2026-10-15T08:56:42.953817+00:00

Exact executed command:

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-focused-review/E07.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode 'q='"'"') OR TRUE -- '
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:56:42 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 12

{"tasks":[]}
```

Response byte SHA256: `5739090265dfd9d45545f79fc3247949457e4627a575a6b78c5ccd4194142f4d`

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

curl exit code: `0`

#### F03 — Case-insensitive normal title search

UTC: 2026-10-15T08:57:45.094854+00:00

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-sql-fix/F03.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode q=AnALYTICS
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:57:45 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 433

{"tasks":[{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z"}]}
```

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

#### F04 — Existing wildcard behavior stays within Q3 Launch

UTC: 2026-10-15T08:57:45.304863+00:00

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-sql-fix/F04.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode q=%
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:57:45 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 2886

{"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z"},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z"},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z"},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z"},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z"},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z"},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z"}]}
```

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

#### F05 — Forbidden project search remains forbidden

UTC: 2026-10-15T08:57:45.512796+00:00

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-sql-fix/F05.trace.txt --request GET http://127.0.0.1:8001/api/projects/eb475492-eb0b-4660-9d90-9f9d603ec069/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode q=analytics
```

Exact HTTP response:

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 08:57:45 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 21

{"error":"forbidden"}
```

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

#### F06 — Empty query preserves the existing non-search response

UTC: 2026-10-15T08:57:45.793113+00:00

```bash
curl --http1.1 --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 25 --include --trace-ascii /tmp/taskboard-sql-fix/F06.trace.txt --request GET http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/tasks --header 'Authorization: Bearer <REDACTED_JWT>' --get --data-urlencode q=
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 08:57:45 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 3539

{"tasks":[{"id":"a6cbffcf-867c-470f-8007-a9ac3dea054f","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Finalize launch date with marketing","description":"Detail for: Finalize launch date with marketing","status":"done","assignee_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T08:30:20.894987Z","updated_at":"2026-10-15T08:30:20.895008Z","assignee":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"}},{"id":"b0fed58a-6b26-4d35-a75f-3437ce097b3b","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Record demo video","description":"Detail for: Record demo video","status":"in_progress","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":2,"created_at":"2026-10-15T08:30:20.911003Z","updated_at":"2026-10-15T08:30:20.911024Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"205e7059-6f6f-45a8-96c6-b68067a8aafc","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Set up analytics dashboards","description":"Detail for: Set up analytics dashboards","status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":3,"created_at":"2026-10-15T08:30:20.933342Z","updated_at":"2026-10-15T08:30:20.933363Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"6da053ca-e93e-4fac-8a70-e8cb134b8a6c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Draft press release","description":"Detail for: Draft press release","status":"review","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":1,"created_at":"2026-10-15T08:30:20.903101Z","updated_at":"2026-10-15T08:30:20.903126Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}},{"id":"d288f861-3f4b-4cb0-9330-da5efbce8637","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Prepare customer email blast","description":"Detail for: Prepare customer email blast","status":"todo","assignee_id":"269542ef-8686-4bce-94f1-71ffda227a62","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":4,"created_at":"2026-10-15T08:30:20.938438Z","updated_at":"2026-10-15T08:30:20.938459Z","assignee":{"id":"269542ef-8686-4bce-94f1-71ffda227a62","email":"kavya@example.com","name":"Kavya Reddy"}},{"id":"4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"Update pricing page copy","description":"Detail for: Update pricing page copy","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":5,"created_at":"2026-10-15T08:30:20.942737Z","updated_at":"2026-10-15T08:30:20.942759Z","assignee":null},{"id":"5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c","project_id":"be9a139e-e9ee-4528-a004-a5318841f256","title":"QA the new signup flow end-to-end","description":"Detail for: QA the new signup flow end-to-end","status":"todo","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":6,"created_at":"2026-10-15T08:30:20.950029Z","updated_at":"2026-10-15T08:30:20.950057Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}]}
```

Exact curl wire trace:

```text
[Raw wire trace omitted: it contains wrapped credential fragments. The separately captured request and HTTP response are retained with redactions.]
```

#### SQL fix verification summary

Only task-search SQL construction changed: the project UUID and both ILIKE patterns are bound parameters. Existing search response fields, ascending position order, case-insensitive title/description matching, `%`/`_` wildcard behavior, and the empty-query path are preserved. The other review findings were outside this fix.

| Evidence | Request | HTTP | Result |
|---|---|---|---|
| F01 before | Exact E07 injection command | 200 | 12 tasks, including five forbidden Onboarding tasks |
| F02 after | Exact same command, JWT, query, URL, and request trace | 200 | `{"tasks":[]}`; no forbidden tasks |
| F03 | Case-insensitive normal search | 200 | One matching Q3 task |
| F04 | Existing `%` wildcard search | 200 | Seven Q3 tasks only; fields/order equal the original search response restricted to Q3 |
| F05 | Search directly in forbidden Onboarding project | 403 | `{"error":"forbidden"}` |
| F06 | Empty query | 200 | Original seven-task non-search response preserved exactly |

The before/after request-trace SHA256 is `a04ae70184f3c389a0cd332a6f18a0c060282e0e787fb185e8040ceba864fcd7`. The initial terminal-log content is preserved byte-for-byte as a prefix, including the original E07 response. The restarted seeded application uses the fixed query on backend port 8001; frontend port 3000 still proxies to it.

Applied application diff:

```diff
diff --git a/backend/projects/views.py b/backend/projects/views.py
index 2aac320..538e051 100644
--- a/backend/projects/views.py
+++ b/backend/projects/views.py
@@ -111,13 +111,14 @@ class TaskListCreateView(APIView):
         if q:
             with connection.cursor() as cursor:
                 sql = (
-                    f"SELECT id, project_id, title, description, status, assignee_id, created_by_id, position, created_at, updated_at "
-                    f"FROM tasks "
-                    f"WHERE project_id = '{project_id}' "
-                    f"AND (title ILIKE '%{q}%' OR description ILIKE '%{q}%') "
-                    f"ORDER BY position ASC"
+                    "SELECT id, project_id, title, description, status, assignee_id, created_by_id, position, created_at, updated_at "
+                    "FROM tasks "
+                    "WHERE project_id = %s "
+                    "AND (title ILIKE %s OR description ILIKE %s) "
+                    "ORDER BY position ASC"
                 )
-                cursor.execute(sql)
+                pattern = f'%{q}%'
+                cursor.execute(sql, [str(project_id), pattern, pattern])
                 columns = [col[0] for col in cursor.description]
                 rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
             return Response({'tasks': rows})

```

#### Backend test evidence

All tests use Django/pytest-django's separate test database. No seed command ran. Added 14 API regression cases: the exact injection, literal SQL-shaped search text, cross-project isolation, normal title/description searches, case insensitivity, apostrophes, no matches, ordering across statuses, existing wildcards, response fields, empty query, non-member denial, and authentication.

**Red: injection reproduced before the application change**

Working directory: `backend`. Command (output also saved with `tee`):

```bash
POSTGRES_DB=taskboard_inspection POSTGRES_USER=taskboard POSTGRES_PASSWORD=<REDACTED_CREDENTIAL> POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python -m pytest projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks -v --tb=short --junitxml=/tmp/taskboard-sql-fix/red.xml
```

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 1 item

projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks FAILED [100%]

=================================== FAILURES ===================================
____ TestTaskSearch.test_sql_injection_does_not_return_other_projects_tasks ____
projects/tests.py:122: in test_sql_injection_does_not_return_other_projects_tasks
    assert response.json()['tasks'] == []
E   AssertionError: assert [{'assignee_i...': None, ...}] == []
E
E     Left contains 2 more items, first extra item: {'assignee_id': None, 'created_at': '2026-10-15T08:54:30.316000Z', 'created_by_id': 'aaea4cf2-eae2-43e0-b478-e95c3cc2167f', 'description': None, ...}
E
E     Full diff:
E     - []
E     + [
E     +     {...
E
E     ...Full output truncated (24 lines hidden), use '-vv' to show
---------------------------- Captured stderr setup -----------------------------
Creating test database for alias 'default'...
--------------------------- Captured stderr teardown ---------------------------
Destroying test database for alias 'default'...
-------------- generated xml file: /tmp/taskboard-sql-fix/red.xml --------------
=========================== short test summary info ============================
FAILED projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks
============================== 1 failed in 8.11s ===============================

```

**Green: targeted regression after parameter binding**

Working directory: `backend`. Command (output also saved with `tee`):

```bash
POSTGRES_DB=taskboard_inspection POSTGRES_USER=taskboard POSTGRES_PASSWORD=<REDACTED_CREDENTIAL> POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python -m pytest projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks -v --tb=short --junitxml=/tmp/taskboard-sql-fix/green.xml
```

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 1 item

projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [100%]

------------- generated xml file: /tmp/taskboard-sql-fix/green.xml -------------
============================== 1 passed in 14.93s ==============================

```

**Complete existing backend suite plus regression tests**

Working directory: `backend`. Command (output also saved with `tee`):

```bash
POSTGRES_DB=taskboard_inspection POSTGRES_USER=taskboard POSTGRES_PASSWORD=<REDACTED_CREDENTIAL> POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=55432 ../.venv/bin/python -m pytest -v --tb=short --junitxml=/tmp/taskboard-sql-fix/backend.xml
```

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 29 items

projects/tests.py::TestProjects::test_create_project PASSED              [  3%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [  6%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 10%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 13%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 17%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 20%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 24%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 27%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 31%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 34%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 37%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 41%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 44%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 48%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 51%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 55%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 58%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 62%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 65%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 68%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 72%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 75%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 79%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 82%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 86%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 89%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 93%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 96%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [100%]

------------ generated xml file: /tmp/taskboard-sql-fix/backend.xml ------------
======================== 29 passed in 249.21s (0:04:09) ========================

```

JUnit-confirmed final backend results:

```json
{
  "tests": 29,
  "errors": 0,
  "failures": 0,
  "skipped": 0
}
```

#### Seed preservation after the fix

Every column of every row in the seeded users/projects/memberships/tasks tables matches the pre-fix snapshot, including timestamps, assignments, and password hashes.

```json
{
  "unchanged": true,
  "sha256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "counts": {
    "users": 5,
    "projects": 3,
    "memberships": 8,
    "tasks": 12
  }
}
```

The original REVIEW.md is unchanged. The fix commit stages only backend/projects/views.py and backend/projects/tests.py; review and terminal artifacts remain local and uncommitted.

#### Separate SQL fix commit

```text
70f2bd96b9aa4342ee120beab9db5a961d27497d
fix: parameterize task search to prevent SQL injection

Committed files:
backend/projects/views.py
backend/projects/tests.py

Final git status:
## master...origin/master [ahead 1]
?? REVIEW.md
?? TERMINAL_log.md
```

The fix and its regression tests are committed locally. REVIEW.md and TERMINAL_log.md remain uncommitted review artifacts; no push was performed.

## 5. Part 3c real Airtable exports and intervening security checkpoint

Historical export evidence below records actual API calls. Independently comparing the original remote snapshots during this audit confirms the same seven Task IDs and Airtable record IDs after the second run, exactly one remote row per exported task, matching fields, and unchanged unrelated rows. This is verification of saved real evidence, not a new current-base query or export.


```json
{
  "evidenceType": "Previously captured real API HTTP responses and remote record snapshots; no new export or remote request during this audit",
  "first": {
    "total": 7,
    "created": 7,
    "updated": 0,
    "failed": 0,
    "failures": []
  },
  "second": {
    "total": 7,
    "created": 0,
    "updated": 7,
    "failed": 0,
    "failures": []
  },
  "remoteRowCounts": [
    3,
    10,
    10
  ],
  "expectedProjectTasks": 7,
  "firstExportTaskIdsMatch": true,
  "secondExportTaskIdsMatch": true,
  "sameAirtableRecordIds": true,
  "noDuplicateStableTaskIds": true,
  "allExportedFieldsMatchSeed": true,
  "unrelatedRecordsUnchanged": true,
  "airtableScreenshotOrShareLinkPresent": false
}
```

**Historical visual-evidence gap, subsequently resolved:** no Airtable screenshot or share link had been supplied at this export checkpoint. The actual [shared Tasks view](https://airtable.com/appC1ADL6s1JlxKAP/shrz8aTLD3nTVjoVk) was provided and opened without login during the later documentation correction; see the final verification checkpoint below. Its seven original exported task IDs were confirmed visible. The following sentences describe the earlier checkpoint: API evidence proves remote writes/idempotency but does not prove the base UI was opened. README contains an explicit placeholder. The supplied original assignment requires the official npm SDK, which this implementation uses. Earlier legacy-brief wording was incorrect and is superseded by the source correction at the end of this log.

### Airtable configuration checkpoint: paused before real API testing

Created an owner-only root .env with blank credential placeholders. Kept the local .env.example template and removed it from the Git index so both environment files are ignored. Added python-dotenv server-side loading with environment precedence; Docker forwards the three AIRTABLE variables only to the backend. Django system check and isolated configuration-loading checks pass. No secret values are captured here. No Airtable connection or export has been attempted. Waiting for user configuration before continuing the integration and real-base verification.

```json
{
  "root_env_ignored": true,
  "example_ignored_and_kept_locally": true,
  "django_system_check": "passed",
  "server_env_loading": "passed",
  "environment_precedence": "passed",
  "frontend_airtable_variables": false,
  "airtable_api_calls": 0,
  "live_exports": 0,
  "seed_unchanged": true,
  "seed_sha256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "commit_created": false
}
```


### Airtable integration verification — 2026-10-15T09:44:38.624226+00:00
The user authorized real-base verification after configuring the ignored root .env, approved adding a Long text “Task Description” field while preserving the AI Description field, and granted schema.bases:write after an initial 403. The subsequent official-SDK schema creation succeeded. Exports do not modify the schema.

Credentials are read by Django from the root .env or backend environment, then passed through the server-side child environment to the official airtable npm package (0.12.2). Neither tokens nor base identifiers are included below. Both .env and .env.example are ignored and untracked; .env is mode 0600. The local .env.example contains placeholders. No seed command ran during implementation.

#### Authorized schema setup and connection
```json
{"created":true,"fieldType":"multilineText","existingAIFieldPreserved":true}
```
```json
{
  "connected": true,
  "taskDescriptionLongText": true,
  "aiDescriptionPreserved": true
}
```
#### Two real exports through the running Django endpoint

Actual execution used `curl --config -`, supplying the configuration on stdin so the local JWT never appeared in process arguments. The exact export configuration is reproduced below with only that JWT redacted. No task data was supplied by the client.

Export 1:

```sh
curl --config - <<'CURL'
url = "http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/export"
request = "POST"
silent
show-error
include
max-time = 155
header = "Content-Type: application/json"
header = "Authorization: Bearer <REDACTED_LOCAL_JWT>"
CURL
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 09:35:02 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 60

{"total":7,"created":7,"updated":0,"failed":0,"failures":[]}
```

Export 2:

```sh
curl --config - <<'CURL'
url = "http://127.0.0.1:8001/api/projects/be9a139e-e9ee-4528-a004-a5318841f256/export"
request = "POST"
silent
show-error
include
max-time = 155
header = "Content-Type: application/json"
header = "Authorization: Bearer <REDACTED_LOCAL_JWT>"
CURL
```

Exact HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 09:35:09 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 60

{"total":7,"created":0,"updated":7,"failed":0,"failures":[]}
```

Remote verification used the official npm SDK to read every page after each export. Each of the seven source UUIDs has exactly one remote row; Airtable record IDs are identical across the two exports. All seven mapped fields match PostgreSQL, and the three pre-existing unrelated records remain unchanged.

```json
{
  "projectTasks": 7,
  "first": {
    "total": 7,
    "created": 7,
    "updated": 0,
    "failed": 0,
    "failures": []
  },
  "second": {
    "total": 7,
    "created": 0,
    "updated": 7,
    "failed": 0,
    "failures": []
  },
  "remoteRowsBefore": 3,
  "remoteRowsAfterFirst": 10,
  "remoteRowsAfterSecond": 10,
  "uniqueTaskIDs": 7,
  "sameRecordIDsAcrossExports": true,
  "allExportedFieldsMatchDatabase": true,
  "unrelatedRemoteRecordsUnchanged": true,
  "aiDescriptionFieldPreserved": true
}
```

Stable Task ID → remote record ID fingerprints (SHA-256; record identifiers withheld):

```text
4a99cf9a-0c9b-4550-bc73-04ee8fe1e29e  f44d5899ad77f1dcfff2bc6be12aaae2b16298cb59fbfe9c2afe58dcb73ddf05
a6cbffcf-867c-470f-8007-a9ac3dea054f  a9c59e99b441bc2dff86e4be853d29bd62695a8df4aa011392199b3c8afcb692
6da053ca-e93e-4fac-8a70-e8cb134b8a6c  a590606b715ba3ca1f59737dc862a15681d2622905b5e2c0c3fead3c69f68c1b
205e7059-6f6f-45a8-96c6-b68067a8aafc  959c2d6c947c5ae19b440a1d817ea1431e1029f7795f170136c6280aca218eab
b0fed58a-6b26-4d35-a75f-3437ce097b3b  9ffd70eeccb507acd0ed0b6b0229cb2352298905079e550ce282d9517643d68a
d288f861-3f4b-4cb0-9330-da5efbce8637  3c0ffc366dcaba154e6316c01a8cadf79471205b81959e5c20e242f30adf2051
5cdf7cc7-97bf-4a4b-9ba2-0a143436d14c  be54e596a5838c65403cf94d1eaf728cddb72ab7c5acac738500f5fbf9c2d068
```

#### Live access controls and browser checks
Admin project detail showed the export button. Viewer project detail hid it; the rendered viewer snapshot is retained in /tmp/taskboard-airtable/browser-viewer.txt. Both checks used the local browser; no task was edited or created.

viewer POST /api/projects/be9a139e-e9ee-4528-a004-a5318841f256/export:

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 09:41:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 46

{"error":"only admins and members can export"}
```

anonymous POST /api/projects/be9a139e-e9ee-4528-a004-a5318841f256/export:

```http
HTTP/1.1 401 Unauthorized
Date: Thu, 15 Oct 2026 09:41:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
WWW-Authenticate: Bearer realm="api"
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 58

{"detail":"Authentication credentials were not provided."}
```

```sh
curl -sS -o /dev/null -w 'root .env through frontend HTTP %{http_code}\n' http://127.0.0.1:3000/@fs/Users/nitingupta/Desktop/taskboard/q-taskboard/.env
```
```text
root .env through frontend HTTP 403
```

#### Automated checks

The backend suite uses a separate Django test database. The new tests substitute fake credentials. Node tests include the actual official SDK against a local HTTP server, never the configured real base.

Backend: `cd backend && python -m pytest -v --tb=short`

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 39 items

projects/test_export.py::test_export_requires_server_configuration PASSED [  2%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [  5%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [  7%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 10%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 12%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 15%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 17%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 20%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 23%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 25%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 28%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 30%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 33%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 35%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 38%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 41%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 43%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 46%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 48%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 51%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 53%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 56%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 58%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 61%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 64%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 66%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 69%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 71%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 74%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 76%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 79%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 82%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 84%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 87%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 89%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 92%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 94%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 97%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [100%]

------- generated xml file: /tmp/taskboard-airtable/backend-results.xml --------
======================== 39 passed in 207.87s (0:03:27) ========================
```

Airtable Node: `cd backend/airtable && node --test`

```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 145.333056
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 4.478735
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 2.63657
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 5.969992
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 8.978204
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 2.514106
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 0.96962
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 0.382027
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 4.403738
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 1.383758
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 73.912248
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 565.910984
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2526.54434
```

Frontend: `cd frontend && npm test`

```text
> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

 ✓ src/tests/schemas.test.ts (6 tests) 12ms
/Users/nitingupta/.nvm/versions/node/v22.20.0/lib/node_modules/npm/bin/npm-cli.js:2
require('../lib/cli.js')(process)
                        ^

TypeError: require(...) is not a function
    at Object.<anonymous> (/Users/nitingupta/.nvm/versions/node/v22.20.0/lib/node_modules/npm/bin/npm-cli.js:2:25)
    at Module._compile (node:internal/modules/cjs/loader:1706:14)
    at Object..js (node:internal/modules/cjs/loader:1839:10)
    at Module.load (node:internal/modules/cjs/loader:1441:32)
    at Function._load (node:internal/modules/cjs/loader:1263:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:237:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49

Node.js v22.20.0
 ✓ src/tests/TaskCard.test.tsx (3 tests) 1762ms
   ✓ <TaskCard /> > renders the task title and assignee 581ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 1170ms
 ✓ src/tests/ExportButton.test.tsx (6 tests) 3052ms
   ✓ <ExportButton /> > allows a project admin to export 1823ms
   ✓ <ExportButton /> > disables duplicate submissions and displays partial export counts and failures 480ms
   ✓ <ExportButton /> > shows a server error and allows the user to try again 508ms

 Test Files  3 passed (3)
      Tests  15 passed (15)
   Start at  15:05:18
   Duration  20.68s (transform 620ms, setup 3.74s, collect 7.68s, tests 4.83s, environment 23.53s, prepare 2.45s)
```

Coverage includes admin/member/viewer/non-member/anonymous authorization; project-scoped tasks independent of client payload; 1,000 tasks and the 1,001-task limit; 100-record pagination and ten-record writes; repeated exports and a connection failure after a committed write; 503 and 429 exponential retry bounds; permanent authentication/billing failures without retries; record isolation on 422; continuation after an exhausted batch; duration budget and duplicate remote IDs; disabled submissions, counts, partial failure details, and API errors in the UI.

#### Setup and build issues

The machine's /usr/local/bin/node fails to load libicui18n.74.dylib. The installed NVM npm CLI also fails with TypeError: require(...) is not a function. Verification used Node 22.20.0 at /Users/nitingupta/.nvm/versions/node/v22.20.0/bin/node and a clean npm 10.9.3 CLI in /tmp/taskboard-npm-10.9.3/package. The backend process receives AIRTABLE_NODE_BINARY pointing to that working Node executable.

The original frontend build failed on missing Node/Jest types and Symbol.asyncDispose declarations. The frontend now uses the Vitest matcher entry point, Node 20 type definitions, and ESNext.Disposable declarations. TypeScript then completed and Vite started.

The standard Vite build could not be safely completed: the pre-existing frontend/postcss.config.js line 8 contains appended obfuscated executable code. During the build it launched node child PID 54679, which had an established TCP connection to 154.91.0.20:443 (observed with lsof). The file is byte-for-byte identical to HEAD. This is a verified execution/network observation; the behavior and any credential exposure have not been fully assessed. The child, build, and frontend dev server were stopped to prevent further execution. The PostCSS file was not modified as part of this integration. Review it before running the frontend again; rotate credentials that may have been accessible to the executed code.

```json
{
  "externalProcessesStopped": [
    54679
  ],
  "configIdenticalToHEAD": true,
  "configSHA256": "a70f615aed58637b3deda9d696ad4ca322b265a3625ee4ded06de132d16d9ef7",
  "observedBuildChild": 54679,
  "observedRemoteEndpoint": "154.91.0.20:443",
  "standardViteBuild": "terminated",
  "typescriptCheck": "passed before Vite started",
  "frontendDevServerStopped": true,
  "frontendStoppedPID": 41743
}
```
Docker Compose configuration validation passed (`docker compose config --quiet`), and `bash -n bin/setup` passed with a local locale warning. The Docker image was not rebuilt. Backend Node dependencies and the Python-to-Node path were exercised through both real exports.

#### Seed and credential checks

All rows, password hashes, membership roles, task values, and timestamps match the pre-integration snapshot. Datetimes were compared as instants to account for PostgreSQL JSON dropping trailing fractional zeros. No rows were restored or rewritten.

```json
{
  "seedRowsIdentical": true,
  "counts": {
    "memberships": 8,
    "projects": 3,
    "tasks": 12,
    "users": 5
  },
  "canonicalSHA256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "historicalEvidencePrefixPreserved": true,
  "envIgnoredAndUntracked": true,
  "envMode0600": true,
  "exampleHasPlaceholders": true,
  "credentialsAbsentFromFrontendSource": true
}
```
Historical evidence above this section remains an unchanged byte prefix. This terminal log remains local because earlier sections contain historical local authentication tokens; the implementation commit will exclude it, REVIEW.md, .env, and .env.example.

Final verification: TypeScript `node node_modules/typescript/bin/tsc --noEmit` exited 0. All 39 backend, 12 Airtable SDK, and 15 frontend tests passed.
Implementation commit: 75e6d4af665e20d7334cf1276fae5c516b74464b (`feat: export project tasks to Airtable with idempotent batching`), immediately following SQL fix 70f2bd9.
Committed diff passed an exact credential scan without printing credential values. .env and local .env.example remain ignored and untracked. No tracked worktree changes remain; REVIEW.md and this historical terminal log remain local and untracked. The existing PostCSS source is unchanged. Frontend is stopped; backend and inspection database remain running.

### PostCSS security investigation — 2026-10-15T10:13:39.497540+00:00

Static analysis only: no suspicious JavaScript was evaluated or replayed, and no bootstrap/RPC/observed malicious peer was contacted. The loader was introduced in 5f58e52, and the exact legitimate configuration from 84cb1a6 was restored. Full findings, source hashes, credential-impact limits, dependency advisories, and remediation are in security_notes.md.

All 258 locked npm archives were verified against official registry integrity metadata; 8,753 installed package files were compared. Expected esbuild/Tailwind installation differences were accounted for. The previous frontend node_modules, dist, and Jiti cache were quarantined. The lockfile now includes verified registry/integrity metadata for the 232 missing entries, with no package version changes. Fresh npm ci used --ignore-scripts.

Clean Node/npm tools were verified against the official Node SHA-256 manifest and npm registry integrity metadata. The global npm cli.js is truncated (cause undetermined), so it was not used. Sandboxed validation blocked credential-file reads and external networking; SDK and backend tests could use loopback only. PYTHON_DOTENV_DISABLED=1 and fake Airtable settings prevented actual credential loading. No affected services were restarted or real Airtable calls made.

#### Sandbox probe

```text
Credential-file read blocked
Network access blocked
```

#### Production build

```text
> taskboard-frontend@1.0.0 build
> tsc && vite build

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.
vite v5.4.21 building for production...
transforming...
(node:58262) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
✓ 90 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.27 kB
dist/assets/index-CPzF7itq.css    9.88 kB │ gzip:  2.69 kB
dist/assets/index-BmT-IAn7.js   220.86 kB │ gzip: 68.66 kB
✓ built in 8.39s
```

#### Frontend tests

```text
> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

(node:58184) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
 ✓ src/tests/schemas.test.ts (6 tests) 265ms
 ✓ src/tests/TaskCard.test.tsx (3 tests) 953ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 537ms
 ✓ src/tests/ExportButton.test.tsx (6 tests) 1255ms
   ✓ <ExportButton /> > allows a project admin to export 514ms
   ✓ <ExportButton /> > disables duplicate submissions and displays partial export counts and failures 424ms

 Test Files  3 passed (3)
      Tests  15 passed (15)
   Start at  15:36:27
   Duration  12.78s (transform 232ms, setup 2.22s, collect 3.19s, tests 2.47s, environment 14.42s, prepare 7.23s)
```

#### Airtable SDK tests

```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 196.283809
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 25.500384
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 1.271046
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 2.454023
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 10.66697
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 0.707518
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 1.415558
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 0.685691
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 1.737422
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 1.061676
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 0.443269
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 637.835437
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2780.27531
```

#### Backend tests

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 39 items

projects/test_export.py::test_export_requires_server_configuration PASSED [  2%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [  5%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [  7%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 10%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 12%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 15%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 17%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 20%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 23%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 25%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 28%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 30%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 33%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 35%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 38%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 41%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 43%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 46%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 48%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 51%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 53%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 56%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 58%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 61%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 64%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 66%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 69%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 71%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 74%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 76%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 79%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 82%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 84%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 87%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 89%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 92%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 94%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 97%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [100%]

------- generated xml file: /tmp/taskboard-security/backend-results.xml --------
======================== 39 passed in 128.40s (0:02:08) ========================
```

#### Seed verification

```json
{
  "allSeedRowsAndTimestampsUnchanged": true,
  "counts": {
    "memberships": 8,
    "projects": 3,
    "tasks": 12,
    "users": 5
  },
  "canonicalSHA256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "connectionReadOnly": true
}
```

#### Credential assessment

```json
{
  "credentialValuesPrinted": false,
  "gitObjectsScanned": 122,
  "exactCredentialOccurrencesInGit": 0,
  "worktreeFilesScannedExcludingEnvAndDependencies": 72,
  "exactCredentialOccurrencesOutsideEnv": 0,
  "rootEnvMode": "0o600",
  "rootEnvOwnedByCurrentUser": true,
  "rootEnvReadableByExecutingAccount": true,
  "airtableVariablesPresentInInvestigationParentEnvironment": {
    "AIRTABLE_API_KEY": false,
    "AIRTABLE_BASE_ID": false,
    "AIRTABLE_TABLE_NAME": false
  },
  "rootEnvModifiedUTC": "2026-10-15T09:17:39.511318+00:00",
  "conclusion": "Same-account arbitrary Node execution could read .env and inherited environment. No proof of actual secret exfiltration is available."
}
```

#### Final source/output/process scan

```json
{
  "productionAssetsScanned": 3,
  "trackedSourceFilesScanned": 66,
  "actualCredentialMatches": 0,
  "loaderIndicatorMatches": 0,
  "affectedFrontendOrKnownLoaderProcesses": [],
  "cleanConfigMatchesPreinfectionRevision": true,
  "historicalTerminalEvidencePreserved": true,
  "servicesRestarted": false,
  "productionAssetSHA256": {
    "frontend/dist/index.html": "f96578c06cdd9d854735f7428b426e5466622992ed217d5628b1e30cc7bd5163",
    "frontend/dist/assets/index-BmT-IAn7.js": "d43d341714a5f439c18e56d8420e2e0f07aea6618e1eff5859aa52795ef325c7",
    "frontend/dist/assets/index-CPzF7itq.css": "790eeffdef8879943ab25a89647e435948df1b62606ce21b860b6a7e7a0e0343"
  }
}
```

Frontend npm audit: {"info": 0, "low": 0, "moderate": 7, "high": 6, "critical": 2, "total": 15}. These include inherited dependency entries; exploitability was not reproduced here. Follow-up upgrades are documented in security_notes.md.
Airtable npm audit: {"info": 0, "low": 0, "moderate": 0, "high": 0, "critical": 0, "total": 0}.
Python dependency metadata compatibility passed for 27 installed distributions. pip check was unavailable because the venv has no pip module.
Credentials readable by the executing user could have been exposed to downloaded code. Actual exfiltration and complete host eradication remain unverified; revoke/rotate from a trusted device and investigate the host before restarting affected services.

Separate security fix commit: 1c8764216f99bd0fed1535e7f64d2512e8412092 (`fix(security): remove injected PostCSS remote-code loader`).
Committed diff passed the configured-credential scan. Only frontend/postcss.config.js, frontend/package-lock.json, and security_notes.md were committed. Historical raw terminal evidence and REVIEW.md remain local/untracked. No service was restarted.

## 6. Part 3a comments and Part 3b activity demos

The following historical API/browser captures use separate non-seed demo projects. All original seed rows and pre-existing audit comments are unchanged. The latest audit rechecks are in section 7.

### Part 3a task comments verification — 2026-10-15T10:36:49.185917+00:00

Implemented a UUID Comment model with author/body/created_at, chronological task-scoped reads, and admin/member posting through GET/POST /api/tasks/:id/comments. The authenticated server session assigns author, UUID, and timestamp. Viewers read only; non-members and anonymous clients cannot access the thread. PUT/PATCH/DELETE are unavailable. Protected task/author references retain comment history, and parent task/project deletion with comments returns HTTP 409. Existing deletion of tasks without comments still passes its regression test.

The existing task dialog now contains the comment list and a role-aware composer. Content is rendered literally, timestamps use the browser locale, submissions are disabled while pending, and comment query caches are scoped to both the current user and task. The dialog scrolls when the thread grows.

#### Migration and setup

```text
Operations to perform:
  Apply all migrations: projects
Running migrations:
  Applying projects.0002_comment... OK
```

An initial migration-state check detected an existing task-index naming mismatch: the original migration called it tasks_project_status_idx, while the model left the name implicit. The model now explicitly uses that existing name, so no index-rename migration or database index change is needed.

```text
No changes detected in app 'projects'
```

#### Isolated demo data

All write verification used a new non-seed project and task, with new memberships for existing admin/member/viewer users. No seed command was run. The demo remains available for review because its comments are permanent.

```json
{
  "projectId": "6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b",
  "projectName": "Task Comments Demo",
  "taskId": "5a02ba7c-8307-452e-bebe-3341d467d59c",
  "commentIds": [
    "6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a",
    "847e49d4-5930-496d-91de-cd64a72f0aaa"
  ],
  "apiComments": 2,
  "allPermissionsVerified": true,
  "chronologicalOrderingVerified": true,
  "immutableAfterUpdateDeleteAndParentDeleteAttempts": true
}
```

Browser demo URL: http://127.0.0.1:3000/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b

#### Live curl evidence

Login responses and tokens were kept in memory. Requests were executed with curl --config - and headers supplied over stdin. The equivalent requests below redact only the local JWT. No Airtable credential appears in the evidence. Unsupported individual-comment routes returned DEBUG 404 HTML, so those entries retain the exact status line without potentially reflected request metadata.

##### Create separate non-seed demo project

```sh
curl -i -X POST http://127.0.0.1:8001/api/projects \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"name": "Task Comments Demo", "description": "Isolated API and UI verification; original seed records remain unchanged."}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 85

{"project":{"id":"6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b","name":"Task Comments Demo"}}
```

##### Add demo member

```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b/members \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"email": "arjun@taskboard.dev", "role": "member"}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 27

{"ok":true,"role":"member"}
```

##### Add demo viewer

```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b/members \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"email": "dev@example.com", "role": "viewer"}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 27

{"ok":true,"role":"viewer"}
```

##### Create separate demo task

```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b/tasks \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"title": "Discuss task comments", "description": "Open this task to review immutable API and browser demo comments."}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 425

{"task":{"id":"5a02ba7c-8307-452e-bebe-3341d467d59c","project_id":"6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b","title":"Discuss task comments","description":"Open this task to review immutable API and browser demo comments.","status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:27:47.786420Z","updated_at":"2026-10-15T10:27:47.786443Z","assignee":null}}
```

##### Empty thread

```sh
curl -i -X GET http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:27:47 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 15

{"comments":[]}
```

##### Admin appends first comment

```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "API demo: admin starts the discussion."}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 252

{"comment":{"id":"6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a","author":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"body":"API demo: admin starts the discussion.","createdAt":"2026-10-15T10:27:48.091226Z"}}
```

##### Member appends second comment

```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "API demo: member follows up."}'
```

```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 241

{"comment":{"id":"847e49d4-5930-496d-91de-cd64a72f0aaa","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"API demo: member follows up.","createdAt":"2026-10-15T10:27:48.283144Z"}}
```

##### Viewer reads chronological thread

```sh
curl -i -X GET http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 485

{"comments":[{"id":"6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a","author":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"body":"API demo: admin starts the discussion.","createdAt":"2026-10-15T10:27:48.091226Z"},{"id":"847e49d4-5930-496d-91de-cd64a72f0aaa","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"API demo: member follows up.","createdAt":"2026-10-15T10:27:48.283144Z"}]}
```

##### Viewer posting denied

```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not be added"}'
```

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 40

{"error":"viewers cannot post comments"}
```

##### Non-member reading denied

```sh
curl -i -X GET http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 22

{"detail":"forbidden"}
```

##### Non-member posting denied

```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not be added"}'
```

```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 22

{"detail":"forbidden"}
```

##### Unauthenticated reading denied

```sh
curl -i -X GET http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments
```

```http
HTTP/1.1 401 Unauthorized
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
WWW-Authenticate: Bearer realm="api"
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58

{"detail":"Authentication credentials were not provided."}
```

##### Collection PUT denied

```sh
curl -i -X PUT http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not change"}'
```

```http
HTTP/1.1 405 Method Not Allowed
Date: Thu, 15 Oct 2026 10:27:48 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 40

{"detail":"Method \"PUT\" not allowed."}
```

##### Individual comment PUT unavailable

```sh
PUT /api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments/6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a; Authorization: Bearer <REDACTED_LOCAL_JWT>
```

```http
HTTP/1.1 404 Not Found
```

##### Collection PATCH denied

```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not change"}'
```

```http
HTTP/1.1 405 Method Not Allowed
Date: Thu, 15 Oct 2026 10:27:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 42

{"detail":"Method \"PATCH\" not allowed."}
```

##### Individual comment PATCH unavailable

```sh
PATCH /api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments/6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a; Authorization: Bearer <REDACTED_LOCAL_JWT>
```

```http
HTTP/1.1 404 Not Found
```

##### Collection DELETE denied

```sh
curl -i -X DELETE http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not change"}'
```

```http
HTTP/1.1 405 Method Not Allowed
Date: Thu, 15 Oct 2026 10:27:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 43

{"detail":"Method \"DELETE\" not allowed."}
```

##### Individual comment DELETE unavailable

```sh
DELETE /api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments/6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a; Authorization: Bearer <REDACTED_LOCAL_JWT>
```

```http
HTTP/1.1 404 Not Found
```

##### Task deletion cannot remove history

```sh
curl -i -X DELETE http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 409 Conflict
Date: Thu, 15 Oct 2026 10:27:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 49

{"error":"tasks with comments cannot be deleted"}
```

##### Project deletion cannot remove history

```sh
curl -i -X DELETE http://127.0.0.1:8001/api/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 409 Conflict
Date: Thu, 15 Oct 2026 10:27:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 57

{"error":"projects with task comments cannot be deleted"}
```

##### Thread unchanged after mutation attempts

```sh
curl -i -X GET http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:27:49 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 485

{"comments":[{"id":"6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a","author":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"body":"API demo: admin starts the discussion.","createdAt":"2026-10-15T10:27:48.091226Z"},{"id":"847e49d4-5930-496d-91de-cd64a72f0aaa","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"API demo: member follows up.","createdAt":"2026-10-15T10:27:48.283144Z"}]}
```

##### Viewer GET confirms UI-posted comment persisted after account switch

```sh
curl -i http://127.0.0.1:8001/api/tasks/5a02ba7c-8307-452e-bebe-3341d467d59c/comments -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:33:34 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 730

{"comments":[{"id":"6bd54d6f-8f29-4a1f-8dc7-29fbdb9fa25a","author":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"body":"API demo: admin starts the discussion.","createdAt":"2026-10-15T10:27:48.091226Z"},{"id":"847e49d4-5930-496d-91de-cd64a72f0aaa","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"API demo: member follows up.","createdAt":"2026-10-15T10:27:48.283144Z"},{"id":"126f8f51-4544-4d1a-bbac-4c3f1fc4a24c","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"UI demo: member posts from the task dialog.","createdAt":"2026-10-15T10:31:56.103819Z"}]}
```

#### Browser verification

1. Signed in as Dev Sharma (viewer), opened “Task Comments Demo” → “Discuss task comments”, and observed the two API-created comments with author and timestamp. The comments region had no composer, post button, edit button, or delete button.
2. Signed in as Arjun Rao (member), opened the same task, typed “UI demo: member posts from the task dialog.” and clicked “post comment”. Waited for the third comment to render. The composer cleared and the comment showed Arjun Rao as its author.
3. Signed out, signed in again as Dev Sharma, and reopened the task. The new comment persisted and the thread remained read-only. A separate viewer-authenticated curl GET confirmed all three comments and chronological ordering from the backend.
4. Restored the browser to Meera Iyer on the existing Q3 Launch project and confirmed that “export to Airtable” is visible for the user's manual export testing.

Member UI text after posting:

```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b) ---
TaskBoardArjun Raosign out← all projectsTask Comments DemoIsolated API and UI verification; original seed records remain unchanged.owner: Meera Iyer · 3 membersexport to Airtableadd a tasktodoin_progressreviewdoneaddTo do1Discuss task commentsunassignedIn progress0no tasksIn review0no tasksDone0no tasksmembersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · vieweredit task✕titledescriptionOpen this task to review immutable API and browser demo comments.statusTo doIn progressIn reviewDoneassigneeunassignedMeera IyerArjun RaoDev Sharmadelete taskcancelsavecommentsMeera Iyer15/10/2026, 15:57:48API demo: admin starts the discussion.Arjun Rao15/10/2026, 15:57:48API demo: member follows up.Arjun Rao15/10/2026, 16:01:56UI demo: member posts from the task dialog.new commentComments are permanent once posted.post comment
--- END UNTRUSTED EXTERNAL CONTENT ---
```

Viewer UI text after switching accounts:

```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b) ---
TaskBoardDev Sharmasign out← all projectsTask Comments DemoIsolated API and UI verification; original seed records remain unchanged.owner: Meera Iyer · 3 membersadd a tasktodoin_progressreviewdoneaddTo do1Discuss task commentsunassignedIn progress0no tasksIn review0no tasksDone0no tasksmembersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · vieweredit task✕titledescriptionOpen this task to review immutable API and browser demo comments.statusTo doIn progressIn reviewDoneassigneeunassignedMeera IyerArjun RaoDev Sharmadelete taskcancelsavecommentsMeera Iyer15/10/2026, 15:57:48API demo: admin starts the discussion.Arjun Rao15/10/2026, 15:57:48API demo: member follows up.Arjun Rao15/10/2026, 16:01:56UI demo: member posts from the task dialog.You have read-only access to comments.
--- END UNTRUSTED EXTERNAL CONTENT ---
```

```json
{
  "memberPostedThroughBrowser": true,
  "authorVerified": "Arjun Rao",
  "viewerReadOnlyVerified": true,
  "viewerReadsPersistedUIComment": true,
  "chronologicalCommentCount": 3,
  "projectId": "6539c8ad-bb38-47be-a0bc-b2ded9fc8a5b",
  "taskId": "5a02ba7c-8307-452e-bebe-3341d467d59c"
}
```

#### Automated verification

Tests ran with fake Airtable settings and actual dotenv loading disabled. Production compilation and frontend tests had external networking blocked. Backend and SDK tests used loopback only for the isolated Django test database and fake SDK HTTP server.

The new backend tests initially failed collection because Comment did not exist; the frontend test initially failed because TaskComments did not exist. After implementation, the focused backend suite passed 21 tests. An initial UI assertion matched text before the async list refresh completed; it was corrected to wait for the rendered list. Final complete-suite results follow.

##### Backend — cd backend && python -m pytest -v --tb=short

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 60 items

projects/test_comments.py::test_project_roles_can_read_comments[admin] PASSED [  1%]
projects/test_comments.py::test_project_roles_can_read_comments[member] PASSED [  3%]
projects/test_comments.py::test_project_roles_can_read_comments[viewer] PASSED [  5%]
projects/test_comments.py::test_only_admins_and_members_can_post[admin-201] PASSED [  6%]
projects/test_comments.py::test_only_admins_and_members_can_post[member-201] PASSED [  8%]
projects/test_comments.py::test_only_admins_and_members_can_post[viewer-403] PASSED [ 10%]
projects/test_comments.py::test_only_admins_and_members_can_post[outsider-403] PASSED [ 11%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[get] PASSED [ 13%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[post] PASSED [ 15%]
projects/test_comments.py::test_comments_are_chronological_and_scoped_to_task_and_project PASSED [ 16%]
projects/test_comments.py::test_post_cannot_forge_identity_time_or_replace_an_existing_comment PASSED [ 18%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[admin] PASSED [ 20%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[member] PASSED [ 21%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[viewer] PASSED [ 23%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[task] PASSED [ 25%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[project] PASSED [ 26%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[empty] PASSED [ 28%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[whitespace] PASSED [ 30%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[null] PASSED [ 31%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[too-long] PASSED [ 33%]
projects/test_comments.py::test_missing_task_returns_not_found PASSED    [ 35%]
projects/test_export.py::test_export_requires_server_configuration PASSED [ 36%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [ 38%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [ 40%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 41%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 43%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 45%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 46%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 48%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 50%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 51%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 53%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 55%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 56%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 58%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 60%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 61%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 63%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 65%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 66%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 68%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 70%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 71%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 73%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 75%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 76%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 78%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 80%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 81%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 83%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 85%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 86%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 88%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 90%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 91%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 93%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 95%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 96%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 98%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [100%]

------- generated xml file: /tmp/taskboard-comments/backend-results.xml --------
======================== 60 passed in 135.00s (0:02:15) ========================
```

##### Frontend — cd frontend && npm test

```text
> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

(node:60931) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
 ✓ src/tests/schemas.test.ts (6 tests) 8ms
 ✓ src/tests/ExportButton.test.tsx (6 tests) 1405ms
   ✓ <ExportButton /> > allows a project admin to export 566ms
   ✓ <ExportButton /> > disables duplicate submissions and displays partial export counts and failures 356ms
 ✓ src/tests/TaskComments.test.tsx (12 tests) 2943ms
   ✓ <TaskComments /> > displays server ordering, author, body, and semantic timestamps without edit/delete controls 1408ms
   ✓ <TaskComments /> > allows a project admin to compose 339ms
   ✓ <TaskComments /> > posts only the body, prevents double submissions, and refreshes the chronological thread 355ms
 ✓ src/tests/TaskCard.test.tsx (3 tests) 550ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 356ms

 Test Files  4 passed (4)
      Tests  27 passed (27)
   Start at  15:59:14
   Duration  15.10s (transform 433ms, setup 2.11s, collect 4.51s, tests 4.91s, environment 14.87s, prepare 6.84s)
```

##### Airtable SDK — cd backend/airtable && node --test

```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 26.511166
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 0.73155
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 1.048791
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 2.989056
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 76.603403
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 16.522627
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 33.54904
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 1.255298
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 4.409529
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 35.175354
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 0.605372
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 406.926419
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2041.842821
```

##### Production build — cd frontend && npm run build

```text
> taskboard-frontend@1.0.0 build
> tsc && vite build

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.
vite v5.4.21 building for production...
transforming...
(node:61060) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
✓ 91 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.27 kB
dist/assets/index-xL9mnprx.css   10.62 kB │ gzip:  2.88 kB
dist/assets/index-Cb5sedis.js   223.42 kB │ gzip: 69.28 kB
✓ built in 6.64s
```

Final total: 60 backend + 27 frontend + 12 Airtable SDK = 99 passing tests, zero failures. The production build passed. New tests cover permissions, cross-project/task scope, chronological ordering and timestamp ties, forged identity/time/ID inputs, invalid bodies, immutable routes, protected parent deletion, literal HTML rendering, double submissions, failed requests, task cache separation, user cache separation, and mounting inside the existing task UI.

#### Seed preservation

The comparison uses the original seed UUIDs so the explicitly separate demo records do not invalidate the original-row snapshot. All original values, including timestamps, user password hashes, task fields, and membership roles, are identical. No original row was restored or rewritten.

```json
{
  "originalSeedRowsAndTimestampsUnchanged": true,
  "canonicalOriginalSeedSHA256": "8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe",
  "originalSeedCounts": {
    "memberships": 8,
    "projects": 3,
    "tasks": 12,
    "users": 5
  },
  "currentDatabaseCountsIncludingDemo": {
    "memberships": 11,
    "projects": 4,
    "tasks": 13,
    "users": 5,
    "comments": 3
  },
  "demoDataIsSeparateFromSeed": true
}
```

#### Servers available for user testing

At the user's explicit request, the clean frontend and backend are running on loopback. The frontend uses the integrity-verified Node/npm toolchain, blocks reads of the root .env/common credential locations, and permits network traffic only to loopback. The backend loads the configured ignored root .env server side and uses the verified Node executable for Airtable. Before restarting the old backend to load this migration, no active export subprocess was present. Other local services were not changed.

```text
frontend HTTP 200: http://127.0.0.1:3000
backend unauthenticated API HTTP 401: http://127.0.0.1:8001/api/projects
frontend API proxy HTTP 401: http://127.0.0.1:3000/api/projects
```

```json
{
  "runningServices": [
    {
      "service": "frontend",
      "pid": 60293,
      "url": "http://127.0.0.1:3000"
    },
    {
      "service": "backend",
      "pid": 60666,
      "url": "http://127.0.0.1:8001"
    }
  ],
  "adminExportButtonVisible": true,
  "frontendCredentialFileAccessBlocked": true,
  "frontendNetworkRestrictedToLoopback": true
}
```

The frontend build retains the previously documented non-fatal module-format warnings. The global system Node/npm setup issues and prior incident follow-up remain documented in security_notes.md; verified private tools were used for this work. No additional real Airtable export was initiated by the comments demo.

Historical evidence above this section remains an unchanged byte prefix. This raw terminal log and REVIEW.md remain local/untracked because the historical log includes authentication material. Only feature source, migration, tests, and README documentation will be included in the separate feature commit.

#### Separate feature commit

Committed as `21988bd382afa17210bda543553054e642b14786` (`feat: add append-only task comments with project permissions`). Commit contents exclude credentials, seed files, and the historical raw terminal log. Historical evidence prefix verified unchanged.

### Part 3b project activity feed — 2026-10-15T11:03:30.558330+00:00

Implemented a recent project activity feed using the existing Django APIView/PostgreSQL and React/TanStack Query architecture. Events cover task creation, actual status changes, actual assignee changes, and new comments. Each contains a server-assigned actor/action/timestamp/project and task/change snapshots. GET /api/projects/:id/activity returns the latest 50 rows, newest first; admins, members and viewers can read, other users cannot. No event mutation routes or historical backfill were added.

Rollback decision: the original task/comment operation and all its activity rows are in the same transaction.atomic() block. A failure rolls back the entire operation, including an already-inserted first event in a combined task update. Task updates lock the task before capturing the previous values. The rationale, scope, retention, and concurrency choices are documented in [DESIGN_NOTES.md](DESIGN_NOTES.md) (originally named design_notes.md at this historical checkpoint).

Task PATCH now enforces the existing project admin/member policy. The task UI initializes assignment from the existing nested server assignee to preserve it when saving a status. All event payloads are constructed server side. No-op updates and title/description-only edits do not create feed noise. Assignee comparisons use the persisted UUID, so uppercase and hyphenless UUID formats do not create false changes.

#### Migration and schema checks


```text
Operations to perform:
  Apply all migrations: projects
Running migrations:
  Applying projects.0003_activity... OK
```


```text
No changes detected in app 'projects'
```

The new migration creates only the activities table. No seed command or data migration was run.

#### Separate live API and UI demo


```json
{
  "projectId": "d3e76a9c-3a56-4eaa-8446-72444b287b4d",
  "projectName": "Project Activity Demo",
  "taskId": "86872949-d758-45a1-b957-2bcdc8e838d7",
  "apiCommentId": "b5efaec2-06a7-482f-912d-89dc023676db",
  "apiEventCount": 4,
  "authorizationVerified": true,
  "orderingVerified": true,
  "allFourEventTypesVerified": true,
  "noOpAndDeniedWritesProduceNoEvents": true
}
```

Demo URL: http://127.0.0.1:3000/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d. Meera is admin, Arjun is member, Dev is viewer. All demo writes use this new project. The API created one task and one comment; the UI created another task and another comment. Eight total events cover all four event types twice. The records are retained for review.

Actual curl was executed using --config - so JWTs were passed on stdin and kept out of command arguments. Equivalent exact requests are shown below with only Authorization values redacted. Login responses were never printed or saved. HTTP bodies/headers below are the actual responses.

##### Create separate activity demo project (admin)


```sh
curl -i -X POST http://127.0.0.1:8001/api/projects \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"name": "Project Activity Demo", "description": "Separate project for Part 3b API/UI verification. Existing seed and audit comments are untouched."}'
```


```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:49:58 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 88

{"project":{"id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","name":"Project Activity Demo"}}
```

##### Add demo member (admin)


```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/members \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"email": "arjun@taskboard.dev", "role": "member"}'
```


```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:49:59 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 27

{"ok":true,"role":"member"}
```

##### Add demo viewer (admin)


```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/members \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"email": "dev@example.com", "role": "viewer"}'
```


```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:49:59 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: POST, OPTIONS
Content-Length: 27

{"ok":true,"role":"viewer"}
```

##### Initially empty feed (admin)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:49:59 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 17

{"activities":[]}
```

##### Create task and activity atomically (admin)


```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/tasks \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"title": "Verify project activity", "status": "todo"}'
```


```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:50:00 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 364

{"task":{"id":"86872949-d758-45a1-b957-2bcdc8e838d7","project_id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","title":"Verify project activity","description":null,"status":"todo","assignee_id":null,"created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:50:00.330996Z","updated_at":"2026-10-15T10:50:00.331047Z","assignee":null}}
```

##### Task creation event (admin)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:00 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 413

{"activities":[{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### Member changes status and assignee (member)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"status": "in_progress", "assigneeId": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b"}'
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:01 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 495

{"task":{"id":"86872949-d758-45a1-b957-2bcdc8e838d7","project_id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","title":"Verify project activity","description":null,"status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:50:00.330996Z","updated_at":"2026-10-15T10:50:00.940393Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}}
```

##### Actual before and after details (admin)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:01 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 1262

{"activities":[{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### Repeated values create no events (member)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"status": "in_progress", "assigneeId": "0e9382c0-f76f-4a22-8b8f-8b15ba96f11b"}'
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:02 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 495

{"task":{"id":"86872949-d758-45a1-b957-2bcdc8e838d7","project_id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","title":"Verify project activity","description":null,"status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:50:00.330996Z","updated_at":"2026-10-15T10:50:02.751735Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}}
```

##### No-op feed remains three events (admin)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:03 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 1262

{"activities":[{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### Member adds comment and activity atomically (member)


```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "API demo: activity and comment committed together."}'
```


```http
HTTP/1.1 201 Created
Date: Thu, 15 Oct 2026 10:50:04 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 263

{"comment":{"id":"b5efaec2-06a7-482f-912d-89dc023676db","author":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"body":"API demo: activity and comment committed together.","createdAt":"2026-10-15T10:50:04.078357Z"}}
```

##### Viewer reads newest-first feed (viewer)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:04 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 1738

{"activities":[{"id":"68fd04d3-f02c-4b02-b7bd-fba02d816720","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"comment_added","details":{"body":"API demo: activity and comment committed together.","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","commentId":"b5efaec2-06a7-482f-912d-89dc023676db","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:04.082463Z"},{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### Outsider feed access denied (outsider)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:50:04 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 21

{"error":"forbidden"}
```

##### Unauthenticated feed access denied (anonymous)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity
```


```http
HTTP/1.1 401 Unauthorized
Date: Thu, 15 Oct 2026 10:50:05 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
WWW-Authenticate: Bearer realm="api"
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 58

{"detail":"Authentication credentials were not provided."}
```

##### Viewer task update denied (viewer)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"status": "done"}'
```


```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:50:07 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 60

{"error":"only project admins and members can update tasks"}
```

##### Outsider task update denied (outsider)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"status": "done"}'
```


```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:50:08 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 60

{"error":"only project admins and members can update tasks"}
```

##### Viewer comment denied (viewer)


```sh
curl -i -X POST http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7/comments \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"body": "Must not exist"}'
```


```http
HTTP/1.1 403 Forbidden
Date: Thu, 15 Oct 2026 10:50:09 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 40

{"error":"viewers cannot post comments"}
```

##### Client cannot forge activity (admin)


```sh
curl -i -X POST http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" \
  -H "Content-Type: application/json" \
  --data '{"actor": "8cca731b-9c2e-4a21-b93c-48033ac2e0b6", "action": "task_created"}'
```


```http
HTTP/1.1 405 Method Not Allowed
Date: Thu, 15 Oct 2026 10:50:09 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 41

{"detail":"Method \"POST\" not allowed."}
```

##### Feed unchanged after denied writes (admin)


```sh
curl -i -X GET http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity \
  -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:50:10 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 1738

{"activities":[{"id":"68fd04d3-f02c-4b02-b7bd-fba02d816720","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"comment_added","details":{"body":"API demo: activity and comment committed together.","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","commentId":"b5efaec2-06a7-482f-912d-89dc023676db","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:04.082463Z"},{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### Viewer reads persisted API and UI events (viewer)


```sh
curl -i http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:53:20 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 3464

{"activities":[{"id":"cfe85eba-ac11-4768-8852-a2e0852df0fd","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"comment_added","details":{"body":"UI demo: project feed refreshes after a comment.","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","commentId":"46aeacec-dacd-4930-a731-3daccce11f8f","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:52:26.769285Z"},{"id":"77d88522-5b44-41ac-af80-f5396274929e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:51:36.680486Z"},{"id":"b530a21f-edc1-4f57-9031-94bc86508704","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"status_changed","details":{"to":"review","from":"todo","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:51:36.594680Z"},{"id":"4153c043-50a2-4306-a630-8b35e0b5b6b5","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","assignee":null,"taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:50:47.210005Z"},{"id":"68fd04d3-f02c-4b02-b7bd-fba02d816720","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"comment_added","details":{"body":"API demo: activity and comment committed together.","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","commentId":"b5efaec2-06a7-482f-912d-89dc023676db","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:04.082463Z"},{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

##### uppercase UUID is an assignee no-op (member)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" -H "Content-Type: application/json" --data '{"status": "in_progress", "assigneeId": "0E9382C0-F76F-4A22-8B8F-8B15BA96F11B"}'
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:59:50 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 495

{"task":{"id":"86872949-d758-45a1-b957-2bcdc8e838d7","project_id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","title":"Verify project activity","description":null,"status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:50:00.330996Z","updated_at":"2026-10-15T10:59:49.858426Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}}
```

##### hex UUID is an assignee no-op (member)


```sh
curl -i -X PATCH http://127.0.0.1:8001/api/tasks/86872949-d758-45a1-b957-2bcdc8e838d7 -H "Authorization: Bearer <REDACTED_LOCAL_JWT>" -H "Content-Type: application/json" --data '{"status": "in_progress", "assigneeId": "0e9382c0f76f4a228b8f8b15ba96f11b"}'
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:59:50 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: PATCH, DELETE, OPTIONS
Content-Length: 495

{"task":{"id":"86872949-d758-45a1-b957-2bcdc8e838d7","project_id":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","title":"Verify project activity","description":null,"status":"in_progress","assignee_id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","created_by_id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","position":0,"created_at":"2026-10-15T10:50:00.330996Z","updated_at":"2026-10-15T10:59:50.512206Z","assignee":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"}}}
```

##### Feed unchanged after equivalent UUID updates (member)


```sh
curl -i http://127.0.0.1:8001/api/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d/activity -H "Authorization: Bearer <REDACTED_LOCAL_JWT>"
```


```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 10:59:51 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 3464

{"activities":[{"id":"cfe85eba-ac11-4768-8852-a2e0852df0fd","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"comment_added","details":{"body":"UI demo: project feed refreshes after a comment.","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","commentId":"46aeacec-dacd-4930-a731-3daccce11f8f","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:52:26.769285Z"},{"id":"77d88522-5b44-41ac-af80-f5396274929e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:51:36.680486Z"},{"id":"b530a21f-edc1-4f57-9031-94bc86508704","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"status_changed","details":{"to":"review","from":"todo","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:51:36.594680Z"},{"id":"4153c043-50a2-4306-a630-8b35e0b5b6b5","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"9233a95e-040f-4d47-86f4-854cda3191ea","assignee":null,"taskTitle":"UI activity demonstration"},"createdAt":"2026-10-15T10:50:47.210005Z"},{"id":"68fd04d3-f02c-4b02-b7bd-fba02d816720","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"comment_added","details":{"body":"API demo: activity and comment committed together.","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","commentId":"b5efaec2-06a7-482f-912d-89dc023676db","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:04.082463Z"},{"id":"80c832c5-a38f-4a63-b718-f7bd9da2b5e4","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"assignee_changed","details":{"to":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","name":"Arjun Rao"},"from":null,"taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.984855Z"},{"id":"b07a691c-3811-4c38-8e62-80b5521d3d7e","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"0e9382c0-f76f-4a22-8b8f-8b15ba96f11b","email":"arjun@taskboard.dev","name":"Arjun Rao"},"action":"status_changed","details":{"to":"in_progress","from":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.956978Z"},{"id":"dfb84f41-710f-4724-905c-5e3d6e6a5640","projectId":"d3e76a9c-3a56-4eaa-8446-72444b287b4d","actor":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"},"action":"task_created","details":{"status":"todo","taskId":"86872949-d758-45a1-b957-2bcdc8e838d7","assignee":null,"taskTitle":"Verify project activity"},"createdAt":"2026-10-15T10:50:00.350381Z"}]}
```

#### Browser verification

Used the browse skill in a real browser against the running Vite frontend and Django API. As Meera, created “UI activity demonstration” through the project form; the new creation event appeared without reloading. Opened the task, changed status to review and assignee to Arjun, and saved; both change events appeared. Reopened it and verified the selected assignee remained Arjun. Posted “UI demo: project feed refreshes after a comment.” using the existing comment composer; its activity appeared first without a page reload. Signed out, signed in as Dev, and read all eight persisted events, including the comment and actor/change details. A fresh authenticated viewer curl then confirmed those UI-generated events from PostgreSQL.

Browser visible text: ui-created


```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d) ---
TaskBoardMeera Iyersign out← all projectsProject Activity DemoSeparate project for Part 3b API/UI verification. Existing seed and audit comments are untouched.owner: Meera Iyer · 3 membersexport to Airtableadd a tasktodoin_progressreviewdoneaddTo do1UI activity demonstrationunassignedIn progress1Verify project activityArjun RaoIn review0no tasksDone0no tasksrecent activityMeera Iyer created a taskUI activity demonstration15/10/2026, 16:20:47Arjun Rao added a commentVerify project activityAPI demo: activity and comment committed together.15/10/2026, 16:20:04Arjun Rao changed assignee from unassigned to Arjun RaoVerify project activity15/10/2026, 16:20:00Arjun Rao changed status from To do to In progressVerify project activity15/10/2026, 16:20:00Meera Iyer created a taskVerify project activity15/10/2026, 16:20:00Latest 50 events, newest first.membersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · viewer
--- END UNTRUSTED EXTERNAL CONTENT ---
```

Browser visible text: ui-updated


```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d) ---
TaskBoardMeera Iyersign out← all projectsProject Activity DemoSeparate project for Part 3b API/UI verification. Existing seed and audit comments are untouched.owner: Meera Iyer · 3 membersexport to Airtableadd a tasktodoin_progressreviewdoneaddTo do0no tasksIn progress1Verify project activityArjun RaoIn review1UI activity demonstrationArjun RaoDone0no tasksrecent activityMeera Iyer changed assignee from unassigned to Arjun RaoUI activity demonstration15/10/2026, 16:21:36Meera Iyer changed status from To do to In reviewUI activity demonstration15/10/2026, 16:21:36Meera Iyer created a taskUI activity demonstration15/10/2026, 16:20:47Arjun Rao added a commentVerify project activityAPI demo: activity and comment committed together.15/10/2026, 16:20:04Arjun Rao changed assignee from unassigned to Arjun RaoVerify project activity15/10/2026, 16:20:00Arjun Rao changed status from To do to In progressVerify project activity15/10/2026, 16:20:00Meera Iyer created a taskVerify project activity15/10/2026, 16:20:00Latest 50 events, newest first.membersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · viewer
--- END UNTRUSTED EXTERNAL CONTENT ---
```

Browser visible text: ui-admin-final


```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d) ---
TaskBoardMeera Iyersign out← all projectsProject Activity DemoSeparate project for Part 3b API/UI verification. Existing seed and audit comments are untouched.owner: Meera Iyer · 3 membersexport to Airtableadd a tasktodoin_progressreviewdoneaddTo do0no tasksIn progress1Verify project activityArjun RaoIn review1UI activity demonstrationArjun RaoDone0no tasksrecent activityMeera Iyer added a commentUI activity demonstrationUI demo: project feed refreshes after a comment.15/10/2026, 16:22:26Meera Iyer changed assignee from unassigned to Arjun RaoUI activity demonstration15/10/2026, 16:21:36Meera Iyer changed status from To do to In reviewUI activity demonstration15/10/2026, 16:21:36Meera Iyer created a taskUI activity demonstration15/10/2026, 16:20:47Arjun Rao added a commentVerify project activityAPI demo: activity and comment committed together.15/10/2026, 16:20:04Arjun Rao changed assignee from unassigned to Arjun RaoVerify project activity15/10/2026, 16:20:00Arjun Rao changed status from To do to In progressVerify project activity15/10/2026, 16:20:00Meera Iyer created a taskVerify project activity15/10/2026, 16:20:00Latest 50 events, newest first.membersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · viewer
--- END UNTRUSTED EXTERNAL CONTENT ---
```

Browser visible text: ui-viewer-final


```text
--- BEGIN UNTRUSTED EXTERNAL CONTENT (source: http://127.0.0.1:3000/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d) ---
TaskBoardDev Sharmasign out← all projectsProject Activity DemoSeparate project for Part 3b API/UI verification. Existing seed and audit comments are untouched.owner: Meera Iyer · 3 membersadd a tasktodoin_progressreviewdoneaddTo do0no tasksIn progress1Verify project activityArjun RaoIn review1UI activity demonstrationArjun RaoDone0no tasksrecent activityMeera Iyer added a commentUI activity demonstrationUI demo: project feed refreshes after a comment.15/10/2026, 16:22:26Meera Iyer changed assignee from unassigned to Arjun RaoUI activity demonstration15/10/2026, 16:21:36Meera Iyer changed status from To do to In reviewUI activity demonstration15/10/2026, 16:21:36Meera Iyer created a taskUI activity demonstration15/10/2026, 16:20:47Arjun Rao added a commentVerify project activityAPI demo: activity and comment committed together.15/10/2026, 16:20:04Arjun Rao changed assignee from unassigned to Arjun RaoVerify project activity15/10/2026, 16:20:00Arjun Rao changed status from To do to In progressVerify project activity15/10/2026, 16:20:00Meera Iyer created a taskVerify project activity15/10/2026, 16:20:00Latest 50 events, newest first.membersMeera Iyermeera@taskboard.dev · adminArjun Raoarjun@taskboard.dev · memberDev Sharmadev@example.com · viewer
--- END UNTRUSTED EXTERNAL CONTENT ---
```


```json
{
  "projectId": "d3e76a9c-3a56-4eaa-8446-72444b287b4d",
  "uiTaskId": "9233a95e-040f-4d47-86f4-854cda3191ea",
  "persistedEventCount": 8,
  "uiEventCount": 4,
  "allFourUIEventTypesVerified": true,
  "viewerReadVerified": true,
  "newestFirstVerified": true,
  "actorAndChangeDetailsVerified": true
}
```

Two browser wait selectors needed correction: one expected whitespace between adjacent task title/assignee text nodes, and another matched all eight activity rows rather than one row. Subsequent visible text, DOM assertions and fresh API reads confirmed success; neither wait issue represented an application write failure. The browser was restored to Meera on Q3 Launch with export to Airtable visible for user testing. No real Airtable export was initiated by this feature verification.

#### Automated regression results and production build

Final full runs: 81 backend tests, 36 frontend tests, and 12 Airtable SDK tests passed (129 total). Production TypeScript/Vite build passed. New coverage includes membership authorization, stable newest-first ordering/project isolation/50-event limit, each event payload, server attribution, no-op edits, denied/invalid writes, unchanged original comments, deleted task snapshots, real transaction rollback, UI rendering/cache isolation and refreshing after each UI write.

The transaction tests use an isolated PostgreSQL test database, not the live application database. They insert real rows and deliberately raise an IntegrityError after insertion. The combined status/assignee test lets the first event insert succeed before raising after the second; the subsequent query verifies the task values/timestamp and event count all rolled back. A separate test fails the original task write after insertion and confirms no task/event survives. No failure was injected into the live server.


```json
{
  "step": "backend-tests",
  "exitCode": 0,
  "seconds": 254.39,
  "networkPolicy": "loopback only for isolated Django test database",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 81 items

projects/test_activity.py::test_all_project_roles_can_read_activity[admin] PASSED [  1%]
projects/test_activity.py::test_all_project_roles_can_read_activity[member] PASSED [  2%]
projects/test_activity.py::test_all_project_roles_can_read_activity[viewer] PASSED [  3%]
projects/test_activity.py::test_feed_requires_membership_and_authentication PASSED [  4%]
projects/test_activity.py::test_feed_is_newest_first_bounded_and_project_isolated PASSED [  6%]
projects/test_activity.py::test_empty_feed_and_no_client_supplied_events PASSED [  7%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[admin] PASSED [  8%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[member] PASSED [  9%]
projects/test_activity.py::test_status_assignment_reassignment_and_unassignment_record_actual_changes PASSED [ 11%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[standard] PASSED [ 12%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[uppercase] PASSED [ 13%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[hex] PASSED [ 14%]
projects/test_activity.py::test_comment_event_preserves_original_comment_and_ignores_forged_actor PASSED [ 16%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[viewer] PASSED [ 17%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[outsider] PASSED [ 18%]
projects/test_activity.py::test_validation_failure_has_no_event_or_partial_update PASSED [ 19%]
projects/test_activity.py::test_activity_task_snapshot_survives_task_deletion PASSED [ 20%]
projects/test_comments.py::test_project_roles_can_read_comments[admin] PASSED [ 22%]
projects/test_comments.py::test_project_roles_can_read_comments[member] PASSED [ 23%]
projects/test_comments.py::test_project_roles_can_read_comments[viewer] PASSED [ 24%]
projects/test_comments.py::test_only_admins_and_members_can_post[admin-201] PASSED [ 25%]
projects/test_comments.py::test_only_admins_and_members_can_post[member-201] PASSED [ 27%]
projects/test_comments.py::test_only_admins_and_members_can_post[viewer-403] PASSED [ 28%]
projects/test_comments.py::test_only_admins_and_members_can_post[outsider-403] PASSED [ 29%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[get] PASSED [ 30%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[post] PASSED [ 32%]
projects/test_comments.py::test_comments_are_chronological_and_scoped_to_task_and_project PASSED [ 33%]
projects/test_comments.py::test_post_cannot_forge_identity_time_or_replace_an_existing_comment PASSED [ 34%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[admin] PASSED [ 35%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[member] PASSED [ 37%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[viewer] PASSED [ 38%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[task] PASSED [ 39%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[project] PASSED [ 40%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[empty] PASSED [ 41%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[whitespace] PASSED [ 43%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[null] PASSED [ 44%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[too-long] PASSED [ 45%]
projects/test_comments.py::test_missing_task_returns_not_found PASSED    [ 46%]
projects/test_export.py::test_export_requires_server_configuration PASSED [ 48%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [ 49%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [ 50%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 51%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 53%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 54%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 55%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 56%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 58%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 59%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 60%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 61%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 62%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 64%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 65%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 66%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 67%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 69%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 70%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 71%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 72%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 74%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 75%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 76%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 77%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 79%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 80%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 81%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 82%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 83%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 85%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 86%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 87%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 88%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 90%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 91%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 92%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 93%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [ 95%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[create] PASSED [ 96%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[update] PASSED [ 97%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[comment] PASSED [ 98%]
projects/test_activity.py::test_original_operation_failure_cannot_leave_an_activity PASSED [100%]

------- generated xml file: /tmp/taskboard-activity/backend-results.xml --------
======================== 81 passed in 246.98s (0:04:06) ========================
```


```json
{
  "step": "frontend-tests",
  "exitCode": 0,
  "seconds": 45.98,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text

> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

(node:64415) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
 ✓ src/tests/ExportButton.test.tsx (6 tests) 2903ms
   ✓ <ExportButton /> > allows a project admin to export 1776ms
   ✓ <ExportButton /> > disables duplicate submissions and displays partial export counts and failures 633ms
 ✓ src/tests/TaskComments.test.tsx (12 tests) 5411ms
   ✓ <TaskComments /> > displays server ordering, author, body, and semantic timestamps without edit/delete controls 2331ms
   ✓ <TaskComments /> > allows a project admin to compose 609ms
   ✓ <TaskComments /> > allows a project member to compose 395ms
   ✓ <TaskComments /> > posts only the body, prevents double submissions, and refreshes the chronological thread 720ms
   ✓ <TaskComments /> > preserves a draft and displays the server's permission error 427ms
stderr | src/tests/ProjectActivity.test.tsx > <ProjectActivity /> > mounts on the project page and refreshes after creating a task
⚠️ React Router Future Flag Warning: React Router will begin wrapping state updates in `React.startTransition` in v7. You can use the `v7_startTransition` future flag to opt-in early. For more information, see https://reactrouter.com/v6/upgrading/future#v7_starttransition.
⚠️ React Router Future Flag Warning: Relative route resolution within Splat routes is changing in v7. You can use the `v7_relativeSplatPath` future flag to opt-in early. For more information, see https://reactrouter.com/v6/upgrading/future#v7_relativesplatpath.

 ✓ src/tests/ProjectActivity.test.tsx (9 tests) 5742ms
   ✓ <ProjectActivity /> > shows all event types in server order with actor, details, and semantic time 1935ms
   ✓ <ProjectActivity /> > refreshes the mounted feed when a comment is posted 938ms
   ✓ <ProjectActivity /> > refreshes activity after a task update and preserves the server's nested assignee 1078ms
   ✓ <ProjectActivity /> > mounts on the project page and refreshes after creating a task 942ms
 ✓ src/tests/schemas.test.ts (6 tests) 17ms
 ✓ src/tests/TaskCard.test.tsx (3 tests) 672ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 378ms

 Test Files  5 passed (5)
      Tests  36 passed (36)
   Start at  16:19:55
   Duration  37.94s (transform 1.40s, setup 6.08s, collect 13.20s, tests 14.74s, environment 38.03s, prepare 5.17s)
```


```json
{
  "step": "node-tests",
  "exitCode": 0,
  "seconds": 2.38,
  "networkPolicy": "loopback only for fake SDK HTTP server",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 93.646674
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 1.997582
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 24.094908
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 9.336358
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 31.707219
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 4.218018
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 3.084944
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 0.539431
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 1.879007
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 11.44379
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 1.67144
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 485.659183
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 1787.995424
```


```json
{
  "step": "build",
  "exitCode": 0,
  "seconds": 106.84,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text

> taskboard-frontend@1.0.0 build
> tsc && vite build

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.
vite v5.4.21 building for production...
transforming...
(node:64608) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
✓ 92 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.27 kB
dist/assets/index-xL9mnprx.css   10.62 kB │ gzip:  2.88 kB
dist/assets/index-B563Skf_.js   225.46 kB │ gzip: 69.65 kB
✓ built in 14.00s
```

Initial verification issues, retained rather than hidden: the first full backend run had 78 passes and one failure in existing test_export_task_limit[1000-200], reporting “OperationalError: server closed the connection unexpectedly”. Its log/result/XML are retained privately under /tmp/taskboard-activity/initial-backend-*. The Docker database remained running with OOMKilled=false and RestartCount=0; available logs did not identify the cause. No application code or database service change was made for this issue; the complete backend rerun passed, including the failing test.


```text
Initial backend summary: 1 failed, 78 passed in 304.04s.
Failure: projects/test_export.py::test_export_task_limit[1000-200]
django.db.utils.OperationalError: server closed the connection unexpectedly

Container remains running, OOMKilled=false, RestartCount=0.
.2026-10-15 08:21:42.088 UTC [53] LOG:  database system is ready to accept connections
2026-10-15 08:21:51.838 UTC [1] LOG:  database system is ready to accept connections
```

The first production build also found TS2769 in a new test: Testing Library getByRole does not accept an exact option. Removed that redundant test option and reran the complete frontend suite and production build successfully. The build retains the previously documented non-fatal Vite CJS and typeless PostCSS ESM warnings. No dependencies or PostCSS code were changed for this feature.

The final review added a regression for equivalent assignee UUID formats. Before the fix, its uppercase and hyphenless cases both failed by creating false assignee-change events (one standard-format case passed). The endpoint now compares the saved database UUID and reuses that task for serialization; the complete backend suite, including all three cases, passes.


```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 21 items / 18 deselected / 3 selected

projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[standard] PASSED [ 33%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[uppercase] FAILED [ 66%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[hex] FAILED [100%]

=================================== FAILURES ===================================
_______ test_noop_and_untracked_edits_do_not_create_activity[uppercase] ________
projects/test_activity.py:145: in test_noop_and_untracked_edits_do_not_create_activity
    assert not Activity.objects.exists()
E   assert not True
E    +  where True = exists()
E    +    where exists = <django.db.models.manager.Manager object at 0x10a733140>.exists
E    +      where <django.db.models.manager.Manager object at 0x10a733140> = Activity.objects
__________ test_noop_and_untracked_edits_do_not_create_activity[hex] ___________
projects/test_activity.py:145: in test_noop_and_untracked_edits_do_not_create_activity
    assert not Activity.objects.exists()
E   assert not True
E    +  where True = exists()
E    +    where exists = <django.db.models.manager.Manager object at 0x10a733140>.exists
E    +      where <django.db.models.manager.Manager object at 0x10a733140> = Activity.objects
--------------------------- Captured stderr teardown ---------------------------
Destroying test database for alias 'default'...
=========================== short test summary info ============================
FAILED projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[uppercase]
FAILED projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[hex]
================= 2 failed, 1 passed, 18 deselected in 10.27s ==================
```

#### Seed and existing comment protection

A read-only baseline captured all pre-existing users, projects, memberships, tasks and comments before the feature demo. After the demo, every original row and value, including task timestamps and all four pre-existing audit comments, matched that baseline. Only a new demo project, its three memberships, two tasks, two comments and eight activity rows were added. The baseline is private because it contains user password hashes; only its checksum and counts are recorded here.


```json
{
  "allPreexistingRowsAndCommentsUnchanged": true,
  "baselineCounts": {
    "comments": 4,
    "memberships": 11,
    "projects": 4,
    "tasks": 13,
    "users": 5
  },
  "currentCounts": {
    "users": 5,
    "projects": 5,
    "memberships": 14,
    "tasks": 15,
    "comments": 6
  },
  "baselineSHA256": "6308457a105fc697413f54f395bcea6adade389664b498080dad8b080b865bb4"
}
```

#### Running services and credential checks

http://127.0.0.1:3000 — HTTP 200 (401 is expected without authentication).

http://127.0.0.1:8001/api/projects — HTTP 401 (401 is expected without authentication).

http://127.0.0.1:3000/api/projects — HTTP 401 (401 is expected without authentication).

Both servers remain running on loopback. The verified Node/npm toolchain and existing frontend sandbox were retained; frontend network access remains loopback-only and credential-file reads remain blocked. The backend alone loads the ignored server environment for manual Airtable testing. Automated suites use fake Airtable credentials and block external network calls. The backend was restarted to load the migration/code and again for the final persisted-UUID comparison; both times no active export subprocess was present. No unrelated services were restarted.


```json
{
  "configuredAirtableTokenAbsentFromSourceAssetsAndEvidence": true,
  "configuredBaseIdAbsentFromSourceAssetsAndEvidence": true,
  "apiEvidenceJwtRedacted": true
}
```

Historical terminal evidence remains an unchanged byte prefix. The raw TERMINAL_log.md and REVIEW.md remain local/untracked because historical evidence contains authentication material. The feature commit includes source, migration, tests, README and design_notes.md; it excludes credentials and seed files.

#### Separate Part 3b feature commit

Committed as `88b21fe594a35bb4d73e899bc131484732e37877` (`feat: add transactional project activity feed`). Parent is the separate Part 3a comments commit. Post-commit verification confirms only the 15 feature files were committed, with no configured Airtable credentials, environment files, seed files, or raw historical terminal log.

## 7. Final compliance audit and fresh verification

Audit date: 2026-10-15T11:24:53.108804+00:00. Full requirement mapping and blockers: COMPLIANCE_AUDIT.md. Audit changes documentation only; no application/test/seed edits, no new exports, no commits, no history rewriting, no push, and no service restart. Both existing servers remain available.

### Fresh full test suites and production build

Actual final results: **81 backend + 36 frontend + 12 Airtable SDK = 129 passing tests; zero failures. Production TypeScript/Vite build passed.** Tests used an isolated PostgreSQL test database and fake Airtable credentials. Frontend build/tests had external network and credential-file reads blocked; SDK/Django tests were limited to loopback.

#### cd backend && python -m pytest -v --tb=short


```json
{
  "step": "backend-tests",
  "exitCode": 0,
  "seconds": 237.19,
  "networkPolicy": "loopback only for isolated Django test database",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.settings (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 81 items

projects/test_activity.py::test_all_project_roles_can_read_activity[admin] PASSED [  1%]
projects/test_activity.py::test_all_project_roles_can_read_activity[member] PASSED [  2%]
projects/test_activity.py::test_all_project_roles_can_read_activity[viewer] PASSED [  3%]
projects/test_activity.py::test_feed_requires_membership_and_authentication PASSED [  4%]
projects/test_activity.py::test_feed_is_newest_first_bounded_and_project_isolated PASSED [  6%]
projects/test_activity.py::test_empty_feed_and_no_client_supplied_events PASSED [  7%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[admin] PASSED [  8%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[member] PASSED [  9%]
projects/test_activity.py::test_status_assignment_reassignment_and_unassignment_record_actual_changes PASSED [ 11%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[standard] PASSED [ 12%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[uppercase] PASSED [ 13%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[hex] PASSED [ 14%]
projects/test_activity.py::test_comment_event_preserves_original_comment_and_ignores_forged_actor PASSED [ 16%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[viewer] PASSED [ 17%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[outsider] PASSED [ 18%]
projects/test_activity.py::test_validation_failure_has_no_event_or_partial_update PASSED [ 19%]
projects/test_activity.py::test_activity_task_snapshot_survives_task_deletion PASSED [ 20%]
projects/test_comments.py::test_project_roles_can_read_comments[admin] PASSED [ 22%]
projects/test_comments.py::test_project_roles_can_read_comments[member] PASSED [ 23%]
projects/test_comments.py::test_project_roles_can_read_comments[viewer] PASSED [ 24%]
projects/test_comments.py::test_only_admins_and_members_can_post[admin-201] PASSED [ 25%]
projects/test_comments.py::test_only_admins_and_members_can_post[member-201] PASSED [ 27%]
projects/test_comments.py::test_only_admins_and_members_can_post[viewer-403] PASSED [ 28%]
projects/test_comments.py::test_only_admins_and_members_can_post[outsider-403] PASSED [ 29%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[get] PASSED [ 30%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[post] PASSED [ 32%]
projects/test_comments.py::test_comments_are_chronological_and_scoped_to_task_and_project PASSED [ 33%]
projects/test_comments.py::test_post_cannot_forge_identity_time_or_replace_an_existing_comment PASSED [ 34%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[admin] PASSED [ 35%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[member] PASSED [ 37%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[viewer] PASSED [ 38%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[task] PASSED [ 39%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[project] PASSED [ 40%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[empty] PASSED [ 41%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[whitespace] PASSED [ 43%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[null] PASSED [ 44%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[too-long] PASSED [ 45%]
projects/test_comments.py::test_missing_task_returns_not_found PASSED    [ 46%]
projects/test_export.py::test_export_requires_server_configuration PASSED [ 48%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [ 49%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [ 50%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 51%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 53%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 54%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 55%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 56%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 58%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 59%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 60%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 61%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 62%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 64%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 65%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 66%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 67%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 69%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 70%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 71%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 72%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 74%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 75%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 76%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 77%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 79%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 80%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 81%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 82%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 83%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 85%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 86%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 87%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 88%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 90%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 91%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 92%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 93%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [ 95%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[create] PASSED [ 96%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[update] PASSED [ 97%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[comment] PASSED [ 98%]
projects/test_activity.py::test_original_operation_failure_cannot_leave_an_activity PASSED [100%]

------ generated xml file: /tmp/taskboard-final-audit/backend-results.xml ------
======================== 81 passed in 228.99s (0:03:48) ========================
```

#### cd frontend && npm test


```json
{
  "step": "frontend-tests",
  "exitCode": 0,
  "seconds": 42.74,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text

> taskboard-frontend@1.0.0 test
> vitest run

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.9 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

(node:66689) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
 ✓ src/tests/ExportButton.test.tsx (6 tests) 5172ms
   ✓ <ExportButton /> > allows a project admin to export 2923ms
   ✓ <ExportButton /> > disables duplicate submissions and displays partial export counts and failures 1532ms
   ✓ <ExportButton /> > shows a server error and allows the user to try again 429ms
stderr | src/tests/ProjectActivity.test.tsx > <ProjectActivity /> > mounts on the project page and refreshes after creating a task
⚠️ React Router Future Flag Warning: React Router will begin wrapping state updates in `React.startTransition` in v7. You can use the `v7_startTransition` future flag to opt-in early. For more information, see https://reactrouter.com/v6/upgrading/future#v7_starttransition.
⚠️ React Router Future Flag Warning: Relative route resolution within Splat routes is changing in v7. You can use the `v7_relativeSplatPath` future flag to opt-in early. For more information, see https://reactrouter.com/v6/upgrading/future#v7_relativesplatpath.

 ✓ src/tests/ProjectActivity.test.tsx (9 tests) 8159ms
   ✓ <ProjectActivity /> > shows all event types in server order with actor, details, and semantic time 3650ms
   ✓ <ProjectActivity /> > shows a loading state then an empty feed 304ms
   ✓ <ProjectActivity /> > refreshes the mounted feed when a comment is posted 1624ms
   ✓ <ProjectActivity /> > refreshes activity after a task update and preserves the server's nested assignee 1102ms
   ✓ <ProjectActivity /> > mounts on the project page and refreshes after creating a task 936ms
 ✓ src/tests/TaskComments.test.tsx (12 tests) 9486ms
   ✓ <TaskComments /> > displays server ordering, author, body, and semantic timestamps without edit/delete controls 4904ms
   ✓ <TaskComments /> > allows a project admin to compose 729ms
   ✓ <TaskComments /> > allows a project member to compose 721ms
   ✓ <TaskComments /> > keeps role viewer read-only 629ms
   ✓ <TaskComments /> > posts only the body, prevents double submissions, and refreshes the chronological thread 1270ms
   ✓ <TaskComments /> > preserves a draft and displays the server's permission error 677ms
   ✓ <TaskComments /> > mounts in the existing task dialog and derives the comment role from project membership 410ms
 ✓ src/tests/schemas.test.ts (6 tests) 206ms
 ✓ src/tests/TaskCard.test.tsx (3 tests) 782ms
   ✓ <TaskCard /> > renders the task title and assignee 372ms
   ✓ <TaskCard /> > invokes onClick with the task when clicked 383ms

 Test Files  5 passed (5)
      Tests  36 passed (36)
   Start at  16:41:18
   Duration  34.91s (transform 1.09s, setup 4.51s, collect 12.21s, tests 23.81s, environment 28.05s, prepare 4.12s)
```

#### cd backend/airtable && node --test


```json
{
  "step": "node-tests",
  "exitCode": 0,
  "seconds": 3.25,
  "networkPolicy": "loopback only for fake SDK HTTP server",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 8.949557
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 6.926535
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 0.824866
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 3.884393
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 50.009967
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 17.32813
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 0.807117
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 1.318175
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 2.923734
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 4.27862
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 1.257087
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 547.596267
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2685.278864
```

#### cd frontend && npm run build


```json
{
  "step": "build",
  "exitCode": 0,
  "seconds": 84.42,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```text

> taskboard-frontend@1.0.0 build
> tsc && vite build

The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.
vite v5.4.21 building for production...
transforming...
(node:66815) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/postcss.config.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
✓ 92 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.27 kB
dist/assets/index-xL9mnprx.css   10.62 kB │ gzip:  2.88 kB
dist/assets/index-B563Skf_.js   225.46 kB │ gzip: 69.65 kB
✓ built in 12.60s
```

Existing non-fatal Vite CJS/ESM-package warnings remain. Earlier genuine failures, including the transient PostgreSQL disconnect in a prior activity-stage full suite and the UUID regression red test, remain in their historical sections above; they are not current failures.

### Database migration and deployment checks


```json
{
  "command": "python manage.py showmigrations",
  "exitCode": 0
}
```


```text
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
projects
 [X] 0001_initial
 [X] 0002_comment
 [X] 0003_activity
users
 [X] 0001_initial
```


```json
{
  "command": "python manage.py migrate --check",
  "exitCode": 0
}
```


```text
[No output; exit status 0.]
```


```json
{
  "command": "python manage.py makemigrations --check --dry-run",
  "exitCode": 0
}
```


```text
No changes detected
```


```json
{
  "command": "python manage.py check",
  "exitCode": 0
}
```


```text
System check identified no issues (0 silenced).
```


```json
{
  "command": "python manage.py check --deploy",
  "exitCode": 0
}
```


```text
System check identified some issues:

WARNINGS:
?: (security.W001) You do not have 'django.middleware.security.SecurityMiddleware' in your MIDDLEWARE so the SECURE_HSTS_SECONDS, SECURE_CONTENT_TYPE_NOSNIFF, SECURE_REFERRER_POLICY, SECURE_CROSS_ORIGIN_OPENER_POLICY, and SECURE_SSL_REDIRECT settings will have no effect.
?: (security.W002) You do not have 'django.middleware.clickjacking.XFrameOptionsMiddleware' in your MIDDLEWARE, so your pages will not be served with an 'x-frame-options' header. Unless there is a good reason for your site to be served in a frame, you should consider enabling this header to help prevent clickjacking attacks.
?: (security.W003) You don't appear to be using Django's built-in cross-site request forgery protection via the middleware ('django.middleware.csrf.CsrfViewMiddleware' is not in your MIDDLEWARE). Enabling the middleware is the safest approach to ensure you don't leave any holes.
?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.
?: (security.W018) You should not have DEBUG set to True in deployment.

System check identified 5 issues (0 silenced).
```

All migrations are applied and models match checked-in migrations; normal Django check has no issues. Deployment check returns five warnings on local default settings. Those warnings are not counted as failing tests or five independently reproduced vulnerabilities.

### Seed and existing audit comments


```json
{
  "originalSeedRowsUnchangedByTable": {
    "memberships": true,
    "projects": true,
    "tasks": true,
    "users": true
  },
  "originalSeedCounts": {
    "memberships": 8,
    "projects": 3,
    "tasks": 12,
    "users": 5
  },
  "allOriginalSeedRowsUnchanged": true,
  "preexistingAuditCommentsUnchanged": true,
  "preexistingAuditCommentCount": 4,
  "currentCounts": {
    "users": 5,
    "projects": 5,
    "memberships": 14,
    "tasks": 15,
    "comments": 6,
    "activities": 8
  },
  "verifiedAtUTC": "2026-10-15T11:14:56.332207+00:00"
}
```

Original seed counts are 5 users, 3 projects, 8 memberships and 12 tasks. Current totals include separate demo data; seed rows were compared by ID and every value, not by requiring total counts to remain at seed-only values. Seed source/initial migrations are unchanged. All four pre-existing audit comments match their retained baseline.

### Remaining security issues and exact read-only proof


```json
{
  "publicDefaultSigningKeyConfigured": true,
  "unauthenticatedControlStatus": 401,
  "request": "GET /api/users/me; Authorization: Bearer <REDACTED_LOCALLY_FORGED_JWT>",
  "forgedTokenRequestStatus": 200,
  "responseBody": {
    "user": {
      "id": "89e883cc-17b4-46fd-9828-b10243d1c8e2",
      "email": "meera@taskboard.dev",
      "name": "Meera Iyer"
    }
  },
  "usedLoginEndpoint": false,
  "databaseWrites": false
}
```

The live instance accepted a short-lived JWT signed with the public development key, without login. The token/key value is omitted, no token was saved to evidence, and no database write was performed. This confirms a default-configuration authentication weakness; it is not a claim about a deployment with a unique signing key. No fix/configuration change was made. See security_notes.md for remediation and other incident follow-up.


```json
{
  "step": "audit",
  "exitCode": 1,
  "seconds": 30.96,
  "networkPolicy": "official registry audit endpoint; lifecycle scripts disabled",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```json
{
  "project": "frontend",
  "registryVulnerabilityCounts": {
    "info": 0,
    "low": 0,
    "moderate": 7,
    "high": 6,
    "critical": 2,
    "total": 15
  }
}
```


```json
{
  "step": "airtable-audit",
  "exitCode": 0,
  "seconds": 9.62,
  "networkPolicy": "official registry audit endpoint; lifecycle scripts disabled",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```


```json
{
  "project": "backend/airtable",
  "registryVulnerabilityCounts": {
    "info": 0,
    "low": 0,
    "moderate": 0,
    "high": 0,
    "critical": 0,
    "total": 0
  }
}
```

Frontend audit exited 1 with 15 affected dependency entries (2 critical, 6 high, 7 moderate); the Airtable project audit exited 0 with none. These are registry reports; application exploitability was not independently demonstrated for every entry. Maintainer advisories and conditions are linked in security_notes.md. Full audit JSON is retained privately. Credential rotation, other-account/session review and workstation eradication are not verified complete.

### Git history, credentials and submission status


```json
{
  "reachableGitObjectsScanned": 174,
  "configuredAirtableTokenOrBaseIdFound": false,
  "envFilesIgnored": {
    ".env": true,
    ".env.example": true
  },
  "envFilesTracked": false,
  "rootEnvMode": "0o600",
  "seedSourceAndInitialMigrationsUnchanged": true,
  "coreHooksPathConfigured": false,
  "head": "88b21fe594a35bb4d73e899bc131484732e37877",
  "historyRewrittenOrPushedDuringAudit": false
}
```


```text
88b21fe feat: add transactional project activity feed
21988bd feat: add append-only task comments with project permissions
1c87642 fix(security): remove injected PostCSS remote-code loader
75e6d4a feat: export project tasks to Airtable with idempotent batching
70f2bd9 fix: parameterize task search to prevent SQL injection
5f58e52 remove ASSIGNMENT.md
84cb1a6 fix: use API_TARGET env var for Vite proxy so Docker networking works
32caa63 Initial commit
```

The five implementation/security commits remain separate. The history still contains the malicious older PostCSS revision; do not execute it. The original brief is read using git show only. No squash, reset, amend, merge, commit, remote upload or push was performed by this audit.

README, REVIEW, design_notes and security_notes were checked/updated. README now includes explicit setup/test/environment instructions, seed cautions, source map, current inspection ports, SDK override, hook-capture limitations, and placeholders for the actual recording and Airtable visual proof. Final docs are deliberately uncommitted for review; REVIEW.md, TERMINAL_LOG.md and COMPLIANCE_AUDIT.md must still be included in a later authorized documentation commit before submission.

**Submission blockers:** actual screen recording URL; actual Airtable screenshot/share link; absent original setup and initial-test transcripts; final documentation not committed. **Acceptance/timing concerns recorded at this historical checkpoint:** a mistaken npm/Python rubric comparison (corrected after reading the supplied original; official npm is required); original 90–100 minute timebox cannot be attested (retained review-to-activity timeline exceeds it), 24-hour receipt/deadline unknown, no configured/captured AI-conversation hook output. **Security blockers for a trusted deployment:** known signing-key forgery, dependency advisories, unverified credential rotation/host remediation, insecure development defaults and damaged global npm. No missing evidence or remediation is marked complete.

### Final artifact and worktree validation

The audit compared every live application row before/after its read-only checks; users, projects, memberships, tasks, comments and activities are identical. No live data was changed. All final document file links resolve; configured Airtable token/base ID and complete/fragmented JWT prefixes are absent from the inspected submission documents and production assets.

```json
{
  "allLiveRowsIncludingSeedCommentsAndActivityUnchangedDuringAudit": true,
  "canonicalSHA256": "b446deeecdb099ed66ab5cd766a2cecbfae36c0bc902d28320b82265011e7e07"
}
```

```json
{
  "testCounts": {
    "backend": 81,
    "frontend": 36,
    "airtableSDK": 12,
    "total": 129
  },
  "buildPassed": true,
  "migrationsAppliedAndNoModelDrift": true,
  "logRequiredOrderVerified": true,
  "documentLinksResolve": true,
  "credentialsAbsentFromInspectedDocsAndAssets": true,
  "completeOrFragmentedJwtPrefixesInFinalLog": 0,
  "applicationTestsAndSeedSourceUnmodified": true,
  "headUnchanged": "88b21fe",
  "commitsCreatedOrPushedByAudit": 0
}
```

Actual final git status (documentation changes only; HEAD unchanged):

```text
 M README.md
 M design_notes.md
 M security_notes.md
?? COMPLIANCE_AUDIT.md
?? REVIEW.md
?? TERMINAL_LOG.md
```

No commit, squash, history rewrite or push was performed. Both existing loopback services remain running. The missing recording/Airtable visual proof/initial transcripts, pending documentation commit, then-reported SDK/timing concerns and open security issues (the SDK concern was subsequently invalidated by the supplied original) are intentionally reported as incomplete.

### Subsequent prioritized security remediation and final verification

Verified on 2026-10-15T11:53:32.337073+00:00. Source commits: `b5a444b` (JWT/configuration) and `e480e07` (dependencies). This later work was explicitly authorized after the preceding audit. No seed command, infected historical code, real Airtable request, history rewrite or push was performed.

#### JWT root cause, identical curl proof, and key rotation

SimpleJWT inherited the public Django fallback key; Compose also supplied a public key. Settings now refuse missing/weak/development keys, Compose requires a configured private key, and the ignored local server key was rotated using `python3 bin/generate-signing-key --rotate`. The helper printed only a status message and preserved other environment settings. Existing login sessions were invalidated; there is no old-key fallback. The Airtable credential was left unchanged.

The actual process invocation was `curl --config -`, with the following configuration passed on stdin both times. Only the Authorization value is redacted; no token/key value was printed or retained:

```text
url = "http://127.0.0.1:8001/api/users/me"
silent
show-error
include
max-time = 15
header = "Authorization: Bearer <REDACTED_FORGED_JWT>"
```

Before — actual captured complete HTTP response:

```http
HTTP/1.1 200 OK
Date: Thu, 15 Oct 2026 11:40:01 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
Content-Length: 104

{"user":{"id":"89e883cc-17b4-46fd-9828-b10243d1c8e2","email":"meera@taskboard.dev","name":"Meera Iyer"}}
```

After — actual captured complete HTTP response:

```http
HTTP/1.1 401 Unauthorized
Date: Thu, 15 Oct 2026 11:40:08 GMT
Server: WSGIServer/0.2 CPython/3.12.11
Content-Type: application/json
WWW-Authenticate: Bearer realm="api"
Vary: Accept, origin
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 172
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is invalid"}]}
```

The same short-lived JWT remained valid in time during the seven-second comparison; rejection was caused by signature/key rotation, not expiration. Both old public keys are rejected. Fresh login and authenticated GET each return 200.

```json
{
  "exactRequestSha256Before": "ab3699060eee785c11ac373e323b16425092fbaff7183af2efaca85c7aeac9e4",
  "exactRequestSha256After": "ab3699060eee785c11ac373e323b16425092fbaff7183af2efaca85c7aeac9e4",
  "sameForgedRequestReused": true,
  "otherPublicKeyRejected": true,
  "freshLoginStatus": 200,
  "keyValueOrTokensSaved": false,
  "realExportsPausedPendingManualTokenRotation": true
}
```

Production configuration now rejects debug mode, wildcard/missing hosts and weak database passwords. Security/CSRF/frame middleware, restricted CORS and production transport settings are enabled. `taskboard.testing` disables dotenv and uses temporary secrets for tests. These changes do not verify actual production infrastructure or host trust.

#### Dependency changes and setup issues

Frontend: Vite 6.4.4, Vitest 4.1.11, Router DOM 7.18.4 (React retained at 18.3.1), Tailwind/PostCSS plugin 4.3.3; plugin-react 4.7.0. ESM configuration and legacy theme loading preserve the existing UI; button cursors are preserved. Both Docker Node stages use Node 22; a fresh image build was not performed. Python pytest changed from 8.4.2 to 9.1.1 to resolve the temporary-directory advisory (fixed upstream from 9.0.3).

Three npm 10.9.3 resolution attempts (existing tree, clean tree, fresh lock) failed with the same internal peer-resolver error. The affected dependency tree/old lock were retained privately. No --force or incompatible transitive override was used. Representative actual output:

```text
npm error Cannot read properties of null (reading 'edgesOut')
npm error A complete log of this run can be found in: /tmp/taskboard-hardening/npm-cache/_logs/2026-10-15T11_45_36_739Z-debug-0.log
```

An npm 11.6.4 archive from the official registry was verified before execution; its engine range supports the verified Node 22.20.0 runtime. The successful dependency install used `npm install --ignore-scripts --no-audit --no-fund` with the verified CLI and a minimal environment. The lock contains 267 registry packages, all with integrity fields. Actual successful output:

```text
npm warn deprecated whatwg-encoding@3.1.1: Use @exodus/bytes instead for a more spec-conformant and faster implementation

added 196 packages in 50s
```

The virtualenv has no pip. Actual attempted `python -m pip install` output:

```text
/Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python: No module named pip
```

Recovery used `uv pip install --python .venv/bin/python --index-url https://pypi.org/simple "pytest>=9.0.3,<10.0"`. Actual output:

```text
Resolved 5 packages in 629ms
Prepared 1 package in 168ms
Uninstalled 1 package in 102ms
Installed 1 package in 18ms
 - pytest==8.4.2
 + pytest==9.1.1
```

Bare `docker compose config --quiet` initially refused startup configuration because this manual inspection instance has no POSTGRES_USER/DB/password in root dotenv; its live backend uses separate local DB overrides. With temporary non-secret database settings, Compose validation exited 0 without printing expanded credentials. README now requires explicit database configuration for a fresh Docker stack. No Compose stack or database volume was reset.

#### Complete final suites and production build

Commands below ran through the verified runner. Frontend build/tests cannot read root `.env` and have no networking; backend/SDK tests allow only loopback for the isolated PostgreSQL test database and local fake SDK HTTP server. No actual Airtable credentials are passed. Existing test assertions were retained. The sole backend warning intentionally constructs a token using a weak historical public key to verify rejection.

Command: `cd backend && python -m pytest -v --tb=short`

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-9.1.1, pluggy-1.6.0 -- /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/bin/python
cachedir: .pytest_cache
django: version: 5.2.18, settings: taskboard.testing (from ini)
rootdir: /Users/nitingupta/Desktop/taskboard/q-taskboard/backend
configfile: pytest.ini
plugins: django-4.14.0
collecting ... collected 98 items

projects/test_activity.py::test_all_project_roles_can_read_activity[admin] PASSED [  1%]
projects/test_activity.py::test_all_project_roles_can_read_activity[member] PASSED [  2%]
projects/test_activity.py::test_all_project_roles_can_read_activity[viewer] PASSED [  3%]
projects/test_activity.py::test_feed_requires_membership_and_authentication PASSED [  4%]
projects/test_activity.py::test_feed_is_newest_first_bounded_and_project_isolated PASSED [  5%]
projects/test_activity.py::test_empty_feed_and_no_client_supplied_events PASSED [  6%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[admin] PASSED [  7%]
projects/test_activity.py::test_task_creation_records_server_actor_and_initial_state[member] PASSED [  8%]
projects/test_activity.py::test_status_assignment_reassignment_and_unassignment_record_actual_changes PASSED [  9%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[standard] PASSED [ 10%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[uppercase] PASSED [ 11%]
projects/test_activity.py::test_noop_and_untracked_edits_do_not_create_activity[hex] PASSED [ 12%]
projects/test_activity.py::test_comment_event_preserves_original_comment_and_ignores_forged_actor PASSED [ 13%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[viewer] PASSED [ 14%]
projects/test_activity.py::test_forbidden_writes_do_not_change_tasks_comments_or_feed[outsider] PASSED [ 15%]
projects/test_activity.py::test_validation_failure_has_no_event_or_partial_update PASSED [ 16%]
projects/test_activity.py::test_activity_task_snapshot_survives_task_deletion PASSED [ 17%]
projects/test_comments.py::test_project_roles_can_read_comments[admin] PASSED [ 18%]
projects/test_comments.py::test_project_roles_can_read_comments[member] PASSED [ 19%]
projects/test_comments.py::test_project_roles_can_read_comments[viewer] PASSED [ 20%]
projects/test_comments.py::test_only_admins_and_members_can_post[admin-201] PASSED [ 21%]
projects/test_comments.py::test_only_admins_and_members_can_post[member-201] PASSED [ 22%]
projects/test_comments.py::test_only_admins_and_members_can_post[viewer-403] PASSED [ 23%]
projects/test_comments.py::test_only_admins_and_members_can_post[outsider-403] PASSED [ 24%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[get] PASSED [ 25%]
projects/test_comments.py::test_non_members_and_anonymous_cannot_access_a_thread[post] PASSED [ 26%]
projects/test_comments.py::test_comments_are_chronological_and_scoped_to_task_and_project PASSED [ 27%]
projects/test_comments.py::test_post_cannot_forge_identity_time_or_replace_an_existing_comment PASSED [ 28%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[admin] PASSED [ 29%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[member] PASSED [ 30%]
projects/test_comments.py::test_comments_cannot_be_edited_or_deleted[viewer] PASSED [ 31%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[task] PASSED [ 32%]
projects/test_comments.py::test_deleting_parents_cannot_remove_comment_history[project] PASSED [ 33%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[empty] PASSED [ 34%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[whitespace] PASSED [ 35%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[null] PASSED [ 36%]
projects/test_comments.py::test_invalid_comment_bodies_are_rejected[too-long] PASSED [ 37%]
projects/test_comments.py::test_missing_task_returns_not_found PASSED    [ 38%]
projects/test_export.py::test_export_requires_server_configuration PASSED [ 39%]
projects/test_export.py::test_export_authorization[admin-200] PASSED     [ 40%]
projects/test_export.py::test_export_authorization[member-200] PASSED    [ 41%]
projects/test_export.py::test_export_authorization[viewer-403] PASSED    [ 42%]
projects/test_export.py::test_export_authorization[None-403] PASSED      [ 43%]
projects/test_export.py::test_export_requires_authentication PASSED      [ 44%]
projects/test_export.py::test_export_uses_server_tasks_only_and_returns_partial_results PASSED [ 45%]
projects/test_export.py::test_export_task_limit[1000-200] PASSED         [ 46%]
projects/test_export.py::test_export_task_limit[1001-400] PASSED         [ 47%]
projects/test_export.py::test_node_failure_does_not_expose_credentials PASSED [ 48%]
projects/tests.py::TestProjects::test_create_project PASSED              [ 50%]
projects/tests.py::TestProjects::test_list_only_returns_member_projects PASSED [ 51%]
projects/tests.py::TestProjects::test_get_project_detail PASSED          [ 52%]
projects/tests.py::TestProjects::test_non_member_cannot_view_project PASSED [ 53%]
projects/tests.py::TestTasks::test_create_task PASSED                    [ 54%]
projects/tests.py::TestTasks::test_viewers_cannot_create_tasks PASSED    [ 55%]
projects/tests.py::TestTasks::test_delete_task_requires_membership PASSED [ 56%]
projects/tests.py::TestTaskSearch::test_sql_injection_does_not_return_other_projects_tasks PASSED [ 57%]
projects/tests.py::TestTaskSearch::test_search_matches_sql_shaped_text_literally PASSED [ 58%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[ANALYTICS-analytics] PASSED [ 59%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[launch-release] PASSED [ 60%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[customer's-feedback] PASSED [ 61%]
projects/tests.py::TestTaskSearch::test_normal_searches_only_match_tasks_in_the_project[no matching task-None] PASSED [ 62%]
projects/tests.py::TestTaskSearch::test_search_results_keep_position_order_across_statuses PASSED [ 63%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[%] PASSED [ 64%]
projects/tests.py::TestTaskSearch::test_search_preserves_like_wildcards[_] PASSED [ 65%]
projects/tests.py::TestTaskSearch::test_search_keeps_existing_response_fields PASSED [ 66%]
projects/tests.py::TestTaskSearch::test_empty_query_keeps_existing_non_search_behavior PASSED [ 67%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[Analytics] PASSED [ 68%]
projects/tests.py::TestTaskSearch::test_non_member_cannot_search_a_project[') OR TRUE -- ] PASSED [ 69%]
projects/tests.py::TestTaskSearch::test_search_requires_authentication PASSED [ 70%]
users/test_security.py::test_tokens_signed_with_public_development_keys_cannot_impersonate_a_user[<REDACTED_HISTORICAL_PUBLIC_KEY>] PASSED [ 71%]
users/test_security.py::test_tokens_signed_with_public_development_keys_cannot_impersonate_a_user[<REDACTED_HISTORICAL_PUBLIC_KEY>] PASSED [ 72%]
users/test_security.py::test_login_still_issues_a_valid_token_and_security_headers PASSED [ 73%]
users/tests.py::TestRegister::test_creates_user_and_returns_token PASSED [ 74%]
users/tests.py::TestRegister::test_rejects_short_password PASSED         [ 75%]
users/tests.py::TestRegister::test_rejects_duplicate_email PASSED        [ 76%]
users/tests.py::TestRegister::test_rejects_missing_name PASSED           [ 77%]
users/tests.py::TestLogin::test_returns_token_on_valid_credentials PASSED [ 78%]
users/tests.py::TestLogin::test_rejects_wrong_password PASSED            [ 79%]
users/tests.py::TestLogin::test_rejects_missing_email PASSED             [ 80%]
users/tests.py::TestLogin::test_rejects_unknown_email PASSED             [ 81%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[create] PASSED [ 82%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[update] PASSED [ 83%]
projects/test_activity.py::test_activity_write_failure_rolls_back_entire_operation[comment] PASSED [ 84%]
projects/test_activity.py::test_original_operation_failure_cannot_leave_an_activity PASSED [ 85%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[None] PASSED [ 86%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[] PASSED [ 87%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[<REDACTED_HISTORICAL_PUBLIC_KEY>] PASSED [ 88%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[<REDACTED_HISTORICAL_PUBLIC_KEY>] PASSED [ 89%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx] PASSED [ 90%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[django-insecure-aB0123xyzaB0123xyzaB0123xyzaB0123xyzaB0123xyzaB0123xyzaB0123xyzaB0123xyz] PASSED [ 91%]
users/test_security.py::test_missing_weak_or_development_keys_prevent_startup[<unique-long-random-server-secret><unique-long-random-server-secret><unique-long-random-server-secret>] PASSED [ 92%]
users/test_security.py::test_safe_local_defaults_and_explicit_jwt_signing_key PASSED [ 93%]
users/test_security.py::test_production_rejects_unsafe_configuration[overrides0] PASSED [ 94%]
users/test_security.py::test_production_rejects_unsafe_configuration[overrides1] PASSED [ 95%]
users/test_security.py::test_production_rejects_unsafe_configuration[overrides2] PASSED [ 96%]
users/test_security.py::test_production_rejects_unsafe_configuration[overrides3] PASSED [ 97%]
users/test_security.py::test_production_configuration_requires_explicit_hosts_and_secures_transport PASSED [ 98%]
users/test_security.py::test_key_provisioning_is_private_preserves_other_credentials_and_rotates_only_explicitly PASSED [100%]

=============================== warnings summary ===============================
users/test_security.py::test_tokens_signed_with_public_development_keys_cannot_impersonate_a_user[<REDACTED_HISTORICAL_PUBLIC_KEY>]
  /Users/nitingupta/Desktop/taskboard/q-taskboard/.venv/lib/python3.12/site-packages/jwt/api_jwt.py:149: InsecureKeyLengthWarning: The HMAC key is 20 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
    return self._jws.encode(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
------- generated xml file: /tmp/taskboard-hardening/backend-results.xml -------
================== 98 passed, 1 warning in 222.11s (0:03:42) ===================
```

Runner result:

```json
{
  "step": "backend-tests",
  "exitCode": 0,
  "seconds": 229.47,
  "networkPolicy": "loopback only for isolated Django test database",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```

Command: `cd frontend && npm test`

```text

> taskboard-frontend@1.0.0 test
> vitest run


 RUN  v4.1.11 /Users/nitingupta/Desktop/taskboard/q-taskboard/frontend

 ✓ src/tests/ExportButton.test.tsx (6 tests) 2015ms
     ✓ allows a project admin to export  1309ms
     ✓ disables duplicate submissions and displays partial export counts and failures  530ms
 ✓ src/tests/TaskComments.test.tsx (12 tests) 4876ms
     ✓ displays server ordering, author, body, and semantic timestamps without edit/delete controls  1951ms
     ✓ allows a project admin to compose  524ms
     ✓ posts only the body, prevents double submissions, and refreshes the chronological thread  908ms
     ✓ preserves a draft and displays the server's permission error  344ms
 ✓ src/tests/ProjectActivity.test.tsx (9 tests) 5200ms
     ✓ shows all event types in server order with actor, details, and semantic time  1904ms
     ✓ does not reuse a previous user's cached feed  417ms
     ✓ refreshes the mounted feed when a comment is posted  829ms
     ✓ refreshes activity after a task update and preserves the server's nested assignee  813ms
     ✓ mounts on the project page and refreshes after creating a task  655ms
 ✓ src/tests/schemas.test.ts (6 tests) 265ms
 ✓ src/tests/TaskCard.test.tsx (3 tests) 563ms
     ✓ invokes onClick with the task when clicked  402ms

 Test Files  5 passed (5)
      Tests  36 passed (36)
   Start at  17:18:40
   Duration  27.21s (transform 1.90s, setup 5.12s, import 9.31s, tests 12.92s, environment 30.21s)
```

Runner result:

```json
{
  "step": "frontend-tests",
  "exitCode": 0,
  "seconds": 34.74,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```

Command: `cd backend/airtable && node --test`

```text
TAP version 13
# Subtest: repeated exports upsert by stable task ID without duplicate records
ok 1 - repeated exports upsert by stable task ID without duplicate records
  ---
  duration_ms: 9.667814
  type: 'test'
  ...
# Subtest: retries transient failures with bounded exponential backoff
ok 2 - retries transient failures with bounded exponential backoff
  ---
  duration_ms: 0.915164
  type: 'test'
  ...
# Subtest: permanent authentication failures are not retried or exposed
ok 3 - permanent authentication failures are not retried or exposed
  ---
  duration_ms: 0.814476
  type: 'test'
  ...
# Subtest: isolates a rejected record and continues with the rest of every batch
ok 4 - isolates a rejected record and continues with the rest of every batch
  ---
  duration_ms: 4.138597
  type: 'test'
  ...
# Subtest: exports 1000 tasks in ten-record batches and follows all read pages
ok 5 - exports 1000 tasks in ten-record batches and follows all read pages
  ---
  duration_ms: 178.648746
  type: 'test'
  ...
# Subtest: an ambiguous network failure after a committed write cannot create duplicates
ok 6 - an ambiguous network failure after a committed write cannot create duplicates
  ---
  duration_ms: 1.481745
  type: 'test'
  ...
# Subtest: rate limits back off for 30 then 60 seconds and stop after three attempts
ok 7 - rate limits back off for 30 then 60 seconds and stop after three attempts
  ---
  duration_ms: 6.847026
  type: 'test'
  ...
# Subtest: a permanent monthly billing limit is never retried
ok 8 - a permanent monthly billing limit is never retried
  ---
  duration_ms: 0.444976
  type: 'test'
  ...
# Subtest: exhausting one batch of transient errors still exports later batches
ok 9 - exhausting one batch of transient errors still exports later batches
  ---
  duration_ms: 1.271144
  type: 'test'
  ...
# Subtest: the total duration budget returns partial results instead of retrying forever
ok 10 - the total duration budget returns partial results instead of retrying forever
  ---
  duration_ms: 6.790121
  type: 'test'
  ...
# Subtest: existing duplicate Task IDs fail only that task without adding another copy
ok 11 - existing duplicate Task IDs fail only that task without adding another copy
  ---
  duration_ms: 1.852787
  type: 'test'
  ...
# Subtest: official Airtable SDK sends the upsert payload and does not secretly retry 429s
ok 12 - official Airtable SDK sends the upsert payload and does not secretly retry 429s
  ---
  duration_ms: 435.061796
  type: 'test'
  ...
1..12
# tests 12
# suites 0
# pass 12
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2067.194896
```

Runner result:

```json
{
  "step": "node-tests",
  "exitCode": 0,
  "seconds": 2.42,
  "networkPolicy": "loopback only for fake SDK HTTP server",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```

Command: `cd frontend && npm run build`

```text

> taskboard-frontend@1.0.0 build
> tsc && vite build

vite v6.4.4 building for production...
transforming...
✓ 97 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.27 kB
dist/assets/index-62D8yOIc.css   12.14 kB │ gzip:  3.43 kB
dist/assets/index-Drc9a0uY.js   244.68 kB │ gzip: 76.54 kB
✓ built in 8.30s
```

Runner result:

```json
{
  "step": "build",
  "exitCode": 0,
  "seconds": 67.98,
  "networkPolicy": "blocked",
  "actualAirtableCredentialsPassed": false,
  "affectedServicesRestarted": false
}
```

Final result: **146 passing, zero failing: 98 backend + 36 frontend + 12 SDK.** TypeScript and Vite production build pass, with no previous CJS/module-type warnings.

#### Deployment settings, migrations and advisory checks

Command: `python manage.py check --deploy --fail-level WARNING (DJANGO_ENV=production; disposable private configuration)` — exit 0.

```text
System check identified no issues (0 silenced).
```

Command: `python manage.py showmigrations` — exit 0.

```text
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
projects
 [X] 0001_initial
 [X] 0002_comment
 [X] 0003_activity
users
 [X] 0001_initial
```

Command: `python manage.py migrate --check` — exit 0.

```text
(no output)
```

Command: `python manage.py makemigrations --check --dry-run` — exit 0.

```text
No changes detected
```

Command: `cd frontend && npm audit --json --ignore-scripts`

```json
{
  "project": "frontend",
  "exitCode": 0,
  "vulnerabilities": {
    "info": 0,
    "low": 0,
    "moderate": 0,
    "high": 0,
    "critical": 0,
    "total": 0
  }
}
```

Command: `cd backend/airtable && npm audit --json --ignore-scripts`

```json
{
  "project": "backend/airtable",
  "exitCode": 0,
  "vulnerabilities": {
    "info": 0,
    "low": 0,
    "moderate": 0,
    "high": 0,
    "critical": 0,
    "total": 0
  }
}
```

OSV batch query before/after used installed Python distribution names/versions only, never environment values. The before report had two advisory aliases for one pytest issue; after upgrading, all 27 distributions have no known findings. Actual final summary:

```json
{
  "database": "OSV",
  "packagesChecked": 27,
  "findings": []
}
```

#### Live UI/API, real-export evidence and seed integrity

Read-only browser navigation after the upgrade showed the project board, export button and eight newest-first activity entries. Before/after screenshots were captured and visually inspected outside Git; colors/layout were preserved with no horizontal overflow. Opening the task showed its existing comment and Arjun assignment. No Save/post/export button was submitted. Browser command syntax initially caused an automation-only error (`{} is not iterable`); direct supported navigation/screenshot commands succeeded. No application failure was inferred from that tooling error.

Actual rendered DOM observations:

```json
{"path":"/projects/d3e76a9c-3a56-4eaa-8446-72444b287b4d","activityCount":8,"activityText":"recent activity\n\nMeera Iyer added a comment\n\nUI activity demonstration\n\nUI demo: project feed refreshes after a comment.\n\n15/10/2026, 16:22:26\n\nMeera Iyer changed assignee from unassigned to Arjun Rao\n\nUI activity demonstration\n\n15/10/2026, 16:21:36\n\nMeera Iyer changed status from To do to In review\n\nUI activity demonstration\n\n15/10/2026, 16:21:36\n\nMeera Iyer created a task\n\nUI activity demonstration\n\n15/10/2026, 16:20:47\n\nArjun Rao added a comment\n\nVerify project activity\n\nAPI demo: activity and comment committed together.\n\n15/10/2026, 16:20:04\n\nArjun Rao changed assignee from unassigned to Arjun Rao\n\nVerify project activity\n\n15/10/2026, 16:20:00\n\nArjun Rao changed status from To do to In progress\n\nVerify project activity\n\n15/10/2026, 16:20:00\n\nMeera Iyer created a task\n\nVerify project activity\n\n15/10/2026, 16:20:00\n\nLatest 50 events, newest first.","exportVisible":true,"background":"rgb(15, 23, 42)","headerBackground":"rgb(30, 41, 59)","horizontalOverflow":false}
```

Actual rendered DOM observations:

```json
{"dialog":false,"commentCount":1,"commentsText":"comments\nArjun Rao\n15/10/2026, 16:20:04\n\nAPI demo: activity and comment committed together.\n\nnew comment\n\nComments are permanent once posted.\n\npost comment","assignee":"Arjun Rao","horizontalOverflow":false}
```

```json
{
  "anonymousFeed": 401,
  "frontendRoot": 200,
  "frontendProxyAnonymousProjects": 401,
  "adminFeed": 200,
  "legitimateMe": 200,
  "exportPaused": {
    "status": 503,
    "response": {
      "error": "Airtable export is not configured on the server."
    }
  },
  "memberFeed": 200,
  "viewerFeed": 200,
  "sqlPayload": {
    "status": 200,
    "tasks": 0
  },
  "outsiderFeed": 403
}
```

```json
{
  "evidence": "Retained actual HTTP responses and remote snapshots; no new external calls",
  "firstExport": {
    "total": 7,
    "created": 7,
    "updated": 0,
    "failed": 0,
    "failures": []
  },
  "secondExport": {
    "total": 7,
    "created": 0,
    "updated": 7,
    "failed": 0,
    "failures": []
  },
  "remoteCounts": [
    3,
    10,
    10
  ],
  "taskIdsMatch": true,
  "sameRecordIds": true,
  "noDuplicateStableTaskIds": true,
  "fieldsMatchSeed": true,
  "unrelatedRecordsUnchanged": true,
  "realTestingPausedPendingManualTokenRotation": true
}
```

```json
{
  "allLiveRowsUnchangedDuringHardening": true,
  "originalSeedRowsUnchangedByTable": {
    "memberships": true,
    "projects": true,
    "tasks": true,
    "users": true
  },
  "currentCounts": {
    "activities": 8,
    "comments": 6,
    "memberships": 14,
    "projects": 5,
    "tasks": 15,
    "users": 5
  },
  "canonicalSHA256": "b446deeecdb099ed66ab5cd766a2cecbfae36c0bc902d28320b82265011e7e07"
}
```

The official npm package requirement is satisfied: `backend/airtable/package.json` pins `airtable@0.12.2`; `exporter.mjs` imports Airtable, constructs its client and calls base.makeRequest against api.airtable.com. The Django bridge is server-side. No pyairtable replacement was introduced. The supplied original Google document explicitly requires this official npm SDK; the earlier Python-SDK rubric claim was a legacy-source error, corrected below.

The retained actual exports show 7 created, then 0 created/7 updated, remote counts 3→10→10 and unchanged record IDs; snapshots match stable task IDs, field values and unrelated records. This check made no new Airtable call. The user confirmed token revocation is not done and will rotate it manually. The running backend deliberately has an empty AIRTABLE_API_KEY override; an authorized export returns 503. This is a containment pause, not a newly introduced export failure or proof of a replacement token.

All live seed/demo/comment/activity rows match the pre-hardening baseline. Original seed source and initial migrations remain unchanged. The final README retains explicit user-supplied recording and Airtable screenshot placeholders, configuration/test instructions and honest historical transcript gaps. Incident host/other-credential follow-up remains unverified. Nothing was pushed, squashed, reset or amended.


#### Final artifact checks before the separate documentation commit

`python manage.py check` returned exit 0: `System check identified no issues (0 silenced).` The final read-only database comparison, after authenticated API checks, still matches every baseline row:

```json
{
  "allLiveRowsIncludingSeedCommentsAndActivityUnchangedDuringAudit": true,
  "canonicalSHA256": "b446deeecdb099ed66ab5cd766a2cecbfae36c0bc902d28320b82265011e7e07"
}
```

Credential and artifact scan results (no secret values emitted):

```json
{
  "reachableGitObjectsScanned": 201,
  "configuredAirtableTokenBaseIdOrPrivateSigningKeyFound": false,
  "workingFilesAndAssetsScanned": 85,
  "configuredSecretsInSourceAssetsDocs": false,
  "jwtFragmentsPatOrPasswordHashesInDocs": false,
  "envFilesIgnored": {
    ".env": true,
    ".env.example": true
  },
  "envFilesTracked": false,
  "rootEnvMode": "0o600",
  "newPrivateSigningKeyConfigured": true,
  "seedSourceAndInitialMigrationsUnchanged": true,
  "brokenLocalDocumentLinks": [],
  "whitespaceCheckPassed": true,
  "sourceHead": "e480e076c3aa9d4c273ee1d7048559a3a5154ae4",
  "realApiTestingPaused": true,
  "airtableTokenRevocationUserPending": true,
  "hostEradicationUnverified": true
}
```

The scan covers all 201 reachable source-history objects at `e480e07` plus 85 worktree/submission/build files; configured Airtable token, base ID and new private signing key were absent. Both env files remain ignored/untracked and root dotenv mode is 0600. No complete/fragmented JWT, PAT or password hash appears in submitted documents; local links and whitespace checks pass. The intentionally public demo fixture password remains documented in README, not used as a production secret.

This final documentation commit contains README.md, REVIEW.md, design_notes.md, security_notes.md, COMPLIANCE_AUDIT.md and TERMINAL_LOG.md, separately from `b5a444b` and `e480e07`. It preserves the earlier audit/history, supersedes the prior uncommitted-documents blocker, and leaves the user-provided recording and Airtable screenshot placeholders. No credentials, environment files or seed changes are included. A final post-commit clean-status check is reported to the user; the documentation commit cannot contain its own SHA.

Python package compatibility check: `uv pip check --python .venv/bin/python` exited 0; all 27 installed package requirements are compatible. Three padding-only pytest diagnostic lines in historical failure output were normalized for Markdown whitespace checks; HTTP request/response text was preserved.


## 8. Documentation corrections and direct submission-link verification

Captured 2026-10-15T12:41:50.070607+00:00, after published baseline `b60463b`. This is a later verification checkpoint; historical missing-link/uncommitted/transcript-gap statements above describe their dated stages, not the present status. No application/test/seed source, live records, services or authentication configuration was changed for this documentation work. No old setup/test/seed commands or suspicious historical code were executed.

### Authoritative original and filename correction

Read the entire [user-supplied original assignment](https://docs.google.com/document/d/1Fj4td9MZYZyEH59_IrQGTmNQ9CKTq9OuN8RM6r7gha0/edit) through its text export. Its Part 3c explicitly requires the official `airtable` npm package. The legacy repository ASSIGNMENT.md differs; previous Python-SDK/override/acceptance-concern claims were source-selection errors. The implemented official npm SDK satisfies the original requirement directly. An AI-conversation archive is not a deliverable in that supplied original.

Renamed `design_notes.md` to the required `DESIGN_NOTES.md` with the contents preserved; current Markdown links now use that exact case. Historical command/status output retains the filenames used at the time. REVIEW's original file/line links now target reviewed commit `5f58e52` instead of drifting current-file line numbers.

### Genuine original setup and initial tests recovered

Sections 1–2 now include original 08:14–08:30 UTC command/output captures recovered from the private local tool log. Each block identifies its command timestamp, original response line/time and original-output SHA-256. They show Node/ICU and database/tooling failures, successful dependency/migration/startup output, backend 15 setup errors → 15 passes, frontend unavailable runner → 6 passes/one failed suite → 9 passes, and the original TypeScript build failure. The user-authorized original seed load is recorded after those tests; it was not rerun.

The original tool had already truncated the 6,158-line backend error traceback; the retained diagnostic and error summary are explicitly excerpts. No complete traceback or missing continuous terminal capture is invented. Only selected original tool commands/results were copied, with credentials redacted; private source logs are not submission artifacts.

### Actual Airtable share-view check

[Open the actual shared Tasks view](https://airtable.com/appC1ADL6s1JlxKAP/shrz8aTLD3nTVjoVk). Browser navigation returned HTTP 200 without sign-in. Read the rendered Tasks grid, captured a private screenshot, and compared visible stable IDs with the retained original second-export snapshot. All seven original exported IDs are present. The current view has five additional distinct IDs and three blank-ID rows; no cause/date for those later additions is inferred.

```json
{
  "sharedViewUrl": "https://airtable.com/appC1ADL6s1JlxKAP/shrz8aTLD3nTVjoVk",
  "publicBrowserNavigationHTTP": 200,
  "signInRequired": false,
  "table": "Tasks",
  "visibleRowCount": 15,
  "visibleStableTaskIds": 12,
  "uniqueVisibleStableTaskIds": 12,
  "allVisibleTaskIdsUnique": true,
  "capturedVisibleTextSHA256": "2e032e2df4cbd6c196c7e33f98ee5647fd8826889c4573323fd67d3fb460cbce",
  "airtableApiExportTriggered": false,
  "remoteWritesPerformed": false,
  "originalSecondExportTaskCount": 7,
  "allOriginalSecondExportTaskIdsVisible": true,
  "additionalVisibleStableTaskIdsSinceOriginalExport": 5
}
```

This public visual proof fulfills the assignment's screenshot **or share-link** option; a separate screenshot is optional. The current 15-row view is not relabeled as the earlier 10-row second-export snapshot. The historical first/second real export evidence above remains 7 created, then 0 created/7 updated, counts 3→10→10 and unchanged seven Airtable record IDs. This verification only read the public share; it did not trigger another export or use the potentially exposed PAT. That token's revocation/host remediation remains unverified. Only the authorized public shared-view URL is included; no invitation/access-token URL or signed media URL is stored in the repository.

### Actual Loom recording check

[Open the recording](https://www.loom.com/share/5daf18e351574c57b6d9ce1c2878feaf). Public page access, decoded video/audio streams, actual caption text and sampled decoded frames were checked. The opening narration describes cloning/setup; later actual captions discuss review/SQL fix, Airtable upserts/retries, comments, transaction rollback/activity, JWT hardening and the final 146-test/build/migration result. Spoken statements were cross-checked against retained test/code evidence; the recording's generated summary is not treated as proof.

```json
{
  "publicLoomUrl": "https://www.loom.com/share/5daf18e351574c57b6d9ce1c2878feaf",
  "publicAccessVerified": true,
  "videoCodecs": [
    "h264"
  ],
  "audioCodecs": [
    "aac"
  ],
  "maximumVideoDimensions": [
    1728,
    1080
  ],
  "playableDurationSeconds": 11743.146,
  "sourceDurationSeconds": 11994.795,
  "trimRangeCount": 118,
  "trimmedSeconds": 251.649,
  "actualCaptionCues": 1107,
  "sampledFrameSeconds": [
    15,
    190,
    555,
    1300,
    2350,
    3300,
    3630,
    3670,
    3700,
    3750,
    3810,
    4000,
    4600,
    7000,
    8400,
    10800,
    11700
  ],
  "terminalVisibleThroughout": false,
  "browserOnlySampleSeconds": 555,
  "continuousUncutCoverageVerified": false,
  "sampledOcrCredentialMatches": 0,
  "entireRecordingCredentialAbsenceVerified": false
}
```

Verified visual examples: 00:00:15 shows the clone terminal; 00:09:15 shows a full-browser Airtable homepage with the terminal hidden; 01:56:40 shows the security-checkpoint terminal; 02:20:00 shows the comments result/activity request; 03:15:00 shows the final terminal results/documentation commit. Thus narration/stage coverage and link presence pass, but terminal visibility throughout fails literally. Loom reports 118 trimmed ranges (251.649 seconds); uninterrupted full-session coverage is not certified. Source and playable duration exceed the 90–100 minute assignment timebox. The 24-hour deadline cannot be verified without the receipt timestamp.

OCR of 17 sampled video frames and the current public Airtable screenshot found no configured PAT/signing-key value or generic token pattern. This is a limited sample check, **not** proof that every video frame is credential-free. Raw frames, captions, source logs and signed media/cookie data remain outside Git.

### Verification scope and publication

This correction is documentation/filename-only. Previously completed code verification remains **98 backend + 36 frontend + 12 SDK tests = 146 passing**, production build passed and migrations current; no new code test/build run is claimed for these edits. Link/case, historical HTTP preservation, Markdown whitespace, sensitive-content and seed-source checks are performed on the corrected documents. The pre-publication baseline is `b60463b`. The final completion step creates a separate documentation commit and performs a normal master-to-origin/master push, then verifies local/remote HEAD equality and clean status. Its resulting SHA is reported at delivery; it cannot be embedded inside its own commit. No history rewriting is performed.


Actual pre-publication documentation validation (no code tests were rerun for these Markdown-only changes):

```json
{
  "configuredSecretsFoundOutsideAuthorizedPublicShareUrl": [],
  "genericSecretPatternsFound": [],
  "brokenLocalLinks": [],
  "balancedMarkdownFences": true,
  "historicalCommandAndHttpBlocksUnchanged": 312,
  "designNotesCaseRenamePreservesContent": true,
  "onlyMarkdownFilesChanged": true,
  "seedSourceAndInitialMigrationsUnchanged": true,
  "envFilesIgnoredAndUntracked": true,
  "gitWhitespaceCheckPassed": true,
  "applicationTestsRerunForDocumentationChange": false
}
```
