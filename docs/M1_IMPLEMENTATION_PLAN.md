# PostFlow M1 — Implementation Plan

**Status:** Proposed engineering execution baseline — product-owner approval required  
**Milestone:** M1 — Engineering Foundation  
**Branch:** `docs/m1-engineering-foundation`  
**Authority:** `docs/IMPLEMENTATION_BASELINE.md`, `docs/BUILD_READINESS_REPORT.md`

## 1. Purpose and governing decisions

M1 establishes the minimum trustworthy desktop runtime, local API boundary, persistence foundation, engineering controls and Windows CI needed for later product milestones. M1 is infrastructure and a deliberately narrow local vertical slice; it is not the first feature-complete PostFlow release.

The implementation is a **single-user, local-first modular monolith**:
- Tauri 2 + Rust desktop shell.
- React + TypeScript + Vite presentation layer.
- One supervised Python + FastAPI backend process.
- SQLite + SQLAlchemy + Alembic.
- Local application data and filesystem-managed media.
- Windows OS-backed credential storage for the installation secret.
- GitHub Actions on Windows runners.

The implementation baseline is authoritative over older drafts, wireframes and prototypes. Record a decision rather than silently implementing a conflicting requirement.

## 2. M1 scope contract

### 2.1 In scope

1. Repository scaffolding, pinned toolchains and dependency lockfiles.
2. Tauri desktop shell and React application bootstrap.
3. Python backend package, FastAPI application factory and lifecycle.
4. Rust-owned backend process supervision, readiness handshake, crash detection and graceful shutdown.
5. A private loopback API bound only to `127.0.0.1`; no LAN or wildcard binding.
6. Per-installation random authentication secret held by the OS credential store and provisioned through a protected Rust-to-backend channel.
7. Narrow typed Tauri IPC/API proxy so the React runtime never receives the installation secret.
8. Origin/Host validation, request size/time limits, safe error responses, correlation IDs and secret redaction.
9. SQLite connection/session configuration, SQLAlchemy metadata and Alembic baseline migration.
10. Minimal persistence for the local owner/profile, workspace, brand and non-secret settings.
11. Repository/service boundaries and workspace scoping for persisted records.
12. SQLite-consistent backup/restore foundation, only to the degree needed for the baseline acceptance criteria.
13. Automated lint, format, type-check, unit, integration, migration and desktop build checks.
14. Windows packaged-build smoke test and evidence capture.
15. Engineering documentation, threat-to-test traceability and reproducible developer setup.

### 2.2 Explicitly out of scope

No implementation in M1 of:
- AI provider calls, prompt studio, model routing, local LLM inference or AI credential UX.
- Social account OAuth, social platform adapters or publication.
- Publishing jobs, scheduler, campaign management, analytics or content calendar.
- Content/variant authoring workflows beyond minimal test fixtures or a narrowly approved persistence slice.
- Media library, media transformation or public media hosting.
- SaaS, cloud deployment, multi-tenancy, teams, roles, billing or public API.
- Redis, Celery, PostgreSQL server, Kubernetes, microservices or mandatory Docker.
- Automatic background execution while the app is closed, device asleep or offline.
- Windows 10 production support.

A task that appears in a legacy PRD, schema, prototype or backlog is not authorized unless explicitly listed in this section or approved through change control.

## 3. M1 deliverables

| ID | Deliverable | Required evidence |
|---|---|---|
| M1-D01 | Reproducible monorepo scaffold | Clean checkout setup succeeds on Windows |
| M1-D02 | Desktop shell | Tauri app launches and renders frontend |
| M1-D03 | Backend lifecycle | Rust starts, waits for readiness, supervises and stops backend |
| M1-D04 | Authenticated local API | Unauthorized requests fail; non-loopback binding is rejected |
| M1-D05 | Secret boundary | Secret is OS-stored and never exposed to React, logs or SQLite |
| M1-D06 | Database foundation | Fresh migration, upgrade test, FK/WAL configuration and restart persistence pass |
| M1-D07 | Minimal local vertical slice | Create/read/update workspace and brand through approved IPC path |
| M1-D08 | Backup/restore baseline | Consistent backup and verified restore test pass, or explicitly deferred by PO with risk acceptance |
| M1-D09 | CI quality gates | Required Windows workflow is green and blocks merge |
| M1-D10 | Packaged Windows artifact | Clean Windows 11 VM/user-profile launch and smoke test pass |
| M1-D11 | Traceability | Each M1 task maps to acceptance criteria and test evidence |

## 4. Sequencing and dependency graph

| Increment | Work | Dependencies | Exit condition |
|---|---|---|---|
| M1.0 | Freeze decisions, repo conventions, toolchain matrix | Approved baseline | No unresolved blocking architecture decisions |
| M1.1 | Scaffold Tauri, React/TS/Vite and Python package | M1.0 | Clean dev launch; lint/type-check commands exist |
| M1.2 | Backend lifecycle and process supervision | M1.1 | Startup, readiness, crash and shutdown tests pass |
| M1.3 | Local API security and Rust proxy | M1.2 | Secret boundary and hostile-request tests pass |
| M1.4 | SQLite, SQLAlchemy, Alembic and minimal entities | M1.1 | Fresh/upgrade migration and persistence tests pass |
| M1.5 | Backup/restore, data lifecycle and diagnostics | M1.4 | Integrity and recovery tests pass |
| M1.6 | CI, Windows packaging and release evidence | M1.1–M1.5 | All required gates green on clean Windows 11 |

Parallel work is permitted only where dependencies are satisfied. Security architecture must not be postponed until after a working unauthenticated API exists.

## 5. Work package mapping

- Desktop/runtime: backlog T-009–T-017.
- CI/security scanning: T-018–T-019.
- Persistence/data lifecycle: T-020–T-029.

Before implementation, reconcile task IDs and acceptance IDs against `TRACEABILITY_MATRIX.md`; do not invent traceability mappings. Each issue/PR must identify the task IDs, affected decisions, test evidence and any deviations.

## 6. Architectural decisions to freeze before coding

1. **Backend packaging:** package Python as a Tauri sidecar executable for production; development may use the Python interpreter. PyInstaller is the initial candidate, not a proven fact. A spike must verify native dependencies, resource paths, Windows Defender/SmartScreen behavior, clean-machine startup and shutdown. If it fails, evaluate an alternative packager before feature work.
2. **Port allocation:** Rust selects an available ephemeral loopback port and passes it to the backend. The backend must not silently fall back to a wildcard address.
3. **Authentication:** Rust retrieves or creates a high-entropy per-installation secret in Windows Credential Manager/DPAPI-backed storage and provisions it to the backend over a protected local bootstrap channel. React never receives it.
4. **Frontend access:** React invokes narrowly scoped Tauri commands. Rust attaches authentication to requests to the local FastAPI service. Do not expose a general-purpose authenticated HTTP proxy.
5. **Worker lifecycle:** one supervised backend process in M1. Scheduler/worker product behavior is deferred; no hidden service or Windows service is introduced.
6. **SQLite concurrency:** one application-owned database, short write transactions, bounded connection pool and explicit busy timeout.
7. **Data path:** use Tauri application data directory; never rely on current working directory or source-tree-relative writable paths.

Any unresolved choice affecting a trust boundary, persistence compatibility or installer behavior is a blocker, not an implementation-time guess.

## 7. Implementation rules and change control

- One increment per PR where practical; small reviewable PRs preferred.
- No application feature outside scope.
- No secrets, real customer data or production platform credentials in tests.
- No schema edits without an Alembic migration.
- No bypass of Rust proxy to call authenticated backend endpoints from browser JavaScript.
- No merge with failing mandatory checks or unreviewed security exceptions.
- Any scope change requires a written proposal stating user value, cost, security/privacy impact, schedule impact, migration impact and tests; Product Owner and Lead Architect approval are required.

## 8. Definition of Done

A task is Done only when:
- acceptance criteria are linked and objectively met;
- implementation and tests are committed in the same reviewed change;
- formatting, linting, type checks and relevant tests pass;
- security-sensitive behavior has negative tests;
- logs/errors do not disclose secrets or sensitive payloads;
- documentation and configuration are updated;
- no unresolved critical/high issue remains without explicit risk acceptance;
- PR review is complete and CI evidence is retained.

## 9. M1 exit decision

M1 is complete only when every mandatory criterion in `M1_ACCEPTANCE_TESTS.md` passes on a clean supported Windows 11 environment and the Product Owner accepts the evidence. A green development server is not proof of a packaged desktop release. Mock tests are not proof of external API access. No external AI or social integration is part of M1.

**Release recommendation:** do not begin M2 feature work until M1 exit is signed off.