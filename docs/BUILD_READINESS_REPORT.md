# PostFlow — Build Readiness and Requirements Review

**Document:** BUILD_READINESS_REPORT.md  
**Review date:** 9 November 2026  
**Review baseline:** main branch at commit 74f310d911c0e0e3ef72b71ef888cced26460e6e  
**Review type:** Requirements, architecture, scope, security, data, API, UX, feasibility and delivery-document review  
**Decision:** **CONDITIONAL GO — MVP scope approved for implementation planning; production release not approved**  
**Implementation audit:** Not possible from the current repository contents; no application source code is present.

---

## 1. Executive decision

PostFlow has a coherent product direction and a largely complete documentation baseline. Its core proposition—create source content, adapt it into independent platform variants, approve a specific revision, and publish through controlled integrations—is technically viable as a local-first desktop product.

However, the current specifications overstate the initial delivery breadth. The PRD, acceptance criteria, platform research, database schema, UI specification, roadmap and test plan do not consistently distinguish:
- the product vision and eventual platform matrix;
- the minimum desktop MVP;
- capabilities that require external platform approval;
- capabilities that are intentionally deferred;
- architectural extension points that are not implementation commitments.

The documentation also contains unresolved decisions around media delivery, native desktop OAuth, local API authentication, scheduling persistence, supported Windows versions and traceability.

### 1.1 Decision summary

| Area | Decision | Status |
|---|---|---|
| Product direction | Local-first social content creation and controlled publishing desktop app | Approved |
| Initial deployment | Single-user Windows desktop application | Approved |
| Architecture | Tauri 2 + React/TypeScript + FastAPI + SQLite modular monolith | Approved with security conditions |
| AI integration | One fully implemented cloud AI provider for first MVP; adapter-based expansion | Approved; PRD/AC adjustment required |
| Social publishing | One officially authorized platform integration at most for first MVP | Conditional on platform feasibility gate |
| Content and variants | Source content, independent platform variants and immutable revision history | Approved |
| Approval | Human approval required for every first-MVP publication; exact-revision binding | Approved; release blocker |
| Scheduling | Local persistent scheduling while the desktop worker is running and machine is awake/online | Approved with explicit limitation |
| Media | Local media library; platform-native upload only where supported | Approved with media gate |
| Analytics | Operational local dashboard; external performance analytics deferred or read-only P1 | Approved with scope reduction |
| Collaboration / SaaS | Excluded from desktop MVP | Approved |
| Windows support | Windows 11 production baseline; Windows 10 best-effort development only, not a supported secure production target | Approved with support-policy update |
| Build readiness | Requirements baseline can enter implementation after listed decision updates; no code-level readiness claim | Conditional GO |

### 1.2 What this approval means

The product scope and target architecture are approved as the implementation baseline described in Section 3. This approval authorizes implementation planning and foundation work.

It does **not**:
- certify that any source code exists or has passed review;
- guarantee developer access, platform app review, OAuth approval or commercial API rights;
- authorize all seven researched social platforms;
- approve a public SaaS launch;
- certify compliance with privacy laws or platform terms;
- waive the release gates in Section 10.

A platform integration remains disabled until its own access, permission, account eligibility, media workflow and live-publish evidence pass the integration gate.

---

## 2. Review scope, evidence and limitations

### 2.1 Documents reviewed

The review inspected the current main-branch documentation set:

- PRODUCT_VISION.md
- PRD.md
- USER_STORIES.md
- ACCEPTANCE_CRITERIA.md
- TRACEABILITY_MATRIX.md
- ARCHITECTURE.md
- SYSTEM_DESIGN.md
- ARCHITECTURE_DIAGRAMS.md
- DATABASE_SCHEMA.md
- API_SPECIFICATION.md
- UI_UX_SPECIFICATION.md
- SECURITY.md
- THREAT_MODEL.md
- PRIVACY.md
- FEASIBILITY_REPORT.md
- PLATFORM_API_RESEARCH.md
- ROADMAP.md
- TASK_BREAKDOWN.md
- TEST_PLAN.md
- docs/wireframes/WIREFRAMES.md
- docs/prototype/index.html

The preceding roadmap/task/test-plan pull request is already merged into main.

### 2.2 Repository inspection

At the reviewed commit, the repository root contains:
- README.md (10 bytes; only the project heading)
- docs/

No application source directories, dependency manifests, build configuration, test implementation, CI workflows, migrations, installer configuration or runtime code were present in the root tree.

Therefore:
- the architecture was assessed for consistency and implementability;
- the documentation was checked for contradictory requirements and missing decisions;
- no code-level architecture conformance, dependency audit, build test, runtime test, security test or performance benchmark could be performed;
- task completion status must not be inferred from the existence of specifications.

This is a documentation-readiness review, not a source-code audit.

### 2.3 Evidence classification

- **Verified in repository:** file contents, declared architecture, requirements, priorities, diagrams, schema proposals and current repository tree.
- **Design recommendation:** decisions made in this report to resolve contradictions and constrain MVP scope.
- **External validation required:** live platform access, current API permissions, app review, OAuth configuration, pricing, legal requirements and actual device behavior.
- **Not verified:** implemented behavior, tests passing, security posture of a built application and production performance.

---

## 3. Approved MVP scope

### 3.1 Product definition

PostFlow MVP is a **single-user, local-first Windows desktop application** that lets one local owner manage workspaces and brands, create source content, generate or edit platform-specific variants, manage local media, connect an officially supported social account, approve an exact content revision, publish through a verified official API, and schedule eligible posts while the desktop worker is active.

The product is not a browser-based SaaS service in its initial release. The local desktop application is the system of record for user content, media, job state and audit history.

### 3.2 P0 — included in the MVP

#### Application foundation
- Tauri 2 desktop shell.
- React + TypeScript presentation layer.
- Python + FastAPI modular-monolith backend.
- SQLite persistence using SQLAlchemy and Alembic.
- One local installation profile; no cloud identity service.
- Workspace creation and switching for the local owner.
- Application startup/shutdown, backend readiness and error recovery.
- Loopback-only local API with authenticated, protected IPC.
- Structured logging with secret and sensitive-content redaction.

#### Brand and content management
- Workspace and brand profile CRUD.
- Source content creation, editing and persistence.
- Platform-specific variants as separate records.
- Source and variant revision history.
- Optimistic concurrency for conflicting edits.
- Content library, composer and preview.
- Platform capability-based validation.
- Basic content status and operational activity.

#### AI assistance
- One production AI provider adapter end-to-end.
- Provider credential entry, test, replace and remove.
- OS-backed secret storage; no raw key in SQLite or frontend.
- User-selected model from the implemented provider's supported model list.
- Explicit disclosure before prompts, selected content or media metadata leave the device.
- Structured-output validation and safe rendering.
- Provider timeout, rate-limit and malformed-output handling.
- No silent provider fallback.

The adapter interface must permit additional providers without coupling the content domain to vendor SDKs. A second provider is a later increment, not a launch dependency.

#### Media
- Local media library and workspace-scoped asset metadata.
- Safe upload, filename normalization and generated storage paths.
- MIME allowlist, magic-byte validation, size limits and safe image processing.
- Media-to-variant association.
- Platform-specific media compatibility checks.
- Original asset preservation.

Video processing is limited to bounded, tested operations. Full video editing is excluded.

#### Social account and publishing
- One social-platform adapter selected only after the M0 feasibility gate.
- Official authorization flow and supported account types only.
- Least-privilege scopes and account capability validation.
- Secure token storage and lifecycle management.
- One durable publishing job per destination account.
- Backend-enforced preflight and approval checks.
- Human approval required before external publication.
- Approval bound to the exact variant revision and material publication payload.
- Immutable publish-attempt history.
- Idempotent job creation and bounded retry for definitive transient failures.
- Unknown-outcome reconciliation; never blind-retry an ambiguous external request.
- Confirmed external post ID/permalink and publication history.
- Partial-success isolation across destinations if multi-destination composition is retained.

If no platform passes the access gate, the team may build the platform-neutral content workflow and a manual-export/manual-publishing assistance path. It must not market or label the result as an automated publishing MVP until at least one real integration passes.

#### Scheduling and calendar
- One-time scheduled publication.
- Persistent job/schedule state in SQLite.
- UTC execution timestamps and an IANA timezone identifier.
- Calendar week/list views and schedule management.
- Worker startup recovery and missed-job reporting.
- Atomic job claiming and restart-safe execution.
- Explicit UI warning that the desktop app/worker must be running, the device awake and internet available.

No cloud scheduler or remote execution guarantee is included.

#### Operations, privacy and recovery
- Settings for non-secret configuration.
- Local operational dashboard.
- Audit events for security-sensitive and publishing actions.
- Backup and restore with confirmation and integrity verification.
- Local export and deletion controls.
- No third-party behavioral analytics by default.
- Signed installer/update verification before public distribution.
- Accurate privacy notice based on shipped behavior.

### 3.3 P1 — deferred from initial MVP unless separately approved

- Additional AI providers and multi-model comparison.
- Provider fallback and task-based routing.
- Advanced AI research/content intelligence.
- Additional social-platform adapters beyond the first verified integration.
- Social performance analytics beyond verified essential metrics.
- Advanced campaign management and campaign reporting.
- Advanced image/video transformations.
- Advanced notifications and recommendations.
- Bulk publishing and advanced workflow automation.
- Additional platform-specific media workflows.
- Advanced calendar and reporting views.

### 3.4 FUTURE — explicitly excluded

- Commercial SaaS deployment.
- Cloud identity, multi-tenancy and tenant isolation.
- Multi-user collaboration and workspace membership.
- Team approval roles and role-based publishing delegation.
- Subscription billing and usage-based billing.
- Enterprise SSO.
- Cloud media storage and distributed job execution.
- Public developer API.
- Agency/client account management.
- Advanced social listening.
- Local foundation-model inference or model training.
- Automated likes, follows, comments, direct messages, fake engagement, scraping, CAPTCHA bypass or policy circumvention.
- Unapproved browser automation for social publishing.

### 3.5 MVP success criteria

The MVP is successful only when a real end-to-end path can be demonstrated:

1. Install and launch the signed desktop application on the supported OS baseline.
2. Create a local workspace and brand.
3. Create source content and a platform-specific variant.
4. Attach valid media when supported by the selected platform.
5. Connect an eligible test account using the official authorization flow.
6. Review the exact variant revision, destination, media and schedule.
7. Approve the revision.
8. Publish through the official API and verify the remote result.
9. Schedule a separate approved post.
10. Restart the application and recover the scheduled job without duplicate publication.
11. Inspect the attempt history and audit events.
12. Back up and restore the local data successfully.

A mocked integration does not satisfy the real publishing success criterion.

---

## 4. Contradictions and resolutions

The following decisions supersede conflicting statements in the current documents. The source documents should be updated to reflect this baseline before implementation begins in the affected modules.

| ID | Conflict / gap | Resolution | Required document updates |
|---|---|---|---|
| R-01 | PRD lists a broad social platform target; platform research lists multiple P0/P1/P2 integrations; acceptance criteria assign different priorities; roadmap says choose one later. | First MVP supports at most one real automated publishing integration. Select it through documented access, account, scope, media and live-test evidence. All other destinations remain unsupported for automated publishing or use manual assistance. | PRD, platform research, acceptance criteria, UI, roadmap, task breakdown |
| R-02 | Four initial AI providers are named, while multi-provider generation/fallback is P1 and roadmap proposes one adapter first. | One fully implemented provider is required for the first AI-enabled MVP. Provider abstraction is P0; additional adapters, comparison and fallback are P1. No silent fallback. | PRD, acceptance criteria, user stories, UI, task breakdown |
| R-03 | Analytics appears in navigation and some requirements, but advanced analytics is future/P1 and schema labels snapshots as later MVP. | Keep local operational KPIs (queue, approval, failure, scheduled counts). Defer social performance analytics unless one verified metric is required and available from the first platform. Never fabricate or infer metrics. | PRD, UI, DB, API, acceptance criteria |
| R-04 | Campaigns appear in data model and product scope, while UI/PRD treat campaign management as future/optional. | Exclude campaign CRUD and reporting from MVP. Retain no campaign dependency in core content/publishing flow. Add campaign tables later only when approved. | DB schema, API, UI, PRD, task breakdown |
| R-05 | Workspace members and SaaS roles appear in architecture/security, but the desktop product is single-user and collaboration is future. | Local installation profile is the sole owner. Workspace separation is organizational data separation, not multi-user authorization. Defer workspace_members and team roles to SaaS. | DB schema, API, security, threat model, UI |
| R-06 | Desktop scheduler is described as persistent, but the product also implies scheduling while the computer may be off or app closed. | Scheduling is durable across application restarts, but executes only while the local worker is running and the device is awake and online. Missed jobs are surfaced and recovered by an explicit policy. No cloud execution claim. | PRD, UI, API, DB, privacy, acceptance criteria |
| R-07 | Media is stored locally, but some platform APIs require a platform upload workflow or remotely retrievable media URL. | No generic public media relay in MVP. The selected platform adapter must support direct upload or an explicitly approved secure upload workflow. If public hosting is mandatory and no safe delivery design is approved, media publishing is blocked; text-only capability may be evaluated separately. | Platform research, architecture, security, privacy, acceptance criteria |
| R-08 | OAuth language assumes backend code exchange, but a native desktop app cannot safely embed a confidential client secret. | Use the provider's supported native/public-client authorization-code flow with system browser and PKCE where available. If a platform requires confidential client authentication, use a separately secured broker service or defer that integration. Never ship a client secret in the desktop binary. | Architecture, API, security, threat model, platform research |
| R-09 | Local API bearer secret is described as unavailable to frontend JavaScript but also provisioned to the trusted Tauri runtime. | Keep the installation secret in the Rust/Tauri side. Route API calls through a narrow Tauri IPC proxy or equivalent protected native bridge. Do not hand the bearer secret to React, browser storage, URLs or arbitrary web content. | Architecture, API, security, threat model, UI implementation contract |
| R-10 | DB defines scheduled_at on publish_jobs and a separate schedules table for one-time scheduling; API also exposes schedule resources. | For MVP one-time schedules, publish_jobs is the canonical execution record and stores scheduled_at_utc plus IANA timezone. Remove the separate schedules table from MVP unless it stores genuinely distinct recurring intent. Calendar reads publish jobs. | DB schema, API specification, architecture diagrams, test plan |
| R-11 | Windows 10 and Windows 11 are both listed as supported; Windows 10 support ended 14 October 2025. | Windows 11 is the supported production baseline. Windows 10 may be used for development experiments or best-effort compatibility testing, but no security-support guarantee is made. | PRD, feasibility, acceptance criteria, test plan, installer docs |
| R-12 | Traceability matrix includes a baseline status but states story-level reconciliation is pending. | The repository contains 96 user-story IDs and 102 acceptance-criteria IDs, but the existence of IDs does not prove each story is correctly mapped to acceptance and test cases. Complete and verify exact story-to-acceptance-to-test links. | TRACEABILITY_MATRIX, USER_STORIES, ACCEPTANCE_CRITERIA, TEST_PLAN |
| R-13 | ARCHITECTURE.md and SYSTEM_DESIGN.md both present architecture decisions and can drift. | ARCHITECTURE.md is the authoritative system architecture and boundary document. SYSTEM_DESIGN.md is the detailed implementation design. A change to one must trigger review of the other and diagrams. | Both architecture documents, document index |
| R-14 | PRD remains marked Draft / Pending Approval despite detailed downstream specifications. | This report records the conditional scope approval. Update PRD status only after the product owner accepts this baseline and its external dependencies. | PRD, document status metadata |
| R-15 | API and schema are detailed but no code or migration artifacts exist. | Treat contracts as proposed baseline. Generate implementation from reviewed DTOs and Alembic migrations; do not assume a written endpoint/table exists in the product. | API, DB, implementation repository |

---

## 5. Architecture approval

### 5.1 Approved logical architecture

Use a **modular monolith with a supervised local worker**, not microservices.

| Layer | Approved component | Responsibility |
|---|---|---|
| Desktop shell | Tauri 2 / Rust | Window lifecycle, native IPC, secure API proxy, packaging, updater |
| Presentation | React + TypeScript | Navigation, screens, local UI state, previews, user interactions |
| Local API | FastAPI | Authenticated DTO boundary, request validation, use-case invocation |
| Application/domain | Python modules | Workspace, brand, content, variant, approval, media, account, publish and schedule rules |
| Integration | Adapter interfaces | One selected AI provider and one selected social platform initially |
| Persistence | SQLite + SQLAlchemy + Alembic | Durable application records, revisions, jobs, attempts and audit |
| Secret storage | Windows Credential Manager / DPAPI-backed integration | API keys, OAuth tokens and installation secret |
| Files | Application-owned local media directory | Original assets, safe derivatives and exports |
| Background execution | One persistent, bounded worker | Schedule evaluation, job claiming, publish attempts and recovery |

Dependency direction:

- UI calls native IPC; native IPC proxies approved local API calls.
- FastAPI invokes application services.
- Application services depend on domain interfaces, not SDKs or database models.
- Adapters implement AI/social interfaces.
- Repositories implement persistence interfaces.
- Worker invokes the same application services and policy checks as interactive requests.

Do not put publishing business rules in the frontend, provider adapter or scheduler loop.

### 5.2 Runtime and local API security

Approved requirements:
- FastAPI binds to 127.0.0.1 only.
- Use a random per-installation secret with at least 256 bits of entropy.
- Store the secret in OS-backed storage.
- React must not receive the raw installation secret.
- Tauri native code owns the secret and performs authenticated API requests through a narrow IPC interface.
- No arbitrary URL proxy, generic shell execution or credential-read IPC command.
- Restrict allowed origins and content types; do not treat CORS as authentication.
- Apply request size limits, timeouts, rate limits and strict Pydantic schemas.
- Health endpoints expose only minimal liveness/readiness.
- Fail closed if secure storage is unavailable.

### 5.3 OAuth decision

The desktop app is a native public client unless a separately hosted broker is introduced. The desktop binary is not a secure location for provider client secrets.

For each selected platform:
1. Verify its current supported native/public-client OAuth flow.
2. Use system browser authorization.
3. Use state, short expiry, single-use validation and PKCE S256 where supported.
4. Validate callback platform, redirect URI, state and initiating transaction.
5. Exchange the code according to the platform's supported native-client model.
6. Keep tokens in OS secure storage.
7. Store only opaque credential references and non-secret metadata in SQLite.
8. Verify identity, account type and granted scopes.
9. Disable unsupported actions when required scopes or app review are missing.

If confidential client authentication is mandatory, either implement a reviewed broker with its own security/privacy/operational scope or defer the integration. Do not embed a client secret.

### 5.4 Publishing and approval invariants

These are release-blocking invariants:

- Every destination account gets an independent publish job.
- A job references an immutable variant revision.
- Approval binds to that exact revision and the reviewed destination/media/payload.
- Any material content, media or destination change requires renewed approval.
- Backend rechecks approval and account capability immediately before external submission.
- Job creation is idempotent; the same key with a different request fingerprint returns conflict.
- Attempts are append-only and uniquely numbered.
- Retry only after a definitive retryable failure.
- Ambiguous timeout or crash after request transmission enters reconciliation.
- Never blindly retry an unknown outcome.
- Persist external identifiers only when confirmed.
- Partial success does not roll back a successful destination.

The initial MVP requires human approval for all external publication. Auto-publish rules are excluded.

### 5.5 Database decision

Use the current schema as a design reference, with the following MVP adjustments:
- app_profiles is the local installation owner; no SaaS user authentication.
- workspaces and brands are local-owner data.
- workspace_members is deferred.
- campaign entities are deferred.
- one-time schedule fields live on publish_jobs; no duplicate schedules table in MVP.
- analytics_snapshots are deferred unless a verified metric is explicitly accepted.
- approvals remain immutable records tied to exact variant revision IDs.
- provider and OAuth credentials remain OS-store references, never raw secret columns.
- SQLite is the single desktop source of truth.

All schema changes require Alembic migrations, foreign-key enforcement, integrity tests, backup-before-migration and tested restore.

### 5.6 Media delivery decision

Local filesystem storage remains the default. A local path is not a public URL and must never be represented as one.

Before enabling media publication, the selected platform adapter must prove:
- supported upload initiation and completion workflow;
- required media formats, size and processing constraints;
- correct account permissions;
- safe retry and upload reconciliation;
- no public exposure of the local media directory.

Do not build a general-purpose public media proxy, temporary bucket or tunnel as an MVP shortcut. Any remote media hosting requires a separate threat model, consent disclosure, retention policy, access controls and cost review.

### 5.7 Worker and scheduling decision

Use one supervised worker process with bounded concurrency. Avoid multiple heavyweight workers on the target desktop hardware.

- The worker claims jobs transactionally.
- A lease/claim expiry supports recovery after process crash.
- The worker reuses the same publishing service as interactive operations.
- Schedule timestamps are UTC; IANA timezone is preserved for display and user intent.
- App shutdown does not erase schedules.
- App closed, device asleep, powered off or offline means execution cannot be guaranteed.
- Startup recovery must classify due, missed, claimed and unknown-outcome jobs without creating duplicates.

No Redis, Celery, PostgreSQL server, Kubernetes or cloud worker is required for the desktop MVP.

---

## 6. API and contract decisions

The existing API specification is a strong starting point, but implementation must follow these rules:

1. Keep the versioned API prefix and stable DTOs.
2. Use UUID identifiers, UTC ISO-8601 timestamps and snake_case fields consistently.
3. Require the native Tauri proxy to authenticate local API calls; never expose secrets to React.
4. Use strict request models and reject unknown fields on security-sensitive commands.
5. Enforce workspace/resource ownership in application services, not only in routes or UI.
6. Use optimistic concurrency for mutable content and variants.
7. Use an Idempotency-Key for publish commands and any other externally side-effecting command.
8. Use one consistent error envelope and map FastAPI validation errors into it.
9. Return 202 for asynchronous tasks and provide task/job status resources.
10. Never return ORM models directly.
11. Do not return provider keys, OAuth tokens, local installation secrets, raw authorization codes or filesystem paths.
12. OpenAPI must be generated from FastAPI/Pydantic and checked into the release/contract workflow.

### 6.1 MVP endpoint groups

Keep only the routes required for:
- health and system status;
- workspace and brand CRUD;
- AI provider configuration for the one implemented provider;
- content and variant CRUD/revisions;
- variant validation and approval;
- media upload/list/detail/association;
- one platform OAuth/account lifecycle;
- publish preflight, job creation, job status, history, retry and reconciliation;
- calendar/scheduled-job queries and schedule mutation;
- local settings, audit history, backup and restore.

Defer public API, campaign endpoints, team membership, billing, SaaS identity, advanced analytics and multi-provider orchestration.

### 6.2 Canonical schedule contract

For a one-time post:
- POST publish command creates a publish job with scheduled_at_utc and timezone.
- Immediate publish is explicit and distinct from a scheduled timestamp.
- Calendar queries publish jobs.
- Schedule edit/pause/resume/cancel routes operate on the publish job identifier.
- A separate schedules table is not required.

Recurring schedules, if introduced, require a separate recurrence model and explicit product decision.

---

## 7. Security, privacy and threat review

The existing SECURITY.md, THREAT_MODEL.md and PRIVACY.md provide a good baseline. The following are mandatory implementation controls, not documentation-only claims.

### 7.1 Critical controls

- Native secret boundary: raw local API secret remains in Rust/native code.
- OS secure storage for API keys and OAuth tokens; fail closed.
- No secrets in frontend bundles, SQLite, logs, crash reports, diagnostics or backups.
- OAuth state and PKCE verifier are short-lived and single-use.
- Minimum OAuth scopes; disconnect and revoke lifecycle.
- Human approval and exact revision verification before publish.
- No blind retries after ambiguous external outcomes.
- Safe media path confinement, magic-byte validation and resource limits.
- Prompt injection and hostile AI output treated as untrusted data.
- External data transmission disclosed before first use and at meaningful scope changes.
- No silent AI provider fallback.
- Backups and exports clearly identified as containing content/media and protected accordingly.
- Signed update artifacts and verified update metadata.
- No third-party behavioral telemetry by default.

### 7.2 Endpoint threat boundary

The threat model correctly identifies localhost as untrusted. A loopback bind and CORS are not sufficient controls.

The implementation must defend against:
- hostile websites probing localhost;
- local processes calling the API;
- CSRF and DNS-rebinding-style attacks;
- Tauri command overexposure;
- mass assignment and workspace/resource ID manipulation;
- compromised or malicious provider responses;
- malicious media and parser resource exhaustion;
- credential leakage through exceptions or diagnostics;
- compromised update artifacts.

A fully compromised user account or OS cannot be reliably defended against by a desktop application running under that same account. Document this limitation.

### 7.3 Privacy commitments

The local-first claim must be qualified:
- content and media remain local by default;
- selected prompts/content/media metadata may be transmitted to the chosen AI provider;
- publication content/media is transmitted to the selected social platform;
- optional hosting, if ever introduced, is a separate data recipient;
- data already transmitted to third parties is outside direct local deletion control;
- local content/media must not be described as encrypted at rest unless encryption is actually implemented and verified.

Retention values in PRIVACY.md are proposed defaults, not current behavior. Implement and test retention before presenting them as active product behavior.

### 7.4 Windows support

Windows 10 reached end of support on 14 October 2025. The current acceptance criteria and test plan still describe Windows 10 and Windows 11 as supported configurations. Update them to make Windows 11 the production baseline.

Windows 10 can remain a developer's experimental environment, but a release running on it must not be described as security-supported. A user operating on Windows 10 should understand that OS-level security exposure is not mitigated by PostFlow.

---

## 8. Requirements and traceability quality

### 8.1 Current state

The repository contains 96 user-story identifiers and 102 acceptance-criteria identifiers. The traceability document includes the epic/module and acceptance/test coverage structures, but explicitly says exact story-level assignments are pending reconciliation.

The current traceability baseline is therefore **not yet complete at story level**.

### 8.2 Required reconciliation

Before feature implementation is considered complete:
- Every P0 user story maps to one or more exact acceptance criteria.
- Every P0 acceptance criterion maps to an implementation module and at least one test.
- Every test ID references an existing requirement/acceptance ID.
- Every platform acceptance criterion has a platform-specific access and release gate.
- Every P0 security invariant has a negative test proving prohibited behavior is rejected.
- Deferred requirements are marked P1/FUTURE and do not remain hidden in MVP screens or API contracts.
- No provisional IDs or guessed links are accepted as traceability evidence.

### 8.3 Source-of-truth hierarchy

When documents disagree, use this order:

1. This BUILD_READINESS_REPORT.md for approved MVP scope and resolved decisions.
2. PRD.md for product-level requirements after it is updated to reflect this approval.
3. ACCEPTANCE_CRITERIA.md for testable functional acceptance.
4. USER_STORIES.md for user-facing outcomes.
5. ARCHITECTURE.md for system boundaries and architecture decisions.
6. SYSTEM_DESIGN.md and ARCHITECTURE_DIAGRAMS.md for detailed design.
7. DATABASE_SCHEMA.md and API_SPECIFICATION.md for data and API contracts.
8. SECURITY.md, THREAT_MODEL.md and PRIVACY.md for security/privacy requirements.
9. UI_UX_SPECIFICATION.md and wireframes for presentation behavior.
10. ROADMAP.md, TASK_BREAKDOWN.md and TEST_PLAN.md for delivery sequencing and verification.

This hierarchy does not permit a lower-level document to silently override a higher-level requirement. Conflicts must be recorded and reconciled.

---

## 9. Implementation sequence and prerequisites

### Gate 0 — Baseline correction (must complete before affected implementation)

- Update PRD MVP scope and product status.
- Update platform matrix and select one candidate integration.
- Update AI provider count and P0/P1 classifications.
- Resolve Windows support statement.
- Update UI navigation and defer analytics/campaigns/team functions.
- Update DB schedule model and remove MVP workspace membership/campaign/analytics dependencies.
- Finalize native API proxy and OAuth public-client/broker decision.
- Finalize first platform media delivery approach.
- Complete exact traceability mapping for P0 requirements.
- Create source-code repository structure, dependency manifests, CI and developer setup instructions.

**Exit:** Approved requirements baseline and an implementable first-platform decision record.

### M1 — Foundation

- Tauri shell and React application.
- Supervised FastAPI startup/readiness/shutdown.
- Rust-side authenticated local API proxy.
- SQLite/SQLAlchemy/Alembic baseline.
- Workspace/brand persistence.
- Secure store abstraction.
- Logging/redaction and CI.

**Exit:** Clean packaged startup, protected local API, migration and restore tests.

### M2 — Content vertical slice

- Content and revision domain.
- Variant model and validation.
- Composer and content library.
- Approval workflow.
- Audit events.

**Exit:** Create/edit/approve exact revision and prove approval invalidation after edits.

### M3 — AI and media

- One AI adapter.
- Credential lifecycle and disclosure.
- Structured output validation.
- Local media library and safe processing.

**Exit:** One real provider test and media security suite pass.

### M4 — First social integration

- Platform access and account eligibility.
- Native OAuth and secure token lifecycle.
- Capability registry.
- Media workflow.
- Controlled account test.

**Exit:** Real account and official publish permission verified. If not, keep integration disabled.

### M5 — Publishing and recovery

- Durable per-destination jobs.
- Idempotency and immutable attempts.
- Preflight and exact approval recheck.
- Retry and reconciliation.
- External post verification.

**Exit:** Controlled real publish plus fault-injection tests pass.

### M6 — Scheduling

- Persistent due-job evaluator.
- Atomic claim/lease.
- Restart recovery and missed-job UX.
- Timezone/DST policy.
- Calendar.

**Exit:** No duplicate dispatch under concurrent worker, restart and ambiguous-outcome scenarios.

### M7 — Release hardening

- Full P0 regression.
- Security/privacy verification.
- Backup/restore and migration upgrade.
- Performance on supported hardware.
- Signed installer and update validation.
- Release documentation and known limitations.

**Exit:** All release gates in Section 10 pass.

---

## 10. Build and release gates

### 10.1 Build-start gate

Implementation may start after:
- the scope decisions in Section 3 are accepted;
- contradictions R-01 through R-15 are incorporated into affected specifications or tracked as explicit pre-implementation decisions;
- a source-code project structure and CI baseline are created;
- first-platform feasibility owner and evidence plan are assigned.

Platform-independent foundation work may proceed while platform access is being evaluated. OAuth and platform-specific publishing must not be implemented against an unselected assumption.

### 10.2 MVP release gate — no waivers for these failures

| Gate | Pass condition |
|---|---|
| Runtime | Supported Windows 11 install launches and shuts down cleanly |
| Local API | Loopback only; unauthorized and hostile-origin requests rejected; secret never exposed to React |
| Data | Migrations, foreign keys, integrity checks and isolated backup restore pass |
| Content | Source/variant isolation, revision history and optimistic concurrency pass |
| Approval | Backend rejects stale, missing or mismatched approval |
| AI | One selected provider works; disclosure and secret redaction pass; no silent fallback |
| OAuth | State/PKCE and token lifecycle pass for selected platform |
| Platform | Official API permission, eligible account and live publish capability verified |
| Media | Upload workflow is supported and safe; otherwise media publishing remains disabled |
| Publishing | Idempotency, immutable attempts, partial failure and unknown-outcome reconciliation pass |
| Scheduler | Restart, worker lease, timezone and missed-run tests pass |
| Privacy | Data-flow notice matches actual network behavior and retention implementation |
| Security | No unresolved Critical or High exploitable finding |
| Packaging | Signed artifact, clean install, upgrade and updater verification pass |
| Traceability | All P0 requirements map to implementation and passing tests |

### 10.3 No-go conditions

Do not release automated publishing if:
- no platform has verified production publishing access;
- OAuth relies on an embedded confidential secret;
- approval can be bypassed through API or worker paths;
- a timeout can create an uncontrolled duplicate post;
- credentials are stored or logged in plaintext;
- backup restore cannot be verified;
- media delivery requires an unreviewed public endpoint;
- the application claims scheduling while the device is off or the worker is stopped;
- the privacy notice materially differs from actual data transmission.

---

## 11. Risk register

| Risk | Severity | Mitigation / decision | Owner |
|---|---|---|---|
| No application code in repository | Critical for implementation status | Create source tree, manifests, CI and executable vertical slice | Engineering |
| Platform API approval/access unavailable | High | Early proof of access; one platform only; manual fallback | Product / Integration |
| Public media delivery unresolved | High | Prefer supported direct upload; otherwise defer media publishing | Architecture / Integration |
| Native OAuth client-secret incompatibility | High | Public-client PKCE or separate broker; no embedded secret | Security / Integration |
| Local API secret exposed to webview | Critical | Rust-side proxy; negative tests | Security / Desktop |
| Duplicate publication after ambiguous timeout | Critical | Idempotency, attempts and reconciliation | Backend |
| Stale approval can publish | Critical | Exact revision/payload binding and pre-submit recheck | Backend |
| Windows 10 unsupported baseline | High | Windows 11 production support; explicit Windows 10 disclaimer | Product / Release |
| Scheduler unavailable while device is off | Medium | Clear limitation and missed-run recovery | Product / Backend |
| SQLite write contention | Medium | Single bounded worker, short transactions, atomic claim | Backend |
| AI/provider outage and cost | Medium | One provider, bounded requests, explicit failure states | Integration |
| Media parser vulnerabilities | High | Limits, patched libraries, isolated processing | Security |
| Requirements drift across documents | High | Source-of-truth hierarchy and change control | Product / Architecture |
| Traceability not reconciled at story level | High | Complete exact US→AC→test mapping | QA / Product |
| Scope expansion delays MVP | High | Enforce P0/P1/FUTURE boundaries | Product |

---

## 12. Required documentation changes

The following documents must be reconciled with this report. The report itself is the approved decision record until those edits are merged.

| Document | Required change |
|---|---|
| PRD.md | Replace broad initial provider/platform commitment with approved P0 scope; clarify one provider/one platform |
| PRODUCT_VISION.md | Keep long-term vision; label non-MVP capabilities explicitly |
| USER_STORIES.md | Reclassify P0/P1/FUTURE consistently; preserve long-term stories |
| ACCEPTANCE_CRITERIA.md | Correct platform/provider priorities; make unsupported platform features conditional |
| TRACEABILITY_MATRIX.md | Complete exact story-level mapping and mark deferred items |
| ARCHITECTURE.md | Record Rust-side API proxy, native OAuth and one-worker runtime |
| SYSTEM_DESIGN.md | Align schedule, OAuth, media and local secret handling |
| ARCHITECTURE_DIAGRAMS.md | Update trust boundaries, media flow, native API proxy and schedule ownership |
| DATABASE_SCHEMA.md | Defer membership/campaign/analytics tables; canonicalize one-time schedules |
| API_SPECIFICATION.md | Align schedule routes with publish_jobs; restrict MVP endpoints; document native proxy |
| UI_UX_SPECIFICATION.md | Hide/defer advanced analytics, campaign, collaboration and unsupported integrations |
| SECURITY.md | Explicit native secret boundary and public-client OAuth decision |
| THREAT_MODEL.md | Include native proxy, broker contingency and media hosting decision |
| PRIVACY.md | Ensure no unimplemented retention or encryption claim is presented as active behavior |
| FEASIBILITY_REPORT.md | Make Windows 11 production baseline explicit and revalidate resource budgets after prototype |
| PLATFORM_API_RESEARCH.md | Add chosen platform decision record with current access/permission evidence |
| ROADMAP.md | Reflect one-provider/one-platform MVP and build-start gate |
| TASK_BREAKDOWN.md | Reorder tasks to complete decision records before integration implementation |
| TEST_PLAN.md | Align OS matrix, schedule model, OAuth model and exact traceability references |

---

## 13. Final approval record

### Approved

- Local-first Windows desktop product direction.
- Single-user desktop deployment profile.
- Tauri 2 + React/TypeScript + FastAPI + SQLite modular monolith.
- One cloud AI provider for first MVP.
- One real social publishing integration at most, subject to external access gate.
- Source content, independent variants and revision history.
- Local media library with platform-specific upload validation.
- Human approval before every first-MVP external publication.
- Durable, idempotent publishing jobs and unknown-outcome reconciliation.
- Local persistent scheduling with explicit runtime limitation.
- Local operational dashboard, backup/restore, audit and privacy controls.
- Separate future SaaS architecture and scope.

### Deferred / not approved for MVP

- Four-provider production integration commitment.
- Seven-platform automated publishing commitment.
- Automatic AI provider fallback.
- Campaign management.
- Advanced social analytics.
- Team collaboration and approval roles.
- Cloud scheduling, distributed workers and SaaS infrastructure.
- Public media relay without a separate security/privacy approval.
- Auto-publishing without human approval.

### Conditions before implementation of integrations

1. Select the first platform with verified developer access, account eligibility, scopes and live publishing capability.
2. Confirm native OAuth support or approve a separately hosted broker.
3. Prove the selected platform's media upload flow; otherwise constrain media publishing.
4. Implement the Tauri-native API proxy so React never receives the local API secret.
5. Reconcile all P0 story/acceptance/test mappings.
6. Update conflicting documents and establish the source-code/CI baseline.

<badge color="warning">Conditional GO</badge>

**Product scope is approved as defined in this report.** Platform-specific implementation remains gated by external API feasibility and the security decisions above. Production release remains NO-GO until every applicable release gate passes.

**Approval meaning:** This is a technical/product baseline recommendation for the repository owner. It is not a substitute for the product owner's explicit sign-off, legal review, platform authorization or test evidence.
