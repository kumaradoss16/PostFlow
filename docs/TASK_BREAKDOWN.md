# PostFlow Task Breakdown and Delivery Backlog

**Version:** 1.0 | **Status:** Proposed backlog; reconcile against code before execution  
**Planning basis:** ROADMAP.md and the 17 epics in USER_STORIES.md

## 1. How to use this backlog

This is a delivery-oriented decomposition, not a claim that all tasks are unimplemented. Inspect the repository and mark each task Done / Partial / Not Started / Blocked with evidence before assigning it.

Task IDs are planning identifiers. They do not replace or invent IDs in USER_STORIES.md or ACCEPTANCE_CRITERIA.md. Add exact references only after mapping against those source documents.

**Priority:** P0 = safe MVP requirement; P1 = important; P2 = enhancement; FUTURE = SaaS/post-MVP.  
**Sizing:** S = small; M = module/workflow; L = cross-module; XL = high uncertainty/external dependency.  
**Owners:** PO product owner; ARCH architect; FE frontend; BE backend; INT integration; QA quality; SEC security; REL release.

## 2. Backlog summary

| Workstream | Task IDs | Milestone |
|---|---|---|
| Product/repository baseline | T-001–T-008 | M0 |
| Desktop/runtime foundation | T-009–T-019 | M1 |
| Database/data lifecycle | T-020–T-029 | M1 |
| Content domain/UI | T-030–T-041 | M2 |
| AI providers | T-042–T-050 | M3 |
| Media library | T-051–T-057 | M3 |
| OAuth/social accounts | T-058–T-067 | M4 |
| Approval/publishing | T-068–T-080 | M5 |
| Scheduler/calendar | T-081–T-089 | M6 |
| Analytics/privacy/release | T-090–T-102 | M7 |
| Expansion/SaaS | T-103–T-110 | M8/M9 |

## 3. Detailed backlog

### A. Product and repository baseline — M0

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-001 | Inventory implementation against all 17 epics | ARCH, PO | P0 | M | None | Status matrix with code/test evidence |
| T-002 | Reconcile PRD, stories, acceptance criteria and architecture conflicts | PO, ARCH | P0 | M | T-001 | Approved decision log |
| T-003 | Freeze desktop MVP scope and exclusions | PO | P0 | S | T-002 | Approved scope baseline/change control |
| T-004 | Select first platform based on API feasibility/access | PO, INT | P0 | L | None | Official docs, scopes, account eligibility and test evidence |
| T-005 | Define supported Windows versions and installer baseline | ARCH, REL, SEC | P0 | M | T-001 | Support matrix and OS risk decision |
| T-006 | Define coding, branching, review and Definition of Done | ARCH | P0 | S | T-001 | Repository engineering rules |
| T-007 | Create risk/dependency register with owners | ARCH, PO | P0 | M | T-002, T-004 | Critical/high risks have mitigation and owner |
| T-008 | Map story → task → acceptance → test traceability | QA, PO | P0 | L | T-001, T-002 | Exact source IDs mapped; gaps flagged |

### B. Desktop/runtime foundation — M1

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-009 | Bootstrap Tauri 2, React, TypeScript and Vite | FE, REL | P0 | M | T-006 | Clean dev and packaged launch |
| T-010 | Implement FastAPI factory, lifecycle and health endpoints | BE | P0 | M | T-006 | Readiness and shutdown tests |
| T-011 | Implement backend supervision and startup handshake | BE, REL | P0 | L | T-009, T-010 | UI waits for backend readiness |
| T-012 | Bind local API to loopback; reject unsafe host config | BE, SEC | P0 | S | T-010 | Non-loopback bind test rejected |
| T-013 | Generate and store installation secret in OS secure storage | BE, SEC | P0 | L | T-010 | 256-bit random secret; no plaintext persistence |
| T-014 | Implement protected Tauri-to-backend secret provisioning | FE, BE, SEC | P0 | XL | T-009, T-013 | Secret absent from bundle/browser storage/logs |
| T-015 | Add Origin validation, request limits, timeouts and throttling | BE, SEC | P0 | M | T-012, T-014 | Hostile-origin and unauthenticated requests rejected |
| T-016 | Add structured logging, correlation IDs and redaction | BE, SEC | P0 | M | T-010 | Canary secrets absent from logs |
| T-017 | Add frontend routing, error boundary and backend-unavailable states | FE | P0 | M | T-009, T-011 | No false-ready dashboard |
| T-018 | Add CI lint, format, type-check and test jobs | REL, FE, BE | P0 | M | T-006, T-009, T-010 | Mandatory checks block merge |
| T-019 | Add dependency, license and secret scanning | REL, SEC | P0 | M | T-018 | Findings reported; leaked secrets block merge |

### C. Database and data lifecycle — M1

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-020 | Configure SQLAlchemy sessions and SQLite pragmas | BE | P0 | M | T-010 | Foreign keys, WAL and busy timeout verified |
| T-021 | Implement Alembic baseline and naming conventions | BE | P0 | L | T-020 | Fresh and upgrade migration tests pass |
| T-022 | Implement workspace/user/brand persistence | BE | P0 | M | T-021 | CRUD and restart persistence pass |
| T-023 | Implement repository/service layer and workspace scoping | BE | P0 | L | T-022 | Cross-workspace access rejected |
| T-024 | Implement settings without secret values | BE | P0 | M | T-021 | No credential values in settings |
| T-025 | Implement SQLite-consistent backup | BE | P0 | L | T-021 | Consistent DB snapshot and manifest |
| T-026 | Implement restore preview, compatibility and confirmation | BE, FE | P0 | L | T-025 | No overwrite without confirmation/pre-restore backup |
| T-027 | Implement post-restore integrity verification | BE, QA | P0 | M | T-026 | Integrity, FK and record checks pass |
| T-028 | Define deletion/cascade and media cleanup semantics | ARCH, BE | P0 | M | T-022 | No orphan references; recoverable file deletion |
| T-029 | Add migration failure and populated-upgrade tests | BE, QA | P0 | L | T-021, T-025 | Upgrade and restore drill passes |

### D. Content domain and UI — M2

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-030 | Implement content item and campaign models | BE | P0 | M | T-023 | Domain/persistence tests pass |
| T-031 | Implement independent platform variants | BE | P0 | M | T-030 | Variant isolation test passes |
| T-032 | Implement monotonic revision and optimistic concurrency | BE | P0 | L | T-031 | Stale update returns conflict |
| T-033 | Implement approval bound to exact revision | BE | P0 | L | T-032 | Approval only valid for current revision |
| T-034 | Add content/approval audit events | BE | P0 | M | T-016, T-033 | Actor/action/resource/time recorded; sensitive data redacted |
| T-035 | Build dashboard and workspace navigation | FE | P0 | M | T-017, T-022 | Normal/empty/error/loading states verified |
| T-036 | Build content library, search and filters | FE | P0 | M | T-030 | Pagination and empty state work |
| T-037 | Build composer and variant editor | FE | P0 | L | T-031, T-032 | Variants isolated; revision conflicts visible |
| T-038 | Build platform preview and validation feedback | FE, BE | P0 | M | T-037 | Preview reflects selected variant/capability |
| T-039 | Build approval review UI with exact payload summary | FE | P0 | M | T-033, T-034 | Reviewer sees content, media, destination, revision |
| T-040 | Implement capability-based platform content validation | BE, INT | P0 | L | T-031, T-004 | Unsupported operation blocked |
| T-041 | Add accessibility, keyboard and responsive-window regression | FE, QA | P1 | M | T-035–T-039 | Core flows usable at supported window sizes |

### E. AI providers — M3

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-042 | Define provider adapter and capability contracts | ARCH, BE | P0 | M | T-030 | Contract/error taxonomy documented |
| T-043 | Implement OS-backed credential abstraction | BE, SEC | P0 | L | T-013 | DB stores references only; write-only UI |
| T-044 | Implement provider configuration and test UI/API | BE, FE | P0 | M | T-042, T-043 | Key not returned; status shown |
| T-045 | Implement first AI provider adapter | INT, BE | P0 | L | T-042–T-044 | Mock contract and authorized live smoke pass |
| T-046 | Implement generation orchestration and task status | BE | P0 | L | T-045, T-030 | Async lifecycle/cancel/error verified |
| T-047 | Validate structured output and safely render it | BE, FE | P0 | M | T-046 | Invalid output rejected; HTML treated as text |
| T-048 | Implement transmission disclosure and context preview | FE, BE | P0 | M | T-046 | Provider and data categories shown |
| T-049 | Implement failure isolation and no-silent-fallback | BE, QA | P0 | M | T-045, T-046 | No secondary call without user choice |
| T-050 | Add further providers after first adapter stabilizes | INT | P1 | L | T-045–T-049 | Each passes shared contract suite |

### F. Media library — M3

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-051 | Implement media schema and workspace-scoped repository | BE | P0 | M | T-021, T-023 | Ownership enforced |
| T-052 | Implement safe upload and generated storage paths | BE | P0 | L | T-051 | Traversal and extension-spoof tests pass |
| T-053 | Add MIME allowlist, magic-byte and size/dimension validation | BE, SEC | P0 | L | T-052 | Invalid/oversized files rejected |
| T-054 | Implement thumbnails and bounded image processing | BE | P1 | M | T-052, T-053 | Original preserved |
| T-055 | Implement isolated FFmpeg processing | BE, SEC | P1 | XL | T-052, T-053 | Resource/time limits and safe args tested |
| T-056 | Build media library UI and variant associations | FE, BE | P0 | M | T-051, T-052 | Upload/preview/attach/remove states work |
| T-057 | Implement platform media capability validation | INT, BE | P0 | M | T-040, T-053 | Invalid media blocked pre-publish |

### G. OAuth and social account integration — M4

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-058 | Record official API feasibility and scope matrix | INT, PO, SEC | P0 | L | T-004 | Dated evidence and approval status |
| T-059 | Implement OAuth state expiry and single-use validation | BE, SEC | P0 | L | T-013, T-058 | Replay/mismatch/expiry rejected |
| T-060 | Implement PKCE and secure callback where supported | BE, INT | P0 | L | T-059 | S256 and redirect binding verified |
| T-061 | Implement server-side token exchange and secure storage | BE, SEC | P0 | L | T-043, T-060 | Tokens never returned or logged |
| T-062 | Implement account identity, granted scopes and status | BE | P0 | M | T-061 | Identity confirmed; scopes visible |
| T-063 | Implement refresh, rotation, revocation and disconnect | BE, INT | P0 | L | T-061 | Concurrent refresh safe; revoked grant requires reauth |
| T-064 | Define platform adapter and capability registry | ARCH, INT | P0 | M | T-058 | Unsupported operations reported accurately |
| T-065 | Implement first platform adapter and normalized errors | INT, BE | P0 | XL | T-064 | Contract and controlled live tests pass |
| T-066 | Build connected accounts UI and scope disclosure | FE | P0 | M | T-062, T-063 | Connect/disconnect/reauth/limited states work |
| T-067 | Verify real publish permission and account eligibility | INT, QA | P0 | XL | T-065, external approval | Verified publish evidence; otherwise disabled |

### H. Approval and publishing — M5

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-068 | Define publish state machine and transition guards | ARCH, BE | P0 | M | T-033, T-064 | Invalid transitions rejected |
| T-069 | Implement publish preflight validation | BE | P0 | L | T-040, T-057, T-063, T-067 | Approval/account/scope/media/capability checked |
| T-070 | Implement per-destination durable job creation | BE | P0 | L | T-068, T-069 | One independent job per destination |
| T-071 | Implement idempotency key and request fingerprint | BE | P0 | L | T-070 | Duplicate safe; changed payload conflicts |
| T-072 | Implement atomic job claiming and worker lease | BE | P0 | L | T-020, T-070 | Concurrent workers cannot double-claim |
| T-073 | Implement immutable publish attempt history | BE | P0 | M | T-070 | Append-only uniquely numbered attempts |
| T-074 | Implement submission and published-post persistence | INT, BE | P0 | L | T-067, T-073 | External ID stored only from verified response |
| T-075 | Implement unknown-outcome reconciliation | INT, BE | P0 | XL | T-074 | Ambiguous timeout never blindly retried |
| T-076 | Implement bounded retry for definitive transient failures | BE | P0 | M | T-073, T-075 | Retry-After honored; permanent errors not retried |
| T-077 | Implement cancel/pause/emergency stop | BE, FE | P0 | M | T-070, T-072 | Cancel semantics reflect external submission |
| T-078 | Build queue, history and attempt detail UI | FE | P0 | M | T-073–T-077 | Status and reconciliation actions clear |
| T-079 | Implement partial-success reporting | BE, FE | P0 | M | T-070, T-074 | Successful destinations remain successful |
| T-080 | Run controlled publish and fault-injection tests | QA, INT | P0 | XL | T-074–T-079 | No unintended duplicate; uncertainty blocks release |

### I. Scheduler and calendar — M6

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-081 | Persist UTC schedule and IANA timezone | BE | P0 | M | T-070 | UTC instant and timezone retained |
| T-082 | Implement persistent due-job evaluator | BE | P0 | L | T-072, T-081 | Due jobs dispatched once |
| T-083 | Implement restart and missed-run recovery | BE, QA | P0 | L | T-082 | Jobs persist and recover safely |
| T-084 | Handle DST/ambiguous/nonexistent local times | BE, QA | P0 | M | T-081 | Explicit deterministic policy |
| T-085 | Implement schedule edit/pause/resume/cancel API | BE | P0 | M | T-081, T-082 | Invalid transitions rejected |
| T-086 | Build calendar and scheduling UI | FE | P0 | L | T-081, T-085 | Create/edit/pause/status states work |
| T-087 | Surface device asleep/offline/app-stopped limitation | FE, BE | P0 | M | T-083 | Runtime dependency clearly disclosed |
| T-088 | Add missed schedule and expired-account notifications | BE, FE | P1 | M | T-083, T-063 | Actionable notice; no silent publish |
| T-089 | Run concurrency/restart/DST/crash suite | QA | P0 | L | T-082–T-088 | No duplicate dispatch; ambiguity reconciled |

### J. Analytics, privacy and release hardening — M7

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-090 | Verify analytics metric availability per platform | INT, PO | P1 | L | T-058, T-067 | Definitions and API evidence |
| T-091 | Implement analytics snapshots and retrieval | BE | P1 | M | T-090 | Only real verified metrics stored |
| T-092 | Build analytics UI | FE | P1 | M | T-091 | Empty/unavailable/stale states |
| T-093 | Implement audit filtering/export/retention | BE, SEC | P0 | M | T-034 | Redaction and retention tests pass |
| T-094 | Implement user export and deletion workflows | BE, FE | P0 | L | T-028, T-093 | Local vs third-party deletion distinguished |
| T-095 | Implement diagnostics preview and safe support bundle | BE, SEC | P1 | M | T-016 | No DB/media/secrets/content by default |
| T-096 | Complete backup/restore and migration recovery drill | QA, BE | P0 | L | T-025–T-029 | Isolated restore passes integrity checks |
| T-097 | Complete security/privacy/threat verification | SEC, QA | P0 | XL | Security-critical tasks | Critical/high findings resolved or release blocked |
| T-098 | Run performance/resource baseline on target hardware | QA, ARCH | P0 | M | M1–M6 | Startup, memory, media and worker measurements |
| T-099 | Run full regression and acceptance suite | QA | P0 | XL | M1–M6 | All P0 criteria pass with evidence |
| T-100 | Build signed installer and verify update artifact | REL, SEC | P0 | L | T-009, T-018, T-019 | Signature, clean install and upgrade pass |
| T-101 | Publish accurate privacy notice and support/security contact | PO, SEC | P0 | M | T-048, T-093–T-097 | Notice matches shipped behavior |
| T-102 | Conduct release review and publish limitations | PO, ARCH, QA, REL | P0 | M | T-096–T-101 | Signed gate checklist and rollback package |

### K. Post-MVP and SaaS — M8/M9

| ID | Task | Owner | Priority | Size | Dependencies | Acceptance / evidence |
|---|---|---|---|---|---|---|
| T-103 | Add next platform after feasibility review | INT | P1 | XL | T-064–T-067, M7 | Per-platform readiness gates pass |
| T-104 | Add further AI providers/model capabilities | INT | P1 | L | T-050, M7 | Shared adapter contract passes |
| T-105 | Add advanced analytics/reporting | BE, FE | P2 | L | T-090–T-092 | Metric semantics/freshness disclosed |
| T-106 | Define SaaS PRD and commercial validation | PO | FUTURE | L | M7 | Separate scope and customer validation |
| T-107 | Design tenant isolation, identity and RBAC | ARCH, SEC | FUTURE | XL | T-106 | SaaS threat model approved |
| T-108 | Design PostgreSQL, cloud storage and distributed jobs | ARCH, BE | FUTURE | XL | T-107 | Scale evidence justifies services |
| T-109 | Complete SaaS privacy/legal/operational assessment | PRIV, SEC, PO | FUTURE | XL | T-106–T-108 | Data processing and regions reviewed |
| T-110 | Implement SaaS deployment and operations | BE, REL, SEC | FUTURE | XL | T-107–T-109 | Separate SaaS gates pass |

## 4. Critical path

~~~text
M0 scope + platform feasibility
  → M1 local runtime + secure storage + database
  → M2 content variants + revision-bound approval
  → M4 OAuth + verified platform adapter
  → M5 preflight + durable jobs + idempotency + reconciliation
  → M6 scheduler/recovery
  → M7 security + backup + packaged release
~~~

AI/media can be parallelized after content contracts stabilize. Do not let provider breadth block proving the first secure publishing workflow.

## 5. External dependencies and failure responses

| Dependency | Needed by | Owner | Evidence | Failure response |
|---|---|---|---|---|
| Social platform developer access | M0/M4 | PO, INT | App dashboard, official docs, test account | Select feasible alternative; never fake support |
| Platform app review/scopes | M4/M5 | PO, INT | Approval and granted scopes | Keep integration disabled |
| AI provider API access | M3 | PO, INT | Valid key/model capability | Keep mocked adapter; core UI can progress |
| Windows secure-storage integration | M1/M3/M4 | SEC, BE | Threat review and secret tests | No plaintext fallback |
| Code-signing identity | M7 | REL, PO | Certificate and signature verification | Do not claim signed release |
| Supported OS policy | M0/M7 | PO, SEC | Support matrix | Disclose unsupported environments |

## 6. Sequencing rules for a small team

- Limit active cross-cutting backend work and UI work; finish contracts before dependent screens.
- Complete one AI adapter before cloning it.
- Complete one platform integration before expanding platform matrix.
- Avoid simultaneous risky changes to schema, job state machine and scheduler.
- Reserve capacity for integration/security tests, docs and packaging.
- Do not start SaaS implementation before desktop MVP review.

## 7. Task tracking template

~~~text
Task ID:
Title:
Milestone:
Owner:
Priority:
Estimate:
Status: Not Started / In Progress / Blocked / In Review / Done
Dependencies:
Related user story IDs:
Related acceptance criterion IDs:
Implementation notes:
Security/privacy impact:
Test cases:
Evidence:
Known limitations:
Reviewer:
Completion date:
~~~

## 8. Definition of Done

A task is complete only when implementation is reviewed, acceptance conditions pass, tests/evidence exist, failure paths are handled, security/privacy controls are met, docs are updated, no P0 defect remains, and packaged desktop behavior is verified where relevant.

**Planning warning:** IDs and sizes are proposed. Confirm repository state and map to existing story/acceptance IDs before converting this backlog into GitHub Issues or delivery commitments.
