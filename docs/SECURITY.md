# PostFlow Security Architecture and Controls

**Document:** SECURITY.md  
**Version:** 1.0  
**Status:** Proposed implementation and release baseline  
**Product profile:** Local-first Windows desktop application; future SaaS profile is separately scoped  
**Related documents:** SYSTEM_DESIGN.md, DATABASE_SCHEMA.md, API_SPECIFICATION.md, THREAT_MODEL.md, PRIVACY.md

## 1. Purpose and security objectives

This document defines the security architecture and mandatory controls for PostFlow. It is an engineering specification, not a claim that controls have already been implemented or independently audited.

Security objectives:

1. Protect social-account OAuth tokens, AI-provider API keys, local API credentials, and user content.
2. Prevent unauthorized publication, account takeover, cross-workspace access, and duplicate publication.
3. Make external data transmission explicit, purpose-limited, and user-controlled.
4. Preserve evidence of security-relevant actions without logging secrets or unnecessary personal data.
5. Keep the desktop MVP operational without requiring cloud infrastructure.
6. Define a separate security boundary for any future multi-tenant SaaS deployment.

Security principles: least privilege, secure defaults, defense in depth, explicit consent, fail closed, data minimization, auditable state transitions, and no silent credential or provider fallback.

## 2. Scope, assumptions, and non-goals

### 2.1 In scope

- Tauri 2 desktop shell and React/TypeScript UI.
- Local FastAPI service and background publishing worker.
- SQLite database and local media storage.
- OS-backed credential storage.
- OAuth authorization and refresh lifecycle for social accounts.
- AI-provider API-key handling and outbound AI requests.
- Publishing approvals, scheduling, retries, and reconciliation.
- Logs, diagnostics, backups, updates, and user privacy controls.

### 2.2 Assumptions and constraints

- The desktop application runs under the logged-in OS user.
- The backend binds only to loopback and is not an Internet-facing service.
- Secrets are stored using Windows Credential Manager / DPAPI-backed facilities through a maintained secure-storage integration. Equivalent OS-backed facilities must be selected for any later supported OS.
- The desktop application cannot protect secrets from malware or an attacker who already controls the user's OS account or has administrator-level access.
- Platform OAuth scopes, app review, API availability, commercial terms, and publishing capabilities vary by platform and must be verified against current official documentation before implementation.
- Windows 10 reached end of support on 14 October 2025. A supported Windows release is the recommended production environment; any continued Windows 10 support requires a documented risk acceptance and supported patching strategy.

### 2.3 Out of scope

This document does not certify compliance with GDPR, India DPDP Act, CCPA/CPRA, SOC 2, ISO 27001, or any platform policy. Legal applicability and obligations require jurisdiction-specific review. It does not define a full enterprise identity provider, endpoint detection platform, or managed key-management service for the desktop MVP.

## 3. Trust boundaries and data flows

| Boundary | Data crossing it | Required controls |
|---|---|---|
| React UI ↔ Tauri shell | User actions, local API access | Tauri capability allowlist, strict CSP, no arbitrary shell execution |
| Tauri shell ↔ FastAPI | Local requests and responses | Loopback-only bind, per-installation authentication, origin validation, request limits |
| FastAPI ↔ SQLite | Content, account metadata, job state | Parameterized ORM queries, workspace authorization, file permissions, migrations |
| Backend ↔ OS credential store | Secret read/write operations | OS user context, opaque references, access restricted to app process/user |
| Worker ↔ social platforms | OAuth credentials, content, media | HTTPS, minimum scopes, account-level consent, rate limits, safe retries |
| Backend ↔ AI providers | Prompts, source content, optional media | Provider disclosure, explicit provider selection, no silent fallback, minimization |
| App ↔ local filesystem | Media, exports, backups, logs | Canonical paths, safe filenames, restrictive ACLs, integrity checks |
| Desktop ↔ update channel | Signed application packages | Authenticated update metadata, signature verification, rollback protection where feasible |

Never treat the frontend, imported media, provider output, platform responses, or local HTTP callers as inherently trusted.

## 4. Authentication and local API protection

### 4.1 Local API

- Bind FastAPI to 127.0.0.1 only. Never bind the desktop profile to 0.0.0.0 or a LAN interface.
- Use an OS-generated cryptographically secure random installation secret with at least 256 bits of entropy.
- Store the secret in OS-backed secure storage. Do not embed it in frontend bundles, source control, config files, SQLite, logs, crash reports, or browser localStorage/sessionStorage.
- Provision the secret to the trusted desktop runtime through a protected IPC mechanism. Do not expose a generic credential-read command to arbitrary web content.
- Require authentication for every endpoint except minimal liveness/readiness responses that disclose no configuration or user data.
- Validate Origin and, where applicable, Tauri webview identity; reject unexpected browser origins and cross-origin requests.
- Use strict CORS (prefer no permissive CORS for the desktop API), request-size limits, timeouts, and rate limits.
- Rotate the installation secret on security reset, suspected compromise, or credential-store reinitialization. Rotation must invalidate the old secret.
- Use constant-time comparison for secret verification and avoid secret-dependent error detail.

Loopback binding alone is not authentication: other local processes and browser contexts may attempt to reach the service.

### 4.2 User authentication and SaaS distinction

The desktop MVP may use a single local OS-user profile and does not need a cloud identity provider. Workspace ownership checks remain mandatory. A future SaaS profile must add server-side user authentication, MFA options, session management, tenant isolation, account recovery, abuse controls, and role-based authorization. Never treat a desktop installation token as a SaaS user identity.

## 5. OAuth and social-account security

### 5.1 Authorization flow

1. User selects a platform and account connection action.
2. Backend creates a high-entropy, one-time OAuth state value, binds it to the initiating local session, platform, redirect URI, and short expiry.
3. Use PKCE with S256 whenever supported; use the platform's current recommended authorization-code flow.
4. Open the authorization URL using the system browser where the platform flow requires it.
5. Validate callback state exactly once; reject missing, expired, replayed, mismatched, or wrong-platform state.
6. Exchange the authorization code server-side over TLS. Never exchange client secrets in the frontend.
7. Validate issuer/authorization server metadata and redirect URI according to the provider's supported protocol.
8. Store access and refresh tokens in OS-backed secure storage. Persist only opaque secret references and non-secret metadata in SQLite.
9. Display the connected account identity and granted scopes. If granted scopes differ from required scopes, mark the integration limited and do not assume full capability.
10. Record a redacted audit event.

OAuth state must be unpredictable, single-use, short-lived, and bound to the initiating operation. Do not put access tokens or refresh tokens in deep links, query strings, logs, analytics, or browser storage.

### 5.2 Scope and account lifecycle

- Request only scopes needed for the user-selected features.
- Separate read, publish, media-upload, and analytics permissions where platform scopes permit.
- Explain the purpose of requested permissions before authorization.
- Do not request broad account-management scopes merely for convenience.
- Track token expiry, granted scopes, account identity, connection status, and last successful verification.
- Refresh tokens server-side, serialize concurrent refresh attempts, and atomically replace rotated tokens.
- Treat invalid_grant, revoked consent, or refresh-token reuse alerts as a disconnected/re-authentication state.
- Provide explicit disconnect and revoke instructions. Remove local token material and attempt remote revocation where supported.
- Never infer that a successful OAuth connection means publishing is approved or supported.

### 5.3 Platform capability verification

Maintain a platform capability registry that records verified API operations, account eligibility, required scopes, media constraints, review status, and evidence date. Do not expose a publish action as available solely because a platform name appears in the UI. Revalidate platform policies and API versions before release.

## 6. AI-provider API-key management

- Accept API keys only through a dedicated credential-entry flow over the authenticated local API.
- Write the secret directly to OS-backed secure storage. Store only a secret reference, provider identifier, status, and timestamps in SQLite.
- Never return the stored key. API responses may return masked metadata such as configured=true and last_verified_at.
- Never include credentials in prompts, provider request logs, telemetry, exception messages, support bundles, or audit details.
- Do not persist raw Authorization headers or provider error bodies.
- Restrict credential retrieval to the provider adapter service. Do not expose a general-purpose endpoint that returns secret values.
- Support replace, test, disable, and delete operations. Test calls must be clearly identified because they transmit a request to the provider.
- If a key is rotated or invalidated, mark the provider unavailable and request user action; do not silently use another provider.
- Do not place provider keys in environment variables for normal desktop runtime unless a documented development-only mode is used and clearly isolated.

A secret-store failure must fail closed. Do not fall back to plaintext SQLite, JSON configuration, or a local .env file.

## 7. Authorization and permission model

### 7.1 Desktop MVP

The local profile is the installation owner. Every request still resolves workspace ownership and resource relationships. UI hiding is not authorization. Application services must enforce permissions before reading or mutating workspace data.

### 7.2 Future SaaS roles

| Role | Read | Create/edit content | Approve | Publish/schedule | Manage accounts/credentials | Manage workspace |
|---|---:|---:|---:|---:|---:|---:|
| Owner | Yes | Yes | Yes | Yes | Yes | Yes |
| Admin | Yes | Yes | Yes | Yes | Yes, subject to re-auth | Yes, except transfer/delete owner |
| Editor | Yes | Yes | No by default | No by default | No | No |
| Approver | Yes | No by default | Yes | No by default | No | No |
| Publisher | Yes | Limited | No | Yes, only approved revision | No | No |
| Viewer | Yes, read-only | No | No | No | No | No |

Roles are a starting policy, not an authorization shortcut. Enforce workspace membership, resource ownership, action-specific permission, and account-level restrictions on every request. Support configurable role policy only after tests cover privilege escalation and conflicting assignments.

## 8. Approval gates and publishing safety

### 8.1 Revision-bound approval

- Every post variant has a monotonically increasing revision.
- Approval records the exact approved revision, approver, timestamp, and decision.
- Any content-affecting edit increments the revision and invalidates prior approval.
- The publishing command must verify that approved_revision equals the current variant revision at enqueue time and again immediately before external submission.
- Destination account, platform, media, caption, and scheduled time must be included in the review summary.
- A material change to destination, media, or payload invalidates approval or requires a new explicit confirmation according to the product policy.
- AI-generated content is untrusted input and must never publish itself.

### 8.2 Default policy

- Human approval is required before the first external publication.
- Auto-publish is disabled by default.
- Enabling an automation rule requires an explicit user action, a visible scope summary, and an audit event.
- High-impact actions (connect account, grant permissions, enable auto-publish, delete account data, restore backup, revoke credentials) require clear confirmation; re-authentication may be required where supported.
- Approval UI must not use preselected consent or misleading button labels.

### 8.3 Reliable execution

- Each destination is a separate publish job with immutable attempt history.
- Use an idempotency key and stable request fingerprint.
- Do not hold database transactions open during external network calls.
- On timeout after submission, mark outcome unknown and reconcile with platform state before retry.
- Never automatically retry an ambiguous result.
- Retry only definitive transient failures and respect Retry-After and platform rate limits.
- Record who initiated, approved, scheduled, retried, cancelled, or reconciled the job.
- Cancellation after the external request is accepted is best-effort; report this accurately.

## 9. Data protection and cryptography

- Use TLS with certificate validation for all external provider and platform calls.
- Use OS-backed encryption for secrets; do not invent or roll custom cryptography.
- Protect local database, media, backups, and logs with OS filesystem permissions. Explain that local content encryption at rest is not provided unless a separately reviewed encryption design is implemented.
- If an encrypted database or backup feature is introduced, use a vetted library and authenticated encryption with versioned keys; document recovery and key-loss consequences.
- Use SHA-256 for media integrity/deduplication, not as a password hash.
- If SaaS passwords are introduced, use a modern password hashing scheme such as Argon2id through a maintained library; prefer a managed identity provider where appropriate.
- Minimize sensitive data in memory and clear temporary buffers where practical, while recognizing Python/runtime copies may not be reliably zeroized.
- Backups must have restrictive permissions and must not silently upload to a cloud destination.

## 10. Input, output, and media security

- Validate all API input with strict Pydantic schemas; reject unexpected fields on security-sensitive endpoints.
- Enforce domain validation separately from type validation.
- Treat AI output, imported files, filenames, image metadata, video metadata, platform responses, and URLs as untrusted.
- Normalize filenames; generate storage names; never use user-supplied path fragments as storage paths.
- Resolve paths and verify they remain inside the configured media root.
- Enforce MIME allowlists, file-size limits, magic-byte checks, extension consistency, and image/video decoding limits.
- Process media in a restricted subprocess where feasible; set CPU, memory, duration, and output-size limits.
- Keep FFmpeg and image libraries patched. Avoid shell command interpolation; pass argument arrays to subprocesses.
- Block or explicitly gate remote URL fetching to prevent SSRF. If URL import is implemented, block loopback, private, link-local, multicast, and metadata-service ranges; re-check DNS and redirects.
- Escape user content in UI rendering; never render provider output as trusted HTML.
- Do not execute generated code, scripts, HTML, or tool instructions from AI output.

## 11. Audit logging and observability

### 11.1 Events to record

- Account connect, disconnect, scope change, token refresh failure, and credential deletion.
- Provider credential create, replace, test, disable, and delete.
- Workspace and role changes (SaaS).
- Content approval/rejection and revision invalidation.
- Auto-publish setting changes.
- Publish enqueue, claim, attempt, success, failure, retry, cancellation, and reconciliation.
- Backup, restore, export, data deletion, and security-setting changes.
- Authentication failures and suspicious request patterns.

### 11.2 Audit record format

Record timestamp (UTC), actor or system identity, action, resource type/id, workspace, correlation ID, outcome, and a minimal redacted detail object. Use append-only semantics at the application layer and restrict mutation permissions. For stronger tamper evidence in SaaS, evaluate immutable external log storage and hash chaining; local audit rows alone are not tamper-proof against an OS administrator.

Never log access tokens, refresh tokens, API keys, client secrets, local API tokens, full authorization headers, raw provider request bodies, or unnecessary full post content. Sanitize CR/LF and control characters to prevent log injection. Define retention and export controls in PRIVACY.md.

## 12. Secure development and release controls

- Pin and update dependencies; review advisories for Tauri, Rust crates, npm packages, Python packages, Pillow, and FFmpeg.
- Generate and review an SBOM for release artifacts.
- Run secret scanning, dependency scanning, static analysis, and license checks in CI.
- Build with production debug settings disabled; do not ship development server or test credentials.
- Sign release artifacts and verify update signatures.
- Restrict Tauri capabilities and CSP; prohibit unrestricted shell, filesystem, and HTTP permissions.
- Use parameterized SQL and safe ORM patterns.
- Review all new outbound data flows and permissions before merging.
- Test backup/restore, credential deletion, OAuth state replay, local API origin/auth checks, workspace isolation, approval invalidation, and unknown publish outcome recovery.
- Perform security review before enabling a new platform or provider integration.
- Maintain a vulnerability-reporting contact and a documented triage process before public release.

### Release-blocking conditions

A release must be blocked if any of the following is true:

1. Any API key, OAuth token, or local API secret is stored in plaintext in SQLite, files, source, logs, or frontend storage.
2. The local API listens on a non-loopback interface without an explicitly approved architecture change.
3. OAuth state replay or callback mismatch is accepted.
4. Cross-workspace access is possible.
5. A changed revision can publish using stale approval.
6. An ambiguous publishing result is blindly retried.
7. A user can enable auto-publishing without explicit informed confirmation.
8. Secret-bearing diagnostics or support bundles can be exported.
9. Critical/high exploitable vulnerabilities remain without documented risk acceptance.
10. Backup restore can overwrite data without explicit confirmation and integrity checks.

## 13. Incident response

1. Contain: disable affected provider/account integration, revoke tokens or rotate keys, and pause scheduled jobs where needed.
2. Preserve: retain relevant redacted audit events and diagnostic evidence; do not copy secrets into incident tickets.
3. Assess: identify affected workspaces, accounts, data types, time window, and external disclosures.
4. Notify: determine platform, contractual, and legal notification obligations with qualified counsel; do not promise a fixed notification period without confirming applicability.
5. Recover: rotate credentials, patch, restore from verified backup if necessary, and reconcile publication state.
6. Learn: document root cause, corrective actions, owners, and verification tests.

## 14. Security acceptance checklist

- [ ] Local API loopback bind, authentication, Origin validation, and request limits verified.
- [ ] OAuth state, PKCE, redirect URI, scope, token refresh, and revocation paths tested.
- [ ] Secrets stored only in OS-backed secure storage.
- [ ] No secret values returned by API or exposed to frontend.
- [ ] Workspace and role checks applied in service layer.
- [ ] Approval is revision-bound and rechecked before publish.
- [ ] Unknown publish outcome enters reconciliation.
- [ ] Media paths, MIME, magic bytes, and processing limits tested.
- [ ] Audit logs are redacted and retention is configured.
- [ ] Backup/export and deletion behavior verified.
- [ ] Dependency, secret, and release-signing checks pass.
- [ ] Security limitations and supported OS versions disclosed.

## M0 Reconciliation — Mandatory Desktop Security Controls

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. FastAPI binds to 127.0.0.1 only. Loopback requests are authenticated; CORS is not authentication. Rust/Tauri owns the installation secret and narrow proxy; React never receives it. API keys/OAuth tokens use Windows Credential Manager or DPAPI-backed storage; SQLite stores opaque references only. OAuth uses system browser and public-client PKCE S256 where supported; never embed a confidential client secret. If native secure OAuth is unsupported, defer integration or approve a separately reviewed broker. AI transmission is disclosed; no silent fallback. Approval is exact revision/destination/media/payload bound and rechecked before publish. Unknown outcomes are reconciled, not blindly retried. Media uses generated paths and bounded validation; no generic public relay. Logs/backups/errors exclude secrets and sensitive payloads.
