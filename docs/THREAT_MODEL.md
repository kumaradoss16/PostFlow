# PostFlow Threat Model

**Document:** THREAT_MODEL.md  
**Version:** 1.0  
**Status:** Proposed threat assessment; validate continuously during implementation  
**Method:** Asset / trust-boundary analysis with STRIDE and attack-scenario prioritization  
**Related documents:** SECURITY.md, PRIVACY.md, SYSTEM_DESIGN.md, API_SPECIFICATION.md

## 1. Purpose

This threat model identifies assets, actors, trust boundaries, abuse cases, and mitigations for PostFlow's local-first desktop architecture. It is a living engineering artifact, not a penetration-test report or proof that mitigations are implemented.

The initial threat model assumes a single-user Windows desktop deployment with Tauri 2, React/TypeScript, FastAPI, SQLite, a persistent worker, local media storage, OS-backed secrets, and outbound integrations with AI providers and social platforms. The future SaaS deployment has materially different risks and must undergo a separate threat-model review before launch.

## 2. System and security assumptions

### 2.1 Components

- Desktop shell: Tauri 2.
- UI: React + TypeScript webview.
- Local API: FastAPI bound to loopback.
- Application/domain services: Python modular monolith.
- Persistence: SQLite via SQLAlchemy/Alembic.
- Worker: persistent scheduler and publishing executor.
- Secret storage: Windows Credential Manager / DPAPI-backed integration.
- Media: local filesystem, Pillow, FFmpeg.
- External services: OpenAI, Gemini, Claude, Perplexity, and social platform APIs.

### 2.2 Assumptions

- The OS account and device are not already fully compromised.
- External services may be unavailable, maliciously configured, or return malformed content.
- Localhost is reachable by other local processes and potentially by hostile browser contexts; loopback is not a trust boundary by itself.
- User-imported media and AI-generated content are untrusted.
- OAuth scope and platform publishing behavior can change.
- A desktop scheduler cannot execute while the computer is powered off, asleep, offline, or the application worker is stopped.
- OS administrators and malware running with the user's privileges may be able to inspect process memory or use the user's credential context. The desktop application cannot fully defend against a compromised endpoint.

## 3. Assets and security objectives

| Asset | Examples | Security objective |
|---|---|---|
| Social credentials | Access/refresh tokens | Confidentiality, integrity, revocability |
| AI credentials | Provider API keys | Confidentiality, least privilege, controlled use |
| Local API secret | Installation bearer token | Prevent unauthorized local API calls |
| User content | Drafts, variants, campaigns | Confidentiality, integrity, availability |
| Media | Images, video, exports | Integrity, safe processing, controlled access |
| Publishing authority | Account scopes and approval state | Prevent unauthorized publication |
| Job state | Scheduled jobs, attempts, external IDs | Integrity, consistency, recoverability |
| Workspace data | Brands, accounts, settings | Isolation and authorization |
| Audit trail | Approval and credential events | Integrity, accountability |
| Backups | DB and media archives | Confidentiality, integrity, recoverability |
| Update artifacts | Installer and updater metadata | Authenticity and integrity |

Primary security outcomes: no credential disclosure; no unauthorized/cross-workspace access; no unapproved publication; no duplicate publish caused by unsafe retries; no silent third-party data transfer; recoverable local data.

## 4. Threat actors

| Actor | Capability / motivation |
|---|---|
| Malicious local process | Probe loopback API, read accessible files, abuse browser-to-localhost behavior |
| Malicious website | Attempt CSRF, localhost request abuse, deep-link manipulation |
| Malware under user account | Read user files, invoke credential store, inspect process or automate UI |
| Malicious/imported document | Exploit parser, path traversal, resource exhaustion |
| Malicious AI output | Prompt injection, unsafe links, deceptive instructions, HTML/script payload |
| Compromised AI provider or platform | Return hostile content, misuse data, leak or abuse credentials |
| External attacker | Exploit exposed service, dependency, update, OAuth callback, or API |
| Insider / future workspace member | Exceed role permissions, access another workspace, publish without approval |
| Supply-chain attacker | Compromise npm/PyPI/Rust dependency, build pipeline, or update artifact |

## 5. Trust boundaries and data-flow risks

| Boundary | Main threat | Required defense |
|---|---|---|
| Webview → Tauri commands | Privilege escalation through exposed command | Minimal command surface, typed inputs, capability allowlist |
| Browser/webview → localhost API | CSRF, DNS rebinding, local API abuse | Random auth token, Origin validation, loopback bind, strict CORS |
| Frontend → backend DTOs | Mass assignment, hidden-field manipulation | Strict schemas, server-side authorization |
| Backend → SQLite | SQL injection, tenant/workspace bypass | Parameterized queries, repository scope checks, FK constraints |
| Backend → secret store | Credential theft or accidental disclosure | OS-backed store, opaque references, redaction |
| Worker → platform APIs | Token theft, duplicate publish, scope overreach | Adapter isolation, TLS, least scopes, idempotency, reconciliation |
| Backend → AI provider | Prompt/data disclosure, provider fallback | Consent, data minimization, explicit provider, disclosure |
| Filesystem → media parser | Malformed file, traversal, decompression bomb | Path confinement, magic bytes, resource limits, patched libraries |
| Update channel → desktop | Malicious update / rollback | Signed artifacts, signature verification, secure update metadata |
| Backup/export → user destination | Data leakage | Explicit selection, warnings, restrictive permissions, integrity checks |

## 6. STRIDE analysis

| Threat category | Example PostFlow threat | Risk | Mitigations |
|---|---|---|---|
| Spoofing | Attacker impersonates local API caller or OAuth callback | High | Per-installation secret, Origin checks, one-time OAuth state, PKCE |
| Tampering | Change variant after approval or alter job state | Critical | Revision-bound approval, transactional state transitions, audit events, integrity checks |
| Repudiation | User denies approving or initiating publication | High | Append-only audit events, actor/correlation IDs, timestamps, immutable attempt records |
| Information disclosure | API key/token appears in DB, logs, frontend, backup | Critical | OS secret store, DTO redaction, log filters, file permissions, secret scans |
| Denial of service | Huge media, AI request loops, local API flooding | Medium/High | Limits, timeouts, concurrency caps, bounded queues, cancellation |
| Elevation of privilege | Viewer/admin boundary bypass in future SaaS | Critical | Service-layer authorization, deny-by-default policy, tenant isolation tests |

Risk labels are initial qualitative priorities. Re-score based on exploitability, exposure, business impact, and implementation evidence.

## 7. Prioritized attack scenarios

### TM-01 — Localhost API abuse / CSRF

**Scenario:** A hostile website or local process sends requests to the local FastAPI service and attempts to connect accounts, read data, alter content, or schedule publication.

**Impact:** Unauthorized data access or publishing.

**Initial severity:** Critical.

**Mitigations:**
- Bind only to 127.0.0.1.
- Require a random per-installation bearer secret for every non-health endpoint.
- Keep the secret out of browser storage and frontend bundles.
- Validate Origin and reject unexpected origins; do not rely on CORS alone.
- Use strict content types, no permissive credentialed CORS, request-size limits, and rate limits.
- Keep Tauri command surface narrow and do not expose a generic arbitrary HTTP or secret-read command.

**Verification:** Browser-origin request tests, missing/invalid token tests, DNS-rebinding-oriented Host/Origin tests, and confirmation that the service is not reachable from another LAN device.

### TM-02 — OAuth state forgery, replay, or callback interception

**Scenario:** An attacker injects a callback, replays an authorization response, swaps accounts, or tricks the app into binding an unintended account.

**Impact:** Account takeover or publication to an attacker-controlled destination.

**Initial severity:** Critical.

**Mitigations:** High-entropy single-use state; short expiry; binding to platform, redirect URI, and initiating session; PKCE S256; strict callback validation; server-side code exchange; exact redirect allowlist; account identity confirmation; no tokens in deep links/logs.

**Verification:** Missing, expired, replayed, mismatched-platform, wrong-redirect, and duplicate-callback tests.

### TM-03 — Credential exposure

**Scenario:** AI key, OAuth token, refresh token, or local API secret leaks through SQLite, config files, logs, telemetry, crash dumps, UI state, or support bundles.

**Impact:** Unauthorized AI spend, account compromise, data access, and publishing abuse.

**Initial severity:** Critical.

**Mitigations:** OS-backed secure storage; database contains opaque references only; write-only credential APIs; response masking; centralized redaction; no raw headers/body logging; secret scanning; credential rotation and revocation guidance.

**Verification:** Canary-secret tests across DB, logs, exports, frontend bundle, crash/support output, and API responses.

### TM-04 — Stale approval / content tampering

**Scenario:** A user approves a variant, then content, media, destination, or scheduling payload changes before publication while the old approval remains valid.

**Impact:** Unintended or harmful publication.

**Initial severity:** Critical.

**Mitigations:** Monotonic revision; approval records exact revision; content-affecting edits invalidate approval; enqueue and pre-submit revision checks; approval summary binds platform/account/media; audit all decisions.

**Verification:** Edit-after-approve tests for caption, hashtags, link, media, destination, and material schedule changes. Every changed payload must require renewed approval.

### TM-05 — Duplicate publication after ambiguous timeout

**Scenario:** Platform accepts a post but response is lost; worker assumes failure and retries.

**Impact:** Duplicate posts, brand damage, rate-limit penalties.

**Initial severity:** High.

**Mitigations:** Stable idempotency identity where platform supports it; immutable attempt history; request fingerprint; state transitions to unknown/reconciling; query platform state where possible; manual resolution if outcome cannot be proven. Never blindly retry ambiguous submissions.

**Verification:** Simulate accepted request + lost response, worker crash after submission, and restart during reconciliation. Confirm no automatic duplicate submission.

### TM-06 — Malicious media / parser exploitation

**Scenario:** Uploaded image/video uses malformed structure, decompression bomb, oversized dimensions, path traversal filename, or vulnerable codec.

**Impact:** Code execution, app crash, data overwrite, resource exhaustion.

**Initial severity:** High.

**Mitigations:** File-size and decoded-dimension limits; MIME allowlist plus magic-byte validation; generated storage names; canonical path confinement; patched Pillow/FFmpeg; restricted subprocess; CPU/memory/time/output limits; optional malware scanning where available.

**Verification:** Polyglot, malformed, oversized, traversal, and decompression-bomb fixtures; ensure parser runs do not escape media root or exhaust system resources.

### TM-07 — Prompt injection and unsafe AI output

**Scenario:** Imported content or retrieved webpage instructs the model to disclose secrets, alter settings, call tools, or publish malicious content.

**Impact:** Data exfiltration, misleading content, unauthorized action.

**Initial severity:** High.

**Mitigations:** Treat source documents and model output as untrusted; separate system policy from content; do not give generation tools access to credentials; require human approval for external actions; validate structured output; escape rendered text; do not execute generated code/HTML; provider calls limited to disclosed content.

**Verification:** Prompt-injection corpus; tests proving AI output cannot read secrets, call publishing directly, bypass approval, or invoke arbitrary filesystem/network tools.

### TM-08 — Cross-workspace access (future SaaS)

**Scenario:** User changes workspace/resource IDs to read or modify another tenant's content, accounts, jobs, or media.

**Impact:** Multi-tenant data breach.

**Initial severity:** Critical for SaaS.

**Mitigations:** Workspace/tenant ID derived from authenticated server context; scope every repository query; enforce authorization in service layer; avoid trusting client-supplied workspace IDs; test object-level authorization on every resource route; isolate object storage and background jobs by tenant.

**Verification:** Automated horizontal and vertical authorization tests; cross-tenant ID substitution tests for all endpoints and job workers.

### TM-09 — Excessive OAuth scopes / platform policy drift

**Scenario:** App requests broad scopes or continues publishing after platform permission changes.

**Impact:** Increased blast radius, app review rejection, account restrictions.

**Initial severity:** High.

**Mitigations:** Minimal scopes; per-capability mapping; dated platform evidence; capability health checks; reauthorization when scopes change; disable unsupported operations; user-facing explanation.

**Verification:** Scope-diff tests and platform integration release checklist.

### TM-10 — SSRF through URL import or remote media fetch

**Scenario:** User or AI-supplied URL targets localhost, private network, cloud metadata service, or redirects to internal resources.

**Impact:** Local service probing, data theft, network pivot.

**Initial severity:** High if remote fetch exists.

**Mitigations:** Prefer no server-side arbitrary URL fetch in MVP. If added, allow only HTTP/HTTPS, block private/loopback/link-local/multicast/reserved ranges, validate resolved IPs at connection time, revalidate redirects and DNS, limit redirects/time/bytes, and use egress controls.

**Verification:** Test localhost, RFC1918, IPv6 local, metadata, DNS rebinding, redirect, and mixed-address responses.

### TM-11 — Supply-chain or malicious update

**Scenario:** Compromised dependency, build workflow, package registry, or update metadata delivers malicious code.

**Impact:** Full local account/data compromise.

**Initial severity:** Critical.

**Mitigations:** Dependency pinning and review; lockfiles; SBOM; secret-protected CI; protected release workflow; signed artifacts; signature verification; least-privilege build tokens; dependency advisory monitoring; reproducible build evaluation.

**Verification:** Signature rejection tests, dependency scan gates, CI permission review, and release provenance review.

### TM-12 — Backup theft or unsafe restore

**Scenario:** Backup contains content and account metadata and is copied to an untrusted location; restore replaces the wrong database or imports tampered data.

**Impact:** Privacy breach, data corruption, credential reference mismatch.

**Initial severity:** High.

**Mitigations:** Explicit export destination and confirmation; restrictive file permissions; never export secret values; manifest and integrity hashes; restore preview; schema compatibility checks; pre-restore backup; transactional/atomic replacement where feasible.

**Verification:** Backup contents inspection, tampered archive rejection, wrong-version restore, and recovery drill.

### TM-13 — Audit log tampering or sensitive logging

**Scenario:** Application logs include secrets or an attacker with local file access alters audit history.

**Impact:** Credential disclosure or unreliable incident evidence.

**Initial severity:** High.

**Mitigations:** Redaction before serialization; append-only application semantics; restricted ACLs; rotation/retention; structured events; correlation IDs. Clearly state that local audit logs are not tamper-proof against an administrator.

**Verification:** Secret canary scan; CR/LF injection tests; attempted mutation tests; retention and export tests.

### TM-14 — Scheduler abuse / auto-publish misconfiguration

**Scenario:** A user unintentionally enables broad automation, or a compromised UI schedules content without approval.

**Impact:** Large-scale unintended publication.

**Initial severity:** High.

**Mitigations:** Auto-publish off by default; scoped automation rules; explicit confirmation; approval policy enforced in backend; maximum queue limits; pause-all control; audit event; visible preview of account/platform/time.

**Verification:** API-level tests bypassing UI; default-off assertion; automation scope tests; emergency pause tests.

## 8. Risk register and prioritization

| ID | Threat | Initial priority | Release requirement |
|---|---|---|---|
| TM-01 | Local API abuse | Critical | Must mitigate and test |
| TM-02 | OAuth callback/state abuse | Critical | Must mitigate and test before account connection |
| TM-03 | Secret exposure | Critical | Must mitigate and test before provider integrations |
| TM-04 | Stale approval | Critical | Must mitigate and test before publishing |
| TM-05 | Duplicate publish | High | Reconciliation required before public publishing |
| TM-06 | Malicious media | High | Limits and path isolation before media import |
| TM-07 | Prompt injection | High | No direct action authority for AI; approval required |
| TM-08 | Cross-workspace access | Critical SaaS | Must be resolved before multi-tenant release |
| TM-09 | Scope/policy drift | High | Platform evidence and review required |
| TM-10 | SSRF | High if URL fetch | Disable or mitigate before enabling URL fetch |
| TM-11 | Supply chain/update | Critical | Signed release and dependency controls |
| TM-12 | Backup/restore | High | Recovery and privacy tests before release |
| TM-13 | Audit integrity/redaction | High | Redaction tests and retention before release |
| TM-14 | Auto-publish misuse | High | Explicit controls and API-level enforcement |

Risk is not accepted merely because a feature is marked MVP. Any residual Critical risk requires a documented owner, rationale, compensating controls, expiry date, and explicit release authorization. High risks require the same treatment or a verified mitigation plan.

## 9. Abuse cases and security test scenarios

- A web page sends POST requests to localhost without the installation token.
- A valid token is submitted from an unexpected Origin.
- OAuth callback is replayed after successful account connection.
- OAuth callback contains a mismatched state or redirect URI.
- Provider credential is added, then searched in SQLite, logs, API responses, exports, and UI state.
- User modifies an approved post after approval and before scheduled execution.
- Worker crashes after platform accepts publication but before local success is persisted.
- A file named with ../ or an absolute path is uploaded.
- A valid image extension contains a different binary format.
- AI response includes script/HTML, tool directives, or prompt-injection text.
- User changes resource IDs to another workspace's resource.
- Restore is attempted from a modified or incompatible backup.
- Automation is enabled through a direct API call without the required confirmation state.

Each scenario must have an automated test where practical, a manual test procedure where automation is impractical, and an evidence artifact attached to the release record.

## 10. Residual risks and limitations

- A compromised OS account can often access data available to that account, including invoking credential-store APIs or inspecting application memory.
- Local audit logs cannot guarantee non-repudiation against a privileged local attacker.
- Desktop scheduling is not cloud scheduling: the device and worker must be awake and running.
- Platform APIs may not expose reliable publish reconciliation or idempotency. Where they do not, the app must surface uncertainty and require manual resolution rather than claim exactly-once delivery.
- AI providers may retain or process submitted data under their own terms. PostFlow cannot guarantee provider-side deletion unless the provider contract and API support it.
- OAuth tokens and app permissions can be revoked or changed externally.
- Windows 10 is out of support; use a supported OS for production.
- Future SaaS requires a separate threat model for tenant isolation, web sessions, identity, cloud storage, service-to-service credentials, backups, and operations.

## 11. Review cadence and change triggers

Review this threat model:
- Before first public release.
- Before adding a new AI provider or social platform.
- Before enabling remote URL fetch, browser automation, plugins, or arbitrary tools.
- Before adding collaboration, SaaS, or cloud synchronization.
- After a material architecture change, security incident, or critical dependency advisory.
- At least once per major release cycle.

A threat is closed only when its mitigation is implemented and verification evidence exists. Documentation alone is not mitigation.
