# PostFlow M1 — Acceptance Tests and Release Gates

**Status:** Proposed executable acceptance baseline  
**Milestone:** M1 Engineering Foundation  
**Target release environment:** Clean Windows 11 x64 machine/user profile

## 1. Acceptance principles

Acceptance is evidence-based. A design statement, green unit test, local development launch or mocked API response is not proof of a packaged application. Each criterion must have a reproducible test, recorded result and owner.

M1 has no AI provider or social-platform integration acceptance criteria because those capabilities are out of scope.

## 2. Test environment

Required:
- clean Windows 11 x64 VM or physical machine;
- standard non-administrator user for normal launch;
- no Python runtime installed for packaged test;
- network available only as required to download/install the artifact;
- clean PostFlow user-data directory;
- test artifact built from a reviewed commit;
- test report with commit SHA, artifact SHA-256, OS build and tool versions.

Also run a development smoke test on the user's constrained Windows 10 environment if desired, but it is best-effort and does not change the Windows 11 production support baseline.

## 3. Test cases

| ID | Scenario | Procedure | Expected result | Gate |
|---|---|---|---|---|
| M1-AT-001 | Clean checkout setup | Follow README on clean Windows dev machine | Dependencies install from lockfiles; app starts | Block |
| M1-AT-002 | Desktop launch | Launch packaged installer/app | Tauri window opens; no false-ready state | Block |
| M1-AT-003 | Backend startup | Observe supervised child process | Rust starts expected sidecar and validates readiness | Block |
| M1-AT-004 | Startup timeout | Delay or prevent backend readiness | UI shows bounded failure; no infinite spinner | Block |
| M1-AT-005 | Protocol mismatch | Start incompatible backend handshake | App refuses ready state and reports safe error | Block |
| M1-AT-006 | Loopback binding | Inspect actual backend listener | Bound only to `127.0.0.1` | Block |
| M1-AT-007 | Unsafe bind rejection | Configure wildcard/LAN host in test | Backend fails closed | Block |
| M1-AT-008 | LAN reachability | Probe backend port from second LAN device | Connection cannot be established | Block |
| M1-AT-009 | Missing auth | Call protected API without credential | Generic 401/403; no data returned | Block |
| M1-AT-010 | Invalid auth | Call protected API with wrong credential | Generic 401/403; rate limit applies | Block |
| M1-AT-011 | Origin/Host attack | Send untrusted Origin/Host combinations | Request rejected before use case | Block |
| M1-AT-012 | Secret isolation | Inspect bundle, args, env, frontend storage, DB and logs | No installation secret is present | Block |
| M1-AT-013 | Narrow proxy | Attempt arbitrary URL/method via frontend IPC | No generic forwarding capability exists | Block |
| M1-AT-033 | Bootstrap pipe isolation | Inspect child process handle inheritance and attempt access from unrelated child | Only the intended backend receives the bootstrap channel | Block |
| M1-AT-034 | WebView CSP/navigation | Attempt remote script load, remote connect, untrusted navigation and popup | CSP blocks remote content; navigation/popup denied or routed through explicit allowlist | Block |
| M1-AT-014 | Backend crash | Terminate backend while UI open | UI becomes unavailable; no false success; bounded recovery | Block |
| M1-AT-015 | Graceful shutdown | Exit app normally | Backend stops and process is reaped | Block |
| M1-AT-016 | Forced shutdown | Hang backend shutdown in test | Rust terminates after bounded grace period | Block |
| M1-AT-017 | Fresh migration | Start with empty database | Alembic upgrade reaches head; schema valid | Block |
| M1-AT-018 | Populated upgrade | Upgrade fixture from prior schema | Data preserved; integrity checks pass | Block |
| M1-AT-019 | Migration failure | Inject failing migration | App does not declare ready; DB recoverable | Block |
| M1-AT-020 | SQLite settings | Inspect every new connection | FK enabled; busy timeout set; WAL verified | Block |
| M1-AT-021 | Persistence restart | Create workspace/brand, restart app | Records remain and can be read | Block |
| M1-AT-022 | Workspace scoping | Request record outside allowed workspace scope | Access denied/not found; no leakage | Block |
| M1-AT-023 | Transaction rollback | Force service failure mid-write | No partial logical mutation remains | Block |
| M1-AT-024 | Backup consistency | Backup while WAL contains committed writes | Backup integrity and expected records pass | Block |
| M1-AT-025 | Restore validation | Restore valid backup to clean profile | Integrity/FK checks pass; records accessible | Block |
| M1-AT-026 | Invalid restore | Restore corrupted/incompatible backup | Rejected; active DB remains untouched | Block |
| M1-AT-027 | Path robustness | Use user profile path with spaces/Unicode | App launches and persists data correctly | Block |
| M1-AT-028 | Clean machine package | Install where Python is absent | Sidecar runs; no developer dependency required | Block |
| M1-AT-029 | CI verification | Open PR and run required workflows | All mandatory Windows checks pass | Block |
| M1-AT-030 | Artifact hygiene | Inspect release artifact | No secrets, `.env`, test DB or dev config | Block |
| M1-AT-031 | Reproducible build evidence | Rebuild same commit/toolchain | Inputs, versions and hashes recorded; differences explained | Block |
| M1-AT-032 | User data uninstall policy | Install, create data, uninstall/reinstall | Data retention/deletion matches explicit policy | Block |

## 4. Minimal vertical-slice acceptance

The M1 local slice is limited to workspace and brand persistence:
1. User launches desktop app.
2. UI obtains readiness through typed Tauri IPC.
3. User creates a workspace.
4. User creates a brand scoped to that workspace.
5. User reads and updates those records.
6. Backend enforces validation and workspace ownership.
7. App restarts.
8. Records remain available.

No AI, media, OAuth or publishing controls should be shown as operational. Placeholder UI must be explicitly marked unavailable or omitted.

## 5. Security release gates

Release is blocked if:
- backend listens on any non-loopback interface;
- protected route accepts missing/invalid auth;
- secret is exposed to React, frontend storage, bundle, process arguments, environment, database, logs or diagnostics;
- arbitrary URL/method/header proxy is available to frontend;
- untrusted Origin/Host can invoke state-changing operations;
- error responses expose stack traces, SQL, paths or secrets;
- secure credential storage failure triggers plaintext fallback;
- any critical/high security finding is unresolved without formally approved exception.

## 6. Reliability and data gates

Release is blocked if:
- app reports ready before backend/database readiness;
- backend child is orphaned after normal exit;
- migration failure damages or silently replaces user data;
- a committed workspace/brand mutation is lost on normal restart;
- restore replaces the active DB before validation;
- integrity or FK checks fail;
- startup/shutdown can hang indefinitely;
- packaged app requires a developer Python installation.

## 7. CI and quality gates

All required Python, frontend, Rust, migration, security, Windows build and packaged smoke jobs must pass. Formatting, lint, type-check, test or build failures are blocking. Any exception must have owner, issue, mitigation, expiry and explicit approval.

## 8. Evidence package

For M1 sign-off retain:
- commit SHA and PR links;
- Windows runner image and toolchain versions;
- CI run URL and job summaries;
- packaged installer/artifact and SHA-256;
- clean-machine install/launch/shutdown report;
- listener inspection and LAN probe result;
- authentication/origin negative-test report;
- secret scanning and artifact inspection report;
- migration/backup/restore test report;
- known limitations and accepted risks;
- Product Owner and Lead Architect sign-off.

## 9. Final go/no-go

**GO** only if all blocking tests pass, no unapproved critical/high issue remains, and evidence package is complete.

**NO-GO** if any mandatory security, data-integrity, runtime lifecycle, clean-package or CI gate fails or lacks evidence.

Product Owner acceptance: ____________________  Date: __________

Lead Architect acceptance: ___________________  Date: __________