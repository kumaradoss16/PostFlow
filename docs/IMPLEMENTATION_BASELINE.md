# PostFlow — Implementation Baseline

**Document type:** Engineering implementation control document  
**Status:** Proposed baseline — requires product-owner acceptance  
**Reviewed branch:** main  
**Reviewed commit:** a05cf5a246eb8d2ca3b3477c61275e5609b7f180  
**Decision record:** [BUILD_READINESS_REPORT.md](./BUILD_READINESS_REPORT.md)  
**Target:** Local-first Windows desktop MVP  
**Production release:** Not approved by this document

> This document converts the existing specifications into an actionable implementation contract. It does not certify platform API access, OAuth approval, legal compliance or production readiness. Where older requirements conflict with this baseline, the decisions below and BUILD_READINESS_REPORT.md take precedence, subject to explicit product-owner acceptance.

---

## 1. Executive decision

**Proceed with M0 requirements reconciliation and repository preparation, then implement the desktop foundation in controlled increments. Do not start full-product implementation.**

PostFlow's first release is a single-user, local-first desktop application for creating source content, managing independent platform variants, using AI assistance, managing local media, approving exact publication revisions, and publishing/scheduling through no more than one verified official social-platform integration.

The approved architecture is a **modular monolith**:

- Tauri 2 + Rust desktop shell.
- React + TypeScript frontend.
- Python + FastAPI local backend.
- SQLite with SQLAlchemy and Alembic.
- Local filesystem media storage.
- OS-backed credential storage.
- One AI provider adapter initially.
- At most one social-platform adapter, selected only after a documented feasibility gate.
- Durable local publishing jobs and a supervised worker.

The MVP is not a SaaS product, distributed microservice system or generic multi-platform automation engine.

### 1.1 What this baseline authorizes

After product-owner acceptance:

1. Requirements reconciliation and traceability repair.
2. Repository scaffolding, engineering standards, CI and test harness.
3. Desktop/backend process integration and secure local API boundary.
4. SQLite initialization and migration foundation.
5. Workspace/brand persistence and the first end-to-end local vertical slice.

It does not authorize enabling an external social integration before access and media feasibility evidence is approved.

### 1.2 Repository status at review

At reviewed main commit a05cf5a246eb8d2ca3b3477c61275e5609b7f180:

- The root contains a minimal README and docs directory.
- No application source directories or dependency manifests were present.
- No Alembic migration artifacts, executable test suite, CI workflow or installer configuration were present.
- Documentation is a design baseline, not evidence that the described functionality exists.

Recheck main before implementation if it has advanced beyond the reviewed commit.

---

## 2. Source-of-truth hierarchy

Use this hierarchy when documents disagree:

1. **IMPLEMENTATION_BASELINE.md** — implementation scope, sequencing, gates and repository conventions.
2. **BUILD_READINESS_REPORT.md** — recorded contradiction resolutions and build-readiness rationale.
3. **PRD.md** — product requirements after reconciliation and acceptance against this baseline.
4. **ACCEPTANCE_CRITERIA.md** — observable acceptance conditions, aligned to approved scope.
5. **USER_STORIES.md** — user-facing requirements aligned to approved scope.
6. **TRACEABILITY_MATRIX.md** — links stories to acceptance criteria, tasks and tests.
7. **ARCHITECTURE.md** — authoritative system architecture and trust boundaries.
8. **SYSTEM_DESIGN.md** — detailed implementation behavior.
9. **ARCHITECTURE_DIAGRAMS.md** — visual representation of the authoritative architecture.
10. **DATABASE_SCHEMA.md** and **API_SPECIFICATION.md** — proposed persistence and API contracts; implementation must validate and version them.
11. **SECURITY.md**, **THREAT_MODEL.md**, **PRIVACY.md** — mandatory security/privacy controls.
12. **PLATFORM_API_RESEARCH.md** — dated evidence for integration decisions; it does not grant platform access.
13. **ROADMAP.md**, **TASK_BREAKDOWN.md**, **TEST_PLAN.md**, **UI_UX_SPECIFICATION.md** — delivery planning, testing and UI guidance, subordinate to approved scope.

**Conflict rule:** do not silently choose whichever document is easiest to implement. Record the conflict, update affected source documents and link the resolution in traceability. No implementation task may expand MVP scope merely because a feature appears in an older document or prototype.

---

## 3. Audited documentation findings

The review covered product, requirements, architecture, data/API, security/privacy, platform feasibility and delivery documents in docs/.

| Document | Audit finding | Implementation treatment |
|---|---|---|
| PRODUCT_VISION.md | Describes a broad multi-provider, multi-platform future product. | Preserve as long-term direction; not MVP scope. |
| PRD.md | Still marked Draft/Pending Approval; objectives and metrics imply multiple AI providers and seven social platforms. | Reconcile to one initial AI provider and at most one verified social integration. |
| USER_STORIES.md | OpenAI/Gemini/Anthropic provider stories are marked P0; multi-platform and campaign language is broader than approved MVP. | Reprioritize stories; retain future stories as P1/Future. |
| ACCEPTANCE_CRITERIA.md | Some criteria still state Windows 10 and Windows 11 are supported; broad provider/destination assumptions remain. | Align P0 criteria with Windows 11 baseline, one provider and platform gates. |
| TRACEABILITY_MATRIX.md | Story and acceptance IDs exist, but exact story-to-acceptance-to-test mapping is not proven complete. | Repair and validate mappings before claiming coverage. |
| BUILD_READINESS_REPORT.md | Records principal contradictions and conditional-go decision. | Use as the decision record; source docs are not assumed reconciled. |
| ARCHITECTURE.md | Defines modular monolith and domain/infrastructure boundaries. | Authoritative architecture document. |
| SYSTEM_DESIGN.md | Detailed design overlaps architecture and may drift. | Treat as detailed design; reconcile with ARCHITECTURE.md and diagrams. |
| ARCHITECTURE_DIAGRAMS.md | Diagrams can drift and may include future/external components. | Show approved MVP paths; label future components. |
| DATABASE_SCHEMA.md | Includes campaigns, workspace membership and separate scheduling concepts that conflict with single-user/one-time schedule scope. | Reconcile before migrations; do not implement deferred tables by default. |
| API_SPECIFICATION.md | API resources and auth/OAuth flows need alignment with native Tauri trust boundaries and simplified schedule model. | Treat as proposed contract; version DTOs and enforce backend invariants. |
| UI_UX_SPECIFICATION.md | Contains future analytics/provider/platform surfaces and broad navigation. | Hide, disable or label unimplemented capabilities; UI reflects backend capability registry. |
| SECURITY.md | Establishes secret storage, local API and approval safeguards. | Release-blocking controls, not optional hardening. |
| THREAT_MODEL.md | Identifies localhost abuse, OAuth replay, secret leakage, stale approval, duplicate publish and unsafe media risks. | Convert threats into test cases and release gates. |
| PRIVACY.md | Requires disclosure and minimization for external provider transmission. | Implement before first external AI request and account connection. |
| FEASIBILITY_REPORT.md | Contains feasibility assumptions requiring current validation. | Supporting analysis, not proof of present-day access or approval. |
| PLATFORM_API_RESEARCH.md | Research covers multiple candidate platforms and restrictions. | Select one candidate using current dated evidence and actual developer-console access. |
| ROADMAP.md | Phased delivery is directionally useful but must match approved scope. | Reconcile milestone scope and dependencies. |
| TASK_BREAKDOWN.md | Includes campaigns, analytics and multiple integrations alongside P0 work. | Reprioritize; do not execute P1/Future tasks in MVP milestones. |
| TEST_PLAN.md | Contains Windows 10/11 and broader feature assumptions. | Update OS support, release gates and tests. |
| MARKET_RESEARCH.md | Supports positioning and market context, not technical acceptance. | Keep separate from engineering release criteria. |
| docs/wireframes and docs/prototype | Illustrative assets may depict features outside approved scope. | Reference for layout only, not implementation contract. |

### 3.1 Required reconciliation register

The following conflicts are known. This baseline records the intended decision; it does not claim source documents have already been corrected.

| ID | Conflict | Baseline decision | Documents to update |
|---|---|---|---|
| RB-01 | Broad multi-platform automated publishing in PRD/vision. | At most one real automated social integration in first MVP. | PRD, stories, AC, platform research, UI, roadmap, tasks, tests. |
| RB-02 | Multiple AI providers marked P0. | One production provider end-to-end; adapter contract supports future providers. | PRD, stories, AC, UI, tasks, tests. |
| RB-03 | Analytics appears as a full module. | Local operational facts only; social performance analytics deferred unless verified and separately approved. | PRD, AC, DB, API, UI, roadmap, tests. |
| RB-04 | Campaign entities/features appear in schema and tasks. | Campaign management excluded from MVP and not a core content/publishing dependency. | DB, API, stories, AC, tasks, tests. |
| RB-05 | Workspace membership/team roles appear in designs. | One local owner; workspaces are organizational partitions, not multi-user authorization. | DB, API, architecture, security, threat model, UI. |
| RB-06 | Scheduler wording implies execution while app/device is off. | Jobs persist, but execution requires worker active, device awake and internet available. | PRD, AC, stories, DB, API, privacy, UI, tests. |
| RB-07 | Local media conflicts with platforms requiring remote media URLs. | No generic public media relay. Block media publishing without safe approved upload path. | Platform research, architecture, API, security, privacy, AC. |
| RB-08 | OAuth descriptions may assume a confidential client secret in desktop binary. | Native/public-client flow with system browser and PKCE where supported; never ship confidential secret. Otherwise defer or approve a separate broker. | Architecture, API, security, threat model, platform research. |
| RB-09 | Local API secret may reach React. | Rust/Tauri owns secret and proxies narrowly scoped requests. React never receives it. | Architecture, API, security, threat model, UI contract. |
| RB-10 | Separate schedules table overlaps publish-job scheduling fields. | One-time scheduled execution is represented by durable publish job; store UTC instant and IANA timezone. | DB, API, diagrams, tests. |
| RB-11 | Windows 10 and 11 both described as supported. | Windows 11 production baseline; Windows 10 best-effort development only. | PRD, AC, feasibility, tests, release docs. |
| RB-12 | Traceability mapping is incomplete/unverified. | Every P0 story maps to AC, implementation task and test evidence. | Traceability matrix, stories, AC, test plan. |
| RB-13 | Architecture and system design overlap. | ARCHITECTURE.md owns system boundaries; SYSTEM_DESIGN.md owns detailed behavior. | Architecture, system design, diagrams. |
| RB-14 | PRD remains pending despite build-readiness report. | Product owner explicitly accepts baseline before PRD status changes. | PRD metadata and approval record. |
| RB-15 | Detailed API/schema specs may be mistaken for implemented contracts. | They remain proposals until code DTOs and migrations are reviewed and tested. | API, DB, tasks, traceability. |

---

## 4. Approved MVP scope

### 4.1 P0 — required for initial MVP

**Application and local data**
- Windows desktop application using Tauri 2.
- Single local owner and organizational workspaces/brands, without team membership or roles.
- React/TypeScript presentation layer.
- Supervised FastAPI backend bound to loopback only.
- SQLite persistence with versioned Alembic migrations.
- Structured logs with secrets and sensitive values redacted.
- Local backup/export and verified restore.

**Content**
- Create and edit source content.
- Create independent platform-specific variants.
- Preserve source and variant revision history.
- Use optimistic concurrency or equivalent stale-write detection.
- Keep destination/account and media association explicit.
- Capability-based validation; unsupported capabilities are not shown as available.

**AI**
- One cloud AI provider integrated end-to-end.
- Provider adapter interface and normalized error model.
- User configures, tests, replaces and removes a credential.
- Secret stored using OS-backed credential storage; database stores only opaque reference.
- Explicit disclosure of provider, purpose and data categories before external transmission.
- Structured AI output is schema-validated and treated as untrusted.
- No silent provider fallback or automatic cross-provider routing.

**Media**
- Local media library and metadata.
- Safe file handling, generated storage names, size/type validation and platform-specific validation.
- Original media preserved when creating derivatives.
- Only implement media processing required for selected platform and P0 journey.

**Accounts and publishing**
- At most one official social-platform integration, chosen only after platform gate.
- Official account authorization and least-privilege scopes.
- Human approval for every first-MVP external publication.
- Approval binds exact variant revision, destination account, media set and material publication payload.
- Material changes invalidate approval.
- Backend repeats approval and preflight checks immediately before submission.
- Independent durable job per destination.
- Idempotent job creation, immutable attempt history and bounded retry only for definitive transient failures.
- Unknown outcomes enter reconciliation; never blindly retry ambiguous submissions.

**Scheduling**
- One-time scheduled publication only.
- Durable job state in SQLite.
- UTC execution instant plus IANA timezone retained.
- Worker executes only while app/worker is active, device awake and online.
- Missed/expired jobs surfaced and handled by explicit recovery policy.
- No cloud execution guarantee.

**Operations and privacy**
- Local operational dashboard: queue, approval, scheduled, published and failure counts derived from local records.
- Account/provider health and actionable errors.
- Privacy/data-transmission disclosure.
- Backup, restore, export and deletion workflows with clear local-vs-third-party boundaries.

### 4.2 P1 — after MVP, separately prioritized

- Additional AI provider adapters.
- Multi-provider comparison, routing and user-authorized fallback.
- Additional social-platform adapters.
- Verified social performance analytics.
- Campaign management and campaign reporting.
- Advanced media transformations and complex video processing.
- Additional research/intelligence features.
- Operational enhancements not required for safe core publishing.

### 4.3 Future — outside desktop MVP

- SaaS deployment and multi-tenancy.
- Team collaboration, member roles and approval delegation.
- Billing, subscriptions and commercial account administration.
- Cloud scheduler or remote execution.
- Cloud media storage or generic public media relay.
- Public API and external automation platform.
- Social listening, engagement automation, scraping or platform-policy circumvention.
- Local foundation-model training or local LLM inference as a product requirement.

**Scope guard:** A feature is not P0 because it appears in a mockup, prototype, vision document, old story or schema draft. It must be explicitly listed above and have a traceable acceptance test.

---

## 5. Architecture and technology contract

### 5.1 Logical architecture

    Tauri 2 / Rust desktop shell
      - Window lifecycle and process supervision
      - OS credential access
      - Narrow typed IPC and authenticated local API proxy
                    |
                    | typed IPC only
                    v
    React + TypeScript UI
      - Views, forms, rendering and user confirmation
      - No database access, provider secrets or publishing rules
                    |
                    | through native proxy
                    v
    Python / FastAPI modular monolith
      API/DTOs -> application use cases -> domain rules
          |              |                 |
          v              v                 v
       SQLAlchemy     AI adapter       Social adapter
       repositories   (one provider)   (zero or one platform)
          |              |                 |
          v              v                 v
       SQLite        Official AI API    Official social API
          |
          +-- local media filesystem
          +-- durable publish jobs, attempts and audit
          +-- supervised local worker/scheduler

This is one desktop application with one backend process and modular internal boundaries. Do not split the MVP into independently deployed microservices.

### 5.2 Component responsibilities

| Component | Owns | Must not own |
|---|---|---|
| Tauri/Rust | App lifecycle, process supervision, native credential access, narrow IPC, local API authentication proxy, packaging. | Product workflows, approval policy, publishing state machine. |
| React/TypeScript | Presentation, user input, rendering, confirmation, usability validation. | Secrets, direct DB access, trusted approval decisions, direct platform API calls. |
| FastAPI | Authenticated DTO boundary, request validation, dependency wiring and use-case invocation. | Vendor-specific business policy embedded in route handlers. |
| Domain/application | Content, revisions, approval, media rules, capability policy, publish transitions, scheduling rules. | Framework and vendor SDK dependencies. |
| Infrastructure/adapters | SQLite, filesystem, OS credential interface, AI/social API clients, worker implementation. | Authority to bypass domain approval or policy. |
| Worker | Claim and execute eligible durable jobs, persist attempts, reconcile unknown outcomes. | Unreviewed content mutation or approval creation. |

### 5.3 Technology selection

| Area | Baseline | Rule |
|---|---|---|
| Desktop | Tauri 2 + Rust | Pin compatible stable versions in manifests/lockfiles. |
| Frontend | React + TypeScript | Use maintained toolchain; lock dependencies. |
| Backend | Python + FastAPI | Select supported Python compatible with native dependencies. |
| Persistence | SQLite + SQLAlchemy + Alembic | All schema changes are migrations. |
| Validation | Typed request/response schemas | Validate API and integration boundaries. |
| Media | Pillow; FFmpeg only if a P0 format requires it | Bound size, dimensions, duration, CPU and processing time. |
| Secrets | Windows Credential Manager or DPAPI-backed integration | No plaintext secrets in SQLite, frontend, logs or backups. |
| Tests | Python unit/integration tests; frontend tests; desktop E2E where practical | Select and pin concrete frameworks in M0. |
| CI | GitHub Actions | Lint, type-check, unit/integration tests, build and security checks. |

**Version policy:** Do not copy arbitrary version numbers into this baseline. During M0, select currently supported compatible versions, pin exact versions in manifests/lockfiles, record the compatibility matrix, and update it through reviewed dependency changes. Floating production dependencies are not acceptable.

### 5.4 Repository structure

Adopt a modular monorepo layout. Names may be adjusted during scaffolding, but boundaries must remain clear.

    PostFlow/
    ├── apps/
    │   ├── desktop/
    │   │   ├── src/                 # React + TypeScript
    │   │   ├── src-tauri/           # Rust/Tauri commands and lifecycle
    │   │   └── package.json
    │   └── backend/
    │       ├── postflow/
    │       │   ├── api/
    │       │   ├── application/
    │       │   ├── domain/
    │       │   ├── infrastructure/
    │       │   ├── integrations/
    │       │   │   ├── ai/
    │       │   │   └── social/
    │       │   ├── worker/
    │       │   └── main.py
    │       ├── migrations/
    │       ├── tests/
    │       └── pyproject.toml
    ├── packages/
    │   └── contracts/
    ├── tests/
    │   ├── integration/
    │   ├── e2e/
    │   └── security/
    ├── scripts/
    ├── docs/
    ├── .github/workflows/
    ├── .gitignore
    ├── README.md
    └── CONTRIBUTING.md

Do not create separate deployable services for AI, social publishing, scheduler or media in the MVP. The integrations directory contains in-process adapter modules.

---

## 6. Non-negotiable security and data-integrity invariants

These are architectural constraints and release blockers. They must be reflected in code, tests and review checklists.

### 6.1 Local API and desktop trust boundary

1. FastAPI binds to 127.0.0.1 only; never bind to 0.0.0.0 in desktop build.
2. Loopback is not authentication. Require a cryptographically random per-installation secret for protected API operations.
3. Rust/Tauri owns the secret and injects authentication through a narrow native proxy.
4. React never receives the raw secret in JavaScript memory, browser storage, URL, DOM, logs or error payloads.
5. Do not expose generic arbitrary HTTP proxy, shell execution, filesystem traversal or credential-read IPC commands.
6. CORS/Origin checks are defense-in-depth, not authentication.
7. Health endpoints expose no sensitive configuration or data.

### 6.2 Credentials and privacy

- AI keys, OAuth tokens and installation secrets use OS-backed secure storage.
- SQLite stores opaque credential references and non-secret metadata only.
- Credential APIs are write-only from UI; return masked status, never the secret.
- Redact authorization headers, tokens, keys, prompts and sensitive content from logs/diagnostics by default.
- Backups never contain raw secret values.
- External AI transmission requires disclosure of provider, purpose and data categories before first request and when relevant settings change.
- Never silently transmit unrelated workspace records, private files or credentials.

### 6.3 OAuth

- Use system browser for authorization.
- Use native/public-client authorization-code flow with PKCE S256 where supported.
- Use high-entropy, short-lived, single-use state bound to platform, redirect URI and initiating flow.
- Validate callback URI, state, expiry, replay and platform binding.
- Never embed a confidential client secret in desktop executable.
- If a platform requires confidential-client authentication and no separately approved broker exists, defer that integration.
- Store tokens in OS-backed storage; show account identity and granted scopes, never token values.

### 6.4 Approval and publication integrity

- Source content and each destination variant are distinct records.
- Every material variant change increments revision identity.
- Approval references exact revision and binds destination account, media set and material publication payload.
- Any material edit after approval invalidates that approval.
- Backend rechecks approval, current revision, destination, media, account state, scopes and capability immediately before submission.
- One durable publish job per destination.
- Use stable idempotency identity/request fingerprint where supported.
- Keep immutable attempt history.
- Retry only definitive transient failures with bounded policy and platform retry guidance.
- Ambiguous timeout or crash after submission becomes unknown/reconciling; never automatically resubmit until outcome is established.
- Distinguish PostFlow acceptance from platform-confirmed publication.

### 6.5 Media safety

- Store assets under application-controlled generated paths; never trust user-provided paths as storage destinations.
- Validate extension, MIME, magic bytes, dimensions, file size and duration as applicable.
- Prevent path traversal, extension spoofing, decompression bombs and unbounded processing.
- Preserve original media when deriving resized/transcoded files.
- Do not fetch arbitrary user-supplied URLs from backend in MVP.
- No generic public media relay or unaudited tunnel.
- If selected platform requires remotely retrievable media and no approved safe upload design exists, block that media capability.

### 6.6 Scheduler and recovery

- Persist jobs before acknowledging scheduling.
- Use transactional job claiming/leases to prevent concurrent duplicate dispatch.
- Store UTC execution instant and IANA timezone; define deterministic daylight-saving behavior.
- On startup, reconcile interrupted/running jobs and surface missed/expired schedules.
- Scheduler is not a cloud service. UI states that app/worker must be active, device awake and internet available.
- App shutdown stops worker gracefully without discarding durable job state.

---

## 7. Platform and provider decision gates

### 7.1 AI provider gate

Before implementing the first live AI adapter, record:

- Provider selected and rationale.
- Official API documentation and supported model list, with review date.
- API key acquisition and account/billing requirements.
- Data categories sent and provider retention/training terms relevant to intended use.
- Supported generation/structured-output capabilities and rate limits.
- Error mapping, timeout and retry behavior.
- Credential storage and rotation test.
- Controlled live smoke test using non-sensitive sample content.

Only one provider is required for P0. The interface must support later adapters, but do not implement multi-provider routing, comparison or fallback in first increment.

### 7.2 Social platform gate

Do not select a platform based only on popularity or API documentation. Evaluate and record evidence in PLATFORM_API_RESEARCH.md:

| Gate | Required evidence |
|---|---|
| Developer access | A developer account and app can actually be created by project owner. |
| Authorization | Supported native/public OAuth flow; PKCE or approved secure approach; no embedded client secret. |
| Account eligibility | A real test account meets platform requirements. |
| Permissions | Required publishing scopes are documented and can be requested/granted. |
| App review | Review, verification or allowlisting requirements and lead time are understood. |
| Publishing | Official API supports required post type and a controlled test publish. |
| Media | Upload path works with local-first storage and does not require an unapproved public relay. |
| Reconciliation | API can verify status, or limitations and manual resolution are documented. |
| Terms and cost | Rate limits, commercial terms, restrictions and fees are understood. |
| Evidence | Dated test results and secret-redacted evidence are recorded. |

**Gate outcome:** PASS, CONDITIONAL or FAIL. Only PASS permits automated publishing implementation. CONDITIONAL permits mock/contract work only. FAIL means select another candidate or ship manual export assistance; do not claim automated publishing.

### 7.3 Manual fallback product path

If no platform passes the gate, continue platform-neutral content creation, AI, local media and export. Manual publishing assistance is acceptable, but the product must not be described as an automated publishing MVP. Keep social adapter disabled.

---

## 8. Delivery plan and implementation milestones

Milestones are dependency-ordered gates, not calendar promises. Each milestone requires review of its exit criteria before the next begins.

### M0 — Implementation baseline and repository preparation

**Objective:** remove specification ambiguity and establish a reproducible engineering foundation.

Tasks:
1. Product owner accepts this baseline and scope boundaries.
2. Reconcile PRD, stories, acceptance criteria, traceability matrix and test plan.
3. Reconcile schema/API/architecture/diagrams to single-user desktop MVP.
4. Decide whether workspace/brand concepts remain P0; retain only if core workflow requires them.
5. Select initial AI provider and complete data-transmission review.
6. Evaluate social candidates; select none until platform gate passes.
7. Create source structure, manifests, lockfiles, environment example and ignore rules.
8. Establish CI for formatting, lint, type-check, unit tests and build.
9. Record supported OS baseline and dependency compatibility matrix.
10. Create ADRs for architecture choices not already explicit.

**Exit criteria**
- Known RB conflicts resolved in source docs or recorded as accepted exceptions.
- Every P0 requirement has an owner/task and planned test.
- No P0 requirement depends on deferred feature.
- CI runs on pull requests and fails on quality-gate violations.
- Clean checkout builds using documented commands.
- No secrets or local data are committed.

### M1 — Desktop/backend foundation

**Objective:** launch secure desktop shell with supervised local backend and durable database.

Tasks:
- Scaffold Tauri 2 + React + TypeScript.
- Scaffold FastAPI modular monolith and dependency wiring.
- Implement Rust-owned installation secret and narrow authenticated IPC proxy.
- Launch FastAPI as supervised child process; handle startup timeout, crash and graceful shutdown.
- Enforce loopback binding and protected API routes.
- Initialize SQLite and Alembic; create first migration.
- Implement structured logging and redaction.
- Add health/status UX that does not leak secrets.
- Add smoke, unit and integration tests.

**Exit criteria**
- Clean Windows 11 environment can install/run development build from documented instructions.
- Tauri launches and supervises FastAPI.
- Backend reachable only through loopback and authenticated native proxy for protected routes.
- React never receives installation secret.
- Backend crash/restart and graceful shutdown are handled.
- Fresh DB creation and sequential migration work.
- Migration failure does not silently destroy or overwrite user data.
- Logs and API errors pass secret-canary checks.
- CI passes.

### M2 — Workspace, brand and content domain

**Objective:** establish core local content system without external integrations.

Tasks:
- Implement local owner/workspace/brand records only as approved in reconciled schema.
- Implement source content CRUD.
- Implement independent platform variant records.
- Implement revision identity, optimistic concurrency and history.
- Implement capability-neutral validation primitives.
- Build workspace navigation, content library and composer.
- Add audit events for material changes.

**Exit criteria**
- Data survives application restart.
- Source and variant edits do not overwrite each other.
- Stale writes return conflict instead of silently overwriting newer content.
- Revision history is queryable and deterministic.
- Tests cover isolation, ownership, deletion and migration behavior.

### M3 — AI adapter and local media

**Objective:** provide controlled AI-assisted generation and safe local asset management.

Tasks:
- Implement OS-backed credential abstraction.
- Implement one provider adapter, model selection and normalized errors.
- Implement disclosure/consent and request preview.
- Validate AI structured output and safely render text.
- Implement local media upload, metadata, safe paths and bounded validation.
- Implement only media processing required for P0.
- Add provider/media contract and fault-injection tests.

**Exit criteria**
- One live provider works through adapter contract.
- No secret returned to frontend or persisted in plaintext.
- Provider/model and request metadata recorded without unnecessary sensitive payload retention.
- No silent fallback occurs.
- Invalid AI output is rejected or safely handled.
- Malformed, oversized and spoofed media is rejected.
- Original assets remain intact after processing.

### M4 — Social account integration (conditional)

**Objective:** connect one eligible account using approved official flow.

Tasks:
- Complete platform gate and record decision.
- Implement OAuth state/PKCE/callback validation as supported.
- Persist account identity, granted scopes and status.
- Implement token refresh/revocation/disconnect.
- Implement capability registry and one platform adapter.
- Verify account eligibility and permissions using controlled test account.

**Exit criteria**
- Platform gate is PASS.
- OAuth replay, expiry, state mismatch and redirect mismatch tests pass.
- Tokens remain in OS-backed storage.
- Account identity and scopes accurately displayed.
- Unsupported operations are blocked.
- No social API secrets or tokens appear in frontend, DB plaintext or logs.

If M4 cannot pass, keep automated publishing disabled and continue only with platform-neutral/manual-export scope.

### M5 — Approval and publishing

**Objective:** deliver one controlled and auditable external publication path.

Tasks:
- Define and test publish state machine.
- Implement preflight and exact-revision approval.
- Implement per-destination durable jobs.
- Implement idempotency identity, request fingerprint and immutable attempts.
- Implement worker claim/lease and bounded retry.
- Implement unknown-outcome reconciliation.
- Build queue, attempt detail, pause/cancel and emergency stop.
- Run controlled test publishing and fault injection.

**Exit criteria**
- Every external publication requires valid approval for exact current payload.
- Editing content/media/destination after approval invalidates approval.
- Backend rechecks immediately before submit.
- Duplicate job creation does not create duplicate publication attempts.
- Ambiguous outcomes never trigger blind retries.
- Attempt history is immutable and auditable.
- Real controlled publication is confirmed through platform evidence.

### M6 — Local scheduling and calendar

**Objective:** schedule approved one-time jobs with reliable restart recovery.

Tasks:
- Persist scheduled UTC instant and IANA timezone.
- Implement durable due-job evaluator and atomic claim.
- Implement restart/missed-run recovery.
- Define DST ambiguous/nonexistent time behavior.
- Build calendar and scheduling controls.
- Display app/device/network execution limitation.

**Exit criteria**
- Schedules survive app restart.
- Worker dispatches a due job once under concurrency.
- Crash/restart tests do not create duplicate publication.
- DST cases are deterministic and documented.
- App stopped/device asleep/offline limitations are visible and accurate.
- Missed schedules are surfaced rather than silently discarded.

### M7 — Hardening and production release candidate

**Objective:** prove product is safe to distribute and recover.

Tasks:
- Complete P0 privacy/export/deletion and backup/restore.
- Run full regression, security, dependency and fault-injection suites.
- Complete accessibility and narrow-window usability checks.
- Produce signed Windows installer and verify install/upgrade/uninstall.
- Generate dependency inventory/SBOM where feasible.
- Complete release notes, known limitations and support policy.
- Close or formally accept all high/critical risks.

**Exit criteria**
- All P0 acceptance criteria and traceability links have passing evidence.
- No unresolved Critical security finding.
- No unresolved High finding without owner, mitigation, expiry and explicit acceptance.
- Backup/restore drill passes on clean test environment.
- Installer signature and upgrade path verified.
- Supported Windows 11 installation passes end-to-end.
- Product claims match verified platform/provider capabilities.

---

## 9. First vertical slice

Do not build the entire dashboard or every module first. The first demonstrable vertical slice should prove the desktop architecture and data boundary with the smallest useful workflow:

1. Launch Tauri desktop shell.
2. Start and supervise FastAPI.
3. Access protected health/status endpoint through Rust-owned IPC proxy.
4. Create one local workspace and brand, if retained in accepted P0 scope.
5. Create and persist one source content item.
6. Restart application and verify the record remains.
7. Display persisted item in React.
8. Run automated tests proving frontend cannot access installation secret and API rejects unauthenticated protected requests.

This slice intentionally excludes live AI, OAuth, social publishing, media processing and scheduling. Those integrations depend on the foundation and their own feasibility gates.

---

## 10. Engineering standards and quality gates

### 10.1 Pull request requirements

Every PR must:
- State scope and linked requirement/task IDs.
- Include tests for changed behavior.
- Update API/schema docs and migrations when contracts change.
- Include security/privacy impact where relevant.
- Avoid mixing unrelated milestones.
- Pass CI.
- Include migration/rollback or recovery notes for persistence changes.
- Include screenshots or short recording for material UI changes where practical.
- Contain no credentials, user content dumps, local database files, media assets or generated build output.

### 10.2 Automated checks

Select and pin exact tools in M0. The pipeline must provide equivalent checks for:

| Layer | Required check |
|---|---|
| Python | Formatter, linter, type checking, unit tests |
| API/backend | Schema validation, auth tests, integration tests |
| Database | Migration upgrade tests, FK/integrity tests, restore tests |
| Frontend | Formatter, lint, TypeScript type check, component tests, production build |
| Rust/Tauri | Format, lint, compile/build checks |
| Security | Secret scanning, dependency vulnerability checks, redaction/canary tests |
| Desktop | Startup/shutdown smoke test and supported OS packaging test |
| End-to-end | Critical user journeys and failure/recovery paths |

### 10.3 Definition of done

A task is done only when:
- Acceptance criteria are implemented.
- Tests cover success, validation failure and relevant failure/recovery paths.
- No P0 invariant is weakened.
- Documentation and traceability are updated.
- CI passes.
- UI behavior reflects backend truth and does not imply unsupported capability.
- No unresolved critical defect is introduced.

A merged PR is not equivalent to a production-ready feature. A mock adapter is not a live integration. A successful HTTP request is not proof of platform publication.

---

## 11. Traceability contract

The traceability matrix must support this chain:

    Product objective
      -> User story
        -> Acceptance criterion
          -> Implementation task / PR
            -> Automated test or documented manual evidence
              -> Release gate

Rules:
- Every P0 story maps to one or more explicit acceptance criteria.
- Every P0 acceptance criterion maps to at least one implementation task and test.
- Every security invariant maps to a negative test or auditable manual test.
- Every external integration requirement links to dated platform evidence.
- Deferred stories remain visible but are excluded from MVP completion percentages.
- Do not count an ID as covered merely because it appears in a matrix; verify referenced behavior exists and test asserts it.

---

## 12. Open decisions and owners

The following decisions must close before the dependent milestone. Where the project owner is the only available decision-maker, record the choice and evidence in an ADR or referenced document.

| Decision | Required by | Owner | Current status |
|---|---|---|---|
| Accept MVP scope and this baseline | Before M0 exit | Product owner | Pending |
| Reconcile PRD/stories/AC/traceability | M0 exit | Product owner + engineering | Open |
| Confirm workspace/brand P0 necessity | M0/M2 | Product owner | Validate against first journey |
| Select Python/Node/Rust/dependency versions | M0 | Engineering | Open; pin in manifests |
| Select first AI provider and data disclosure | Before M3 live adapter | Product owner + engineering | Open |
| Select first social platform | Before M4 | Product owner + integration owner | Open; no selection assumed |
| Verify developer account, scopes, OAuth and app review | Before M4 | Integration owner | External validation required |
| Verify media upload feasibility | Before media publishing | Integration owner + security | External validation required |
| Confirm backup encryption/retention behavior | Before M7 | Engineering + product owner | Open |
| Define missed schedule and DST policy | Before M6 exit | Engineering + product owner | Must be specified and tested |
| Define release signing/distribution process | Before M7 | Product owner + release owner | Open |

---

## 13. Immediate execution checklist

Use this as the next work queue. Do not skip ahead to M3/M4 while M1 foundations are absent.

- [ ] Product owner accepts this baseline.
- [ ] Reconcile PRD scope and status.
- [ ] Reprioritize AI provider stories to one initial provider.
- [ ] Reconcile social platform scope to at most one gated integration.
- [ ] Update Windows support wording to Windows 11 production baseline.
- [ ] Remove campaign/team dependencies from MVP schema and API.
- [ ] Choose one-time scheduling data model; publish job is canonical.
- [ ] Complete P0 story -> AC -> task -> test traceability.
- [ ] Update architecture, system design and diagrams consistently.
- [ ] Scaffold repository structure and manifests.
- [ ] Add CI and required checks.
- [ ] Implement M1 desktop/backend secure startup slice.

**Next implementation instruction:** begin with M0 reconciliation and repository scaffolding only. Do not ask an implementation agent to build PostFlow end-to-end or implement AI/social integrations before the foundation and feasibility gates pass.

---

## 14. Change control

Any proposed change to approved scope, architecture or security invariants must include:

1. Problem and user value.
2. P0/P1/Future classification.
3. Impact on dependencies, data model, API, privacy, threat model and platform terms.
4. Migration and backward-compatibility impact.
5. Acceptance criteria and test plan.
6. Updated traceability links.
7. Product-owner approval.

Security invariants in Section 6 cannot be weakened for implementation convenience or UI requirements. A change introducing a new external data flow, credential boundary, autonomous action or public network exposure requires explicit security review.

---

## 15. References

- [Product Vision](./PRODUCT_VISION.md)
- [Product Requirements Document](./PRD.md)
- [Build Readiness Report](./BUILD_READINESS_REPORT.md)
- [User Stories](./USER_STORIES.md)
- [Acceptance Criteria](./ACCEPTANCE_CRITERIA.md)
- [Traceability Matrix](./TRACEABILITY_MATRIX.md)
- [System Architecture](./ARCHITECTURE.md)
- [System Design](./SYSTEM_DESIGN.md)
- [Architecture Diagrams](./ARCHITECTURE_DIAGRAMS.md)
- [Database Schema](./DATABASE_SCHEMA.md)
- [API Specification](./API_SPECIFICATION.md)
- [Security](./SECURITY.md)
- [Threat Model](./THREAT_MODEL.md)
- [Privacy](./PRIVACY.md)
- [Platform API Research](./PLATFORM_API_RESEARCH.md)
- [Roadmap](./ROADMAP.md)
- [Task Breakdown](./TASK_BREAKDOWN.md)
- [Test Plan](./TEST_PLAN.md)
- [UI/UX Specification](./UI_UX_SPECIFICATION.md)
- [Feasibility Report](./FEASIBILITY_REPORT.md)
- [Market Research](./MARKET_RESEARCH.md)
