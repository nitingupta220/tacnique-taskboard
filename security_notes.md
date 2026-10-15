# Security investigation and remediation

Date: 2026-10-15. Scope: the executable payload appended to `frontend/postcss.config.js`, related project entry points and dependencies, and possible credential exposure.

**Finding: confirmed malicious remote-code loader, critical impact on the developer account.** The loader has been removed. The production build and all 66 existing tests pass. No affected service was restarted. Repository cleanup does not establish that the workstation or previously accessible credentials are safe.

## Investigation method and evidence

The suspicious JavaScript was **never imported, evaluated, or executed during this investigation**. A private copy was saved as inert text outside the repository. Python performed bounded string permutations, dictionary expansion, and string-table substitution; no JavaScript interpreter was used to decode the payload. No RPC service, bootstrap address, or observed malicious peer was contacted.

Git history establishes the introduction point:

| Revision | Observation |
| --- | --- |
| `32caa63` / `84cb1a6` | Legitimate seven-line PostCSS configuration, 81 bytes. |
| `5f58e52e7906429b2a926d54d1bcfbbe27e774a7` | Adds `createRequire` and an obfuscated suffix after the config on line 8, while the commit message says “remove ASSIGNMENT.md”. File grows to 8,613 bytes. |
| `70f2bd9` / `75e6d4a` | Same malicious file, byte for byte; the SQL and Airtable changes did not introduce it. |

The introducing commit's recorded date is 2026-07-29. Git metadata identifies a commit, not the person responsible or whether an account was compromised. The available evidence does not establish a threat actor or malware family.

SHA-256 evidence:

```text
Original infected config (8,613 bytes):
a70f615aed58637b3deda9d696ad4ca322b265a3625ee4ded06de132d16d9ef7

Statically decoded loader (6,317 bytes):
38c384bc711a63426124db15be3b9fd830aed2f3b3207af204b4f51b61f8bfbf

Restored legitimate config (81 bytes):
e32657baf631d7c5f4dc67b4b2ee0ec8e7d5b3c41860e09cddce7c0377cd80bc
```

During the preceding build attempt, process inspection observed child PID 54679 running an obfuscated `node -e` program and an established TCP connection to `154[.]91[.]0[.]20:443`. That observation was already recorded before this investigation. The child, build, and frontend dev server were stopped. A TCP connection on port 443 alone does not establish the protocol or the contents transferred. No packet capture or remote payload response was retained.

Private evidence and verification logs are retained under `/tmp/taskboard-security` (directory mode 0700). The original and decoded samples are inert `.txt` files, not committed. Earlier connection evidence is also in `/tmp/taskboard-airtable/build-issue.json` and the local `TERMINAL_log.md`. Historical infected commits remain unsafe to run; history was not rewritten.

## Recovered behavior

Loading the original config in Node activates these steps:

1. Replace console logging, warning, error, tracing, grouping, and timing methods with empty functions. Expose `require`, the module, and available file paths through globals.
2. Reconstruct code through string permutations, a dictionary decoder, and dynamic `Function` construction. The hidden code starts an asynchronous loader and suppresses exceptions.
3. Submit `eth_blockNumber` and `eth_getBlockByNumber` JSON-RPC requests through fallback Ethereum RPC providers. Search transaction `from` fields for a fixed substring, then read a matching transaction's `to` address.
4. Decode two IPv4 addresses and ports from that address. This lets the remote operator change bootstrap destinations through blockchain data without changing the repository.
5. Fetch JavaScript over HTTP from `/boot` and `/0/boot`, using an `X` header containing fixed tracking identifiers. Execute downloaded code through `eval` and detached `node -e` processes with ignored stdio. A WSL branch additionally attempts `node.exe`.
6. Use a process-local 30-second timestamp check to limit repeated activation. This does not prevent execution in a new process.

The fetch paths contain no signature or integrity verification for the downloaded code. The downloaded program receives the Node process's account privileges and can load filesystem, process, and network modules. This is unrelated to Tailwind or Autoprefixer functionality.

Relevant indicators, defanged where appropriate:

| Indicator | Meaning |
| --- | --- |
| `5-1580-du` | Embedded campaign/tracking marker. |
| `33ff3edaf55a8e03dcbc7cb40d498a49` | Transaction-sender substring and bootstrap header component; its appearance is not evidence that it is a file MD5. |
| `ethereum-rpc[.]publicnode[.]com1` | Literal first fallback hostname; appears malformed. |
| `eth[.]drpc[.]org`, `eth-mainnet[.]public[.]blastapi[.]io` | Public RPC providers referenced for discovery. Their inclusion does not attribute the attack to those providers. |
| `154[.]91[.]0[.]20:443` | Previously observed remote peer of the downloaded child process. |
| `/boot`, `/0/boot` | Statically recovered bootstrap paths. |

A [GitHub/OpenSSF advisory](https://github.com/advisories/GHSA-43g9-xh9q-657c) documents a similar Ethereum-address discovery and detached-execution technique in a different package. That package is absent from this dependency tree. Similarity supports the technique classification, not attribution or an assertion that the two incidents share an operator. [Microsoft's developer-repository investigation](https://www.microsoft.com/en-us/security/blog/2026/02/24/c2-developer-targeting-campaign/) provides related containment and identity-remediation guidance.

## Credential exposure assessment

**Exposure was possible; actual credential exfiltration is unproven. Treat accessible credentials as potentially compromised.**

The recovered first-stage loader does not itself contain a direct `.env` upload routine. It executes arbitrary remotely supplied JavaScript. That downstream code was not preserved, so its actions cannot be fully reconstructed from the repository.

The root `.env` existed before the observed execution; its recorded modification time was 2026-10-15 09:17:39 UTC. It is owned by the same account running the frontend tools and has mode 0600. That mode permits that account's Node processes to read it. Git ignore rules and server-side credential loading do not isolate a secret file from arbitrary code executing as the same operating-system user. Available telemetry does not establish the first or last execution; earlier commands could also have loaded the infected config.

Potentially accessible material includes the Airtable token, other readable environment files, inherited process environment, and other credentials available to that account. The configured Airtable token had record access and was subsequently granted schema-write access, so exposure could affect both base data and schema. The build parent's Airtable variables are absent in the current investigation environment; that does not prove the environment of the terminated process was clean, and file access alone was sufficient.

An exact-value check of the configured Airtable token and base identifier found:

- No occurrence in 122 reachable Git objects.
- No occurrence in 72 inspected worktree files outside `.env`, excluding dependency trees, virtualenvs, Git internals, and tool caches.
- No occurrence in the final production assets or committed remediation diff (checked after validation).

These checks establish absence from the inspected material, not absence of network exfiltration. No credential value was printed or added to the security notes, test logs, or commit. No further real Airtable requests were made during this investigation.

## Related scripts, dependencies, and configuration

Reviewed the project manifests, Vite/Vitest/Tailwind/PostCSS configuration, HTML/React entry points, Dockerfiles, Compose configuration, setup script, Django entry points/settings, Airtable bridge/exporter, and repository Git hook. A scan for the decoded loader's indicators found no additional matching source in the current worktree or installed project dependencies.

The Airtable bridge intentionally invokes the checked-in Node exporter without a shell. The repository's conversation-copy hook is documented in the README; no remote execution was found in it. No active `core.hooksPath`, custom Git execution filter, or fsmonitor command was configured. No additional malicious entry point was identified in this scope.

All **258 locked npm package archives** (248 frontend, 10 Airtable) were fetched from the official npm registry and verified against its published integrity metadata. Comparing **8,753 installed package files** found two explainable installation differences: esbuild's installed executable matched its verified platform package, and Tailwind's renamed ignore file matched the archive's original bytes. After the fresh installation with lifecycle scripts disabled, only the Tailwind ignore-file rename remained. Archive authenticity and matching source do not by themselves prove a dependency has no vulnerabilities.

The installed Node 22.20.0 executable matches the official Node distribution. Comparing its bundled npm with the installed global npm found a single differing file: `npm/lib/cli.js` was empty instead of 407 bytes, last modified at 08:20:16 UTC on 2026-10-15. Its cause is undetermined; no evidence ties that truncation to this loader. The global installation was left unchanged. Validation used a separately downloaded, integrity-verified Node/npm toolchain outside the repository.

The Python requirements contain the expected application/test packages. Metadata compatibility checks pass for all 27 installed distributions. This virtualenv has no `pip` module, so `pip check` was unavailable; dependency requirements were checked through package metadata instead. This was not a full Python vulnerability audit.

### Separate dependency advisories remain

The frontend npm audit reported **15 affected package entries: 2 critical, 6 high, 7 moderate**. These include inherited dependency findings, not 15 independently reproduced Taskboard exploits. They are separate from the malicious repository implant. The separate Airtable npm project audit reported **zero advisories**.

| Area | Current versions | Reported concern / follow-up |
| --- | --- | --- |
| Vitest / Tinypool | 2.1.9 / 1.1.1 | [Vitest UI-server file execution](https://github.com/advisories/GHSA-5xrq-8626-4rwp), [worker-options prototype-pollution gadget](https://github.com/advisories/GHSA-5gmw-xhrv-c9v3), and [run-options gadget](https://github.com/advisories/GHSA-85c8-ppgw-ccpr). No Vitest UI/API service was enabled for validation. |
| Vite / esbuild | 5.4.21 / 0.21.5 | Development-server file access / origin advisories; keep affected dev services stopped pending a reviewed upgrade. |
| Tailwind and parser/glob dependencies | 3.4.19 | Pattern/selector resource-exhaustion advisories. |
| React Router | 6.30.6 | Redirect and SSR-hydration advisories reported by the registry; application exploitability was not established here. |

Several suggested remediations require major upgrades of Vite, Vitest, Tailwind, or React Router. This commit preserves all dependency versions and records these upgrades as follow-up work. The complete audit JSON remains in `/tmp/taskboard-security/audit.log`; audit exited nonzero because advisories remain.

## Remediation and validation

- Restored `frontend/postcss.config.js` exactly to the legitimate configuration from `84cb1a6`, keeping Tailwind and Autoprefixer. Removed the added `createRequire`, console suppression, decoder, and loader.
- Corrected the frontend lockfile introduced in the Airtable commit `75e6d4a`: 232 entries lacked registry/integrity metadata. Added verified official registry URLs and integrity hashes. No package version changed.
- Quarantined the previous frontend dependencies, build output, and Jiti cache outside the repository. Reinstalled frontend dependencies with `npm ci --ignore-scripts` using an empty npm user/global config and a fresh cache. Dependency lifecycle scripts did not run.
- Used a minimal verification environment with fake Airtable settings and `PYTHON_DOTENV_DISABLED=1`. A macOS sandbox blocked reads of the root `.env` and common credential locations. A probe verified that credential-file reads and network access were denied.
- Blocked all networking for production compilation and frontend tests. Node SDK tests and Django tests were restricted to loopback for the fake HTTP server and isolated PostgreSQL test database.

| Check | Result |
| --- | --- |
| Frontend `npm run build` (`tsc && vite build`) | Passed; 90 modules transformed, production HTML/CSS/JS emitted. |
| Frontend `npm test` | 15 passed. |
| Airtable `node --test` | 12 passed. |
| Backend `python -m pytest -v --tb=short` | 39 passed. |
| Package archive / source verification | 258 archives verified; expected installation differences accounted for. |
| Python dependency metadata compatibility | Passed for 27 distributions. |
| Credential / indicator scans | No configured credential values in inspected Git/output material; no loader indicators in current executable source or production assets. |
| Seed snapshot | All rows and timestamps unchanged; canonical SHA-256 `8799d6b77b1050e3a26d922139106a9aa45851c29d98f73559e36ecc028cc9fe`. |

The build retains existing Vite CJS / ESM-package-type warnings; they do not fail compilation. Verification used the clean tools under `/tmp/taskboard-security/toolchain`, through `run-verified.py`; exact outputs and sandbox profiles are alongside it. Services were not restarted, and no seed or real Airtable data was modified.

## Required incident follow-up

1. From a trusted device, revoke the potentially exposed Airtable token and create a replacement with only the necessary base and record permissions. Review the base's available access/activity history for unexpected record or schema changes. Configure the replacement locally without placing it in chat or Git.
2. Assess other credentials and sessions accessible to this account during the execution window, and revoke/rotate as appropriate. Repository cleanup cannot invalidate stolen credentials.
3. Investigate the workstation for downloaded payloads and persistence using endpoint/process/network telemetry; repair the damaged global npm installation from a trusted distribution. Re-establish a trusted execution environment before starting services with fresh credentials.
4. Plan the dependency upgrades identified by the audit, with compatibility testing. The frontend dev server remains stopped.

No claim of complete host eradication or verified absence of exfiltration is made. The confirmed repository loader is removed and the cleaned application has passed the checks above.
