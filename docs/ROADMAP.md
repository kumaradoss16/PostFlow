# PostFlow Product and Engineering Roadmap

**Version:** 1.0 | **Status:** Proposed delivery baseline  
**Initial release:** Local-first Windows desktop MVP  
**Architecture:** Tauri 2 + React + TypeScript + FastAPI + SQLite

## 1. Executive direction

Deliver PostFlow as a dependable local-first publishing system, not as a broad collection of unfinished integrations. The critical path is:

**Foundation → Content workflow → AI and media → Account authorization → Approval and publishing → Scheduling and recovery → Hardening and release.**

The MVP must prove one complete workflow: create a workspace, configure a brand, create source content and platform variants, attach validated media, connect one verified platform account, approve the exact revision, publish, verify the external post, schedule another post, restart the app, and recover safely.

Do not treat platform logos or provider counts as proof of capability. An integration is supported only after official API permissions, account eligibility, live tests and release evidence are verified.

## 2. Delivery principles and scope

- Complete vertical workflows end-to-end before expanding feature breadth.
- Prioritize revisions, approvals, idempotency, immutable attempts and recovery.
- Isolate AI vendors and social platforms behind adapter contracts.
- Keep desktop deployment lightweight: no mandatory Redis, PostgreSQL server, Kubernetes, Docker or local LLM.
- Require human approval by default; auto-publish is off unless explicitly enabled.
- Treat external API access, platform review, scopes and commercial terms as schedule risks.
- Treat SaaS as a separate deployment and product phase.

### Desktop MVP scope
- Tauri lifecycle, secure local API, SQLite persistence and migrations.
- Workspace and brand management.
- AI provider configuration and explicit data-transmission disclosure.
- Source content, independent platform variants and revision history.
- Media upload, validation, library and basic transformations.
- OAuth for platform(s) that pass readiness gates.
- Revision-bound approval, immediate publishing, durable jobs, attempt history and reconciliation.
- Persistent scheduling, calendar, history, settings, audit events and backup/restore.
- Security, privacy, installer, update and recovery hardening.

### Explicit MVP exclusions unless separately approved
Multi-tenant SaaS, collaboration, billing, enterprise SSO, cloud scheduler, distributed queue, local LLM inference, advanced social listening, and any platform operation lacking verified official API authorization.

## 3. Milestone roadmap

Milestones are dependency-ordered, not calendar promises. Assign dates only after repository inspection, task sizing, platform access and capacity planning. Each milestone ends with a demonstrable increment and go/no-go review.

### M0 — Scope, architecture and delivery baseline
**Objective:** Freeze MVP boundary and resolve blocking decisions.

**Tasks**
- Reconcile PRD, user stories, acceptance criteria, UI/UX, security, database and API specifications.
- Inspect repository implementation; classify capabilities as implemented, partial, missing or blocked.
- Select first social platform based on developer access and verified publishing feasibility.
- Define supported Windows versions, installer/update approach, CI, branching and Definition of Done.
- Create dependency/risk register and traceability mapping.

**Dependencies:** Existing product and architecture documents.

**Exit gate**
- MVP scope approved.
- Blocking architecture decisions resolved.
- Platform access plan and owner assigned.
- Backlog contains dependencies, acceptance criteria, owners and test approach.

### M1 — Desktop foundation and persistence
**Objective:** Launch a stable desktop shell with secure local backend and durable data model.

**Tasks**
- Bootstrap Tauri 2, React, TypeScript and Vite.
- Implement FastAPI lifecycle, readiness and health endpoints.
- Implement loopback-only API, per-installation secret provisioning, Origin validation and request limits.
- Configure SQLite, SQLAlchemy, Alembic and workspace/brand CRUD.
- Add structured logging with redaction, worker lifecycle, backup/restore and integrity checks.
- Establish CI lint, type-check, unit, migration and build jobs.

**Dependencies:** M0.

**Exit gate**
- Clean install launches on supported Windows.
- Local API is not remotely exposed and rejects unauthenticated requests.
- Workspace and brand data persist across restart.
- Migration upgrade and backup/restore tests pass.
- No secret is embedded in frontend assets or committed files.

### M2 — Content domain and UI vertical slice
**Objective:** Create, edit, organize and adapt content without external publishing.

**Tasks**
- Implement content items, campaigns, independent platform variants and revisions.
- Implement optimistic concurrency, audit events and revision-bound approval.
- Build dashboard, content library, composer and platform preview.
- Add platform capability metadata and validation interface.
- Implement approval invalidation on content-affecting edit.

**Dependencies:** M1 database, API and UI shell.

**Exit gate**
- Source content produces independent variants.
- Editing one variant does not mutate siblings.
- Revision increments persist.
- Approval for revision N is invalid after revision N+1 exists.
- API validation and UI states match contracts.

### M3 — AI provider integration and media library
**Objective:** Enable controlled AI assistance and safe local asset handling.

**Tasks**
- Define provider adapter and capability contracts.
- Implement OS-backed credential write/test/replace/delete flows.
- Complete one provider end-to-end before adding more.
- Implement generation, structured-output validation and provider failure isolation.
- Require explicit provider selection and transmission disclosure; prohibit silent fallback.
- Implement media upload, magic-byte/MIME checks, size/dimension/duration limits and safe storage names.
- Add bounded image processing and isolated FFmpeg processing.

**Dependencies:** M1 secure storage/API; M2 content model.

**Exit gate**
- At least one provider passes controlled live test.
- Secrets never appear in DB, API responses, logs or frontend persistence.
- Provider timeout/auth/rate-limit/malformed-output tests pass.
- Media traversal, spoofed MIME, oversized and corrupt-file tests pass.
- No unapproved provider fallback occurs.

### M4 — Social account authorization and platform adapter
**Objective:** Establish a secure, verified connection to the first supported platform.

**Tasks**
- Verify developer app access, review status, account eligibility, terms and scopes.
- Implement OAuth authorization code flow, one-time state, PKCE where supported and callback validation.
- Store tokens in OS-backed secure storage; persist opaque references only.
- Implement account identity, scopes, refresh, disconnect and revocation.
- Implement platform adapter, capability discovery, payload validation, error normalization and rate limits.
- Run controlled live API tests.

**Dependencies:** M1 security/credential storage; M2 variants; external platform approvals.

**Exit gate**
- OAuth replay/mismatch/expiry tests pass.
- Tokens never reach frontend or logs.
- Actual API publishing capability is verified for selected account type.
- Integration limitations and required scopes are documented.
- Integration remains disabled if external authorization is missing.

### M5 — Approval, publishing engine and reconciliation
**Objective:** Deliver safe immediate publication.

**Tasks**
- Implement publish preflight and exact-revision approval recheck before external submission.
- Create independent durable job per destination account.
- Implement idempotency keys, request fingerprints, transactional claiming and immutable attempt history.
- Implement job state transitions, bounded retries, permanent failure handling and unknown-outcome reconciliation.
- Persist external post IDs/permalinks and history.
- Add partial-success reporting and emergency pause.

**Dependencies:** M2 approval; M4 verified adapter; M1 persistence/worker.

**Exit gate**
- Unapproved or stale content cannot publish, including via direct API.
- Duplicate requests create one logical job.
- Accepted-request timeout enters reconciliation, never blind retry.
- Worker crash/restart preserves job and attempt state.
- Controlled real publish succeeds on first platform.
- Partial failure does not corrupt successful destinations.

### M6 — Persistent scheduler, calendar and operational workflows
**Objective:** Enable scheduled publishing that survives app restart and communicates desktop limitations.

**Tasks**
- Persist UTC schedule plus IANA timezone.
- Implement due-job evaluation, worker locking, restart recovery and bounded retry.
- Implement schedule create/edit/pause/resume/cancel and calendar views.
- Test daylight-saving transitions and ambiguous/nonexistent local times.
- Surface offline, asleep, app-closed, expired-token and missed-run conditions.

**Dependencies:** M5 publishing engine and durable job model.

**Exit gate**
- Scheduled jobs survive restart and recover deterministically.
- No duplicate dispatch after restart or concurrent worker claim.
- Timezone/DST tests pass.
- UI explains device must be awake, online and running.
- Cancellation semantics reflect whether external submission began.

### M7 — Analytics, privacy, backup and release hardening
**Objective:** Prepare a reliable, supportable desktop MVP.

**Tasks**
- Implement only metrics supported by verified platform APIs.
- Finalize audit retention, diagnostics redaction, export and deletion.
- Complete backup/restore, migration upgrade and recovery drills.
- Run regression, security, dependency, performance, compatibility and accessibility suites.
- Build signed installer; test clean install, upgrade, update verification and uninstall.
- Publish user-facing privacy notice based on actual behavior.
- Prepare release notes, known limitations, support and rollback plan.

**Dependencies:** M1–M6.

**Exit gate**
- All P0 acceptance tests pass.
- No unresolved critical/high security finding.
- No credential exposure or duplicate-publication defect in fault injection.
- Backup restore and upgrade pass.
- Enabled integrations pass controlled live tests.
- Installer/signature/smoke tests pass.
- Privacy/security docs match implementation.
- Release owner signs off.

### M8 — Post-MVP expansion
Add platform adapters, AI providers, advanced analytics, campaigns and media capabilities only after feasibility, threat/privacy review, acceptance criteria and regression coverage are approved.

### M9 — SaaS discovery and separate deployment profile
Evaluate PostgreSQL, identity/MFA, tenant isolation, cloud object storage, distributed jobs, secrets management, backups, billing, quotas, collaboration, subprocessors and data residency. Require separate PRD, threat model, privacy assessment, operating model and cost model. SaaS is not a deployment toggle.

## 4. Dependency graph

~~~mermaid
flowchart TD
    M0[M0 Scope and architecture] --> M1[M1 Desktop and persistence]
    M1 --> M2[M2 Content domain and UI]
    M1 --> M3[M3 AI and media]
    M2 --> M3
    M1 --> M4[M4 OAuth and platform adapter]
    M2 --> M4
    M2 --> M5[M5 Approval and publishing]
    M4 --> M5
    M1 --> M5
    M5 --> M6[M6 Scheduler and calendar]
    M3 --> M7[M7 Hardening and release]
    M4 --> M7
    M5 --> M7
    M6 --> M7
    M7 --> M8[M8 Product expansion]
    M7 --> M9[M9 SaaS discovery]
~~~

AI/media can proceed partly in parallel once content contracts stabilize. Publishing depends on approval, OAuth, verified platform capability and durable job execution.

## 5. Cross-cutting technical risks

| Risk | Probability / impact | Mitigation | Release consequence |
|---|---|---|---|
| Platform API access/review delayed | High / High | Validate access in M0; prototype early | Do not enable blocked platform |
| Platform policy/API drift | Medium / High | Dated capability evidence and adapter isolation | Disable until reverified |
| Duplicate/uncertain publication | Medium / Critical | Idempotency, immutable attempts, reconciliation | Release blocker |
| Credential leakage | Medium / Critical | OS secure store, redaction, secret scans | Release blocker |
| Stale approval/bypass | Medium / Critical | Revision-bound approval, backend enforcement | Release blocker |
| SQLite contention/worker races | Medium / High | Short transactions, atomic claims, concurrency tests | Block if integrity fails |
| Desktop scheduler unavailable during sleep/offline | High / Medium | Persistent queue and explicit UX | Must disclose; no cloud guarantee |
| Unsupported OS risk | High / High | Define supported OS baseline and risk acceptance | No unsupported OS security guarantee |
| 8 GB RAM/storage constraints | Medium / Medium | Bounded media jobs; no local LLM | Performance gate |
| Media parser vulnerabilities | Medium / High | Patched libraries, limits, subprocess isolation | Block unsafe media feature |
| AI outage/rate limits/cost | High / Medium | Adapter isolation, explicit provider choice | Degrade safely |
| Migration/restore data loss | Low / Critical | Backup-before-migration and restore drills | Release blocker |
| MVP scope creep | High / High | Scope freeze and change control | Re-plan, do not accumulate unfinished work |
| Privacy docs diverge from code | Medium / High | Data-flow review against shipped behavior | Block notice approval |

## 6. Critical decisions

1. Select first platform only after developer access and test-account eligibility are verified.
2. Define supported Windows baseline. Windows 10 is out of support; do not imply Microsoft security updates continue.
3. Finalize protected Tauri-to-backend local API secret provisioning before API exposure.
4. Validate secure-storage library and fail-closed behavior early.
5. Decide supervised child worker versus embedded service; test lifecycle and recovery.
6. Bind approval to exact revision and material media/destination fields.
7. Document platform-specific reconciliation options; require manual resolution when outcome cannot be proven.
8. Do not promise analytics metrics without API evidence.

## 7. Release stages

- **Internal alpha:** Local content workflow with mocked external integrations; no public publishing.
- **Private beta:** Secure provider and one verified platform; controlled accounts; approval, publishing and scheduling tests.
- **MVP release candidate:** Scope frozen; P0/security/recovery/backup/platform/installer gates satisfied.
- **General availability:** No blockers; privacy notice, support process and supported integration matrix published.

## 8. Change control and Definition of Done

Any new platform, provider, permission, data flow, automation or SaaS feature requires value statement, architecture/data impact, security/privacy review, API feasibility evidence, dependencies, estimate, acceptance criteria, tests and rollback implications.

A task is done only when code is reviewed, acceptance criteria pass, automated/manual evidence exists, security/privacy controls are implemented, docs are updated, no P0 defect remains and packaged desktop behavior is verified where applicable.
