# PostFlow — Acceptance Criteria

**Document:** `ACCEPTANCE_CRITERIA.md`  
**Product:** PostFlow  
**Document Type:** Product and Engineering Acceptance Specification  
**Version:** 1.0  
**Status:** Baseline Specification  
**Platform:** Windows Desktop (Initial Release)  
**Architecture:** Tauri 2 + React + TypeScript + Python FastAPI + SQLite  
**Related Documents:** `PRODUCT_VISION.md`, `PRD.md`, `USER_STORIES.md`

---

## 1. Purpose

This document defines the measurable acceptance criteria that PostFlow must satisfy before individual features, integrations, milestones, and product releases can be considered complete.

It establishes:

- Functional acceptance conditions.
- Non-functional requirements.
- Data integrity requirements.
- AI provider integration requirements.
- Social platform integration requirements.
- Publishing and scheduling reliability.
- Security and privacy requirements.
- User interface and accessibility expectations.
- Integration and end-to-end testing requirements.
- Release-blocking quality gates.

All criteria must be verifiable through manual testing, automated tests, API contract tests, or documented platform integration evidence.

A feature is not considered complete solely because its frontend implementation is finished.

## 2. Acceptance Principles

PostFlow must follow these principles:

1. **Verifiable:** Every acceptance criterion must have a clear pass/fail outcome.
2. **Traceable:** Requirements must map to product modules and user stories.
3. **Secure by default:** Credentials, account access, and publishing permissions must be protected.
4. **Data integrity first:** No silent data loss, duplicate publishing, or corrupted records.
5. **Failure isolation:** One provider or platform failure must not unnecessarily disrupt unrelated operations.
6. **User control:** Publishing and external data transmission must follow explicit user authorization.
7. **Recoverable:** Interrupted jobs must be recoverable without creating duplicate posts.
8. **Platform compliant:** Each integration must respect the relevant official API capabilities and restrictions.
9. **Observable:** Application operations and failures must be diagnosable without exposing secrets.
10. **Release evidence:** Critical features must have repeatable test evidence before release.

## 3. Acceptance Classification

| Priority | Classification | Meaning |
|---|---|---|
| P0 | Release Blocker | Must pass before the initial production release |
| P1 | High Priority | Required for a complete and reliable product experience |
| P2 | Medium Priority | Important enhancement; may be deferred with approval |
| FUTURE | Future Scope | SaaS, collaboration, or advanced capabilities |

### 3.1 Acceptance outcomes

- **PASS:** All applicable acceptance conditions are satisfied.
- **FAIL:** One or more mandatory conditions are not satisfied.
- **BLOCKED:** Testing cannot proceed because of an external dependency.
- **NOT APPLICABLE:** The criterion does not apply to the tested configuration.

A blocked criterion must include the reason, dependency owner, and next action. It must not be reported as passed.

## 4. Application Foundation and Workspace

**Related stories:** US-001 onward — Application Initialization and Workspace Management.

### AC-APP-001 — Application startup

Priority: P0

- The application must launch successfully on supported Windows 10 and Windows 11 configurations.
- The desktop shell must load the frontend without an unhandled startup exception.
- The local backend must become available before dependent application functionality is enabled.
- Backend startup failures must produce a meaningful error message.
- The application must not silently display a functional dashboard when its required backend is unavailable.

### AC-APP-002 — Local API security

Priority: P0

- The FastAPI service must bind only to `127.0.0.1` by default.
- The service must not expose an unauthenticated remote-access endpoint.
- A per-installation secret must protect local API requests.
- Unauthorized API requests must be rejected.
- Secrets must not appear in application logs, frontend state, or error responses.

### AC-APP-003 — Workspace creation

Priority: P0

- A user must be able to create a workspace.
- Workspace names must be validated.
- Workspace configuration must persist after application restart.
- Workspace records must not be unintentionally overwritten by another workspace.
- Invalid or duplicate workspace operations must return understandable errors.

### AC-APP-004 — Workspace switching

Priority: P1

- Switching workspaces must load the correct associated brands, accounts, content, media, and settings.
- Data belonging to one workspace must not appear in another workspace.
- Unsaved changes must be handled explicitly before switching.
- The active workspace must persist according to the application's documented behavior.

### AC-APP-005 — Application recovery

Priority: P0

- Closing and reopening the application must preserve committed records.
- Interrupted operations must be identified and recovered or marked for reconciliation.
- Application startup must not execute the same publishing job twice.
- Database initialization and migration failures must not silently destroy existing user data.

## 5. Brand Management

### AC-BRAND-001 — Brand creation

Priority: P1

- Users must be able to create, edit, view, and delete brands.
- Brand name and required fields must be validated.
- Brand descriptions, tone, audience, and visual identity settings must persist.
- A brand must belong to the correct workspace.
- Deleting a brand must not silently delete unrelated content or publishing history.

### AC-BRAND-002 — Brand context

Priority: P1

- AI content generation must support selecting a brand.
- The selected brand's configured voice, audience, and guidelines must be included in the generation context when enabled.
- Changing the selected brand must update the context used for subsequent generation.
- Brand context must not leak into unrelated workspace or brand requests.

## 6. AI Provider Management

**Supported initial providers:** OpenAI, Gemini, Claude, and Perplexity, subject to their current API capabilities and terms.

### AC-AI-001 — Provider configuration

Priority: P0

- Users must be able to configure supported AI providers.
- Each provider must have an independent configuration.
- Users must be able to select an available model from the provider's supported model configuration.
- Unsupported provider/model combinations must be rejected.
- Provider availability and configuration status must be visible.

### AC-AI-002 — Secure credential storage

Priority: P0

- API keys must be stored using OS-backed secure storage.
- Raw API keys must never be persisted in plaintext application settings or SQLite records.
- Raw API keys must not be exposed to frontend JavaScript.
- Logs and exceptions must redact credentials.
- Removing a provider credential must remove the corresponding stored secret.
- Credential retrieval must be restricted to the backend integration layer.

### AC-AI-003 — Provider connectivity testing

Priority: P1

- Users must be able to test provider connectivity.
- Successful tests must report a successful connection.
- Invalid credentials must produce a clear authentication error.
- Rate limits, network failures, and provider outages must be distinguished where possible.
- A connectivity test must not trigger an unintended content generation or publishing operation.

### AC-AI-004 — Provider capability registry

Priority: P0

- Each provider adapter must declare its supported capabilities.
- Text generation, structured output, image analysis, and research must not be assumed to be universally supported.
- Unsupported capabilities must be disabled or rejected with an explanatory message.
- Model availability must be configurable and maintainable without changing unrelated provider implementations.

### AC-AI-005 — Provider isolation

Priority: P0

- A provider failure must not corrupt other provider configurations.
- A failed request must preserve previously generated results.
- Errors must identify the relevant provider and operation.
- A failed provider request must not be silently repeated through another provider.

### AC-AI-006 — AI data transmission disclosure

Priority: P0

Before sending user content to a cloud provider:

- The application must identify the selected provider and model.
- The application must disclose the categories of data being transmitted.
- The user must have an opportunity to review the disclosure where required by the configured consent policy.
- The application must not silently transmit unrelated workspace data, credentials, or private files.
- Provider privacy and retention information must be presented accurately when available.
- Consent and transmission decisions must be recorded without storing unnecessary sensitive content.

### AC-AI-007 — Multi-provider generation

Priority: P1

- Users must be able to select multiple configured providers for comparison.
- Each provider request must be independently identifiable.
- A failure from one provider must not discard successful results from another.
- Each result must retain its provider and model metadata.
- Results must not be merged into one output without an explicit user action.

### AC-AI-008 — Provider fallback

Priority: P1

- Automatic fallback must only use providers explicitly authorized by the user.
- Fallback must not bypass data-transmission disclosure requirements.
- The user must be able to identify which provider generated the final output.
- A fallback failure must be reported independently.
- No fallback may silently transmit data to an unapproved provider.

## 7. AI Content Studio

### AC-CONTENT-001 — Content creation

Priority: P0

- Users must be able to create content manually.
- Content must support a title, source text, campaign association, and relevant metadata.
- New content must initially have a draft status.
- Content must persist after application restart.
- Invalid or empty required fields must be rejected.

### AC-CONTENT-002 — AI content generation

Priority: P0

- Users must be able to select a provider and supported model.
- Users must be able to specify the topic, objective, audience, tone, and content instructions.
- Generated output must be associated with the originating content item.
- Provider and model information must be retained.
- Failed generation must not overwrite existing content.
- The generated result must be editable before approval or publication.

### AC-CONTENT-003 — Content regeneration

Priority: P1

- Users must be able to regenerate content.
- Regeneration must create a distinguishable new revision or result.
- Existing approved or published revisions must remain historically accessible.
- Regeneration must not automatically publish content.
- Previous content must not be lost without explicit user action.

### AC-CONTENT-004 — Content revision

Priority: P0

- Users must be able to edit generated content.
- Changes must persist.
- Each material revision must be identifiable.
- Changes to a previously approved variant must invalidate its approval.
- Previously published content must retain its historical snapshot.

### AC-CONTENT-005 — Structured AI output validation

Priority: P0

- Structured provider responses must be validated against the expected schema.
- Invalid JSON or missing required fields must be rejected or handled through a controlled recovery process.
- Malformed AI output must not reach the publishing engine.
- Provider output must be treated as untrusted input.

### AC-CONTENT-006 — AI research and content intelligence

Priority: P2

- Research must only be available through providers or tools that explicitly support the required capability.
- Sources must be preserved when the provider returns source references.
- Unsupported claims must not be presented as verified facts.
- Research results must be distinguishable from user-authored content.
- The application must not fabricate citations or source URLs.

## 8. Media Library

### AC-MEDIA-001 — Media upload

Priority: P0

- Users must be able to upload supported image and video files.
- File type, extension, MIME type, and actual file content must be validated.
- File size must be checked against configured limits.
- Unsupported and potentially dangerous files must be rejected.
- Uploaded assets must be associated with the correct workspace.

### AC-MEDIA-002 — Media storage

Priority: P0

- Media must be stored in the configured application media directory.
- Database references must point to valid media records.
- Media filenames must be handled safely.
- File paths must not allow directory traversal.
- Media records and stored files must remain consistent.

### AC-MEDIA-003 — Media preview

Priority: P1

- Supported images must display previews.
- Supported video files must provide a preview or usable metadata view.
- Missing media must produce an understandable error.
- Preview generation must not modify the original file.

### AC-MEDIA-004 — Media transformations

Priority: P1

- Image resizing and supported transformations must produce valid output.
- The original asset must remain available unless explicitly replaced or deleted.
- Transformation failures must not corrupt the original.
- Generated assets must be distinguishable from source assets.

### AC-MEDIA-005 — Platform media validation

Priority: P0

- Media must be validated against the selected platform's current publishing requirements.
- Image dimensions, format, file size, aspect ratio, and video constraints must be checked where applicable.
- Unsupported media must be blocked before publication.
- Platform requirements must be maintained as configurable integration rules rather than assumed to be permanently fixed.

## 9. Multi-Platform Composer

### AC-COMPOSER-001 — Platform selection

Priority: P0

- Users must be able to select one or more connected social accounts.
- Only supported and authorized destinations must be selectable.
- Platform account identity must be visible.
- Selecting a platform must create or load its independent content variant.

### AC-COMPOSER-002 — Independent platform variants

Priority: P0

- Source content must remain separate from platform-specific variants.
- Each variant must be independently editable.
- Editing one variant must not unexpectedly overwrite other variants.
- Each variant must retain its destination platform and account association.
- Each variant must maintain its own revision history.

### AC-COMPOSER-003 — Platform-specific validation

Priority: P0

- Character limits must be checked against the applicable platform and content type.
- Required fields must be validated.
- Media constraints must be validated.
- Unsupported features must be clearly identified.
- Validation errors must identify the affected destination.

### AC-COMPOSER-004 — Preview

Priority: P1

- Users must be able to preview platform-specific content.
- The preview must reflect the selected variant and media.
- Switching platforms must load the corresponding preview.
- The preview must not be represented as an exact rendering of the live social platform unless that fidelity is demonstrated.

### AC-COMPOSER-005 — Cross-platform publishing preparation

Priority: P0

- Each destination must have an independent publishing job.
- A validation failure for one destination must not silently invalidate unrelated valid destinations.
- Users must be able to review destination-specific content before publishing.
- Publishing status must be tracked independently for each destination.

## 10. Social Account Management

### AC-ACCOUNT-001 — Account connection

Priority: P0

- Users must be able to initiate OAuth authorization for supported platforms.
- OAuth state must be validated.
- PKCE must be implemented where supported and required.
- The application must verify the authorization callback.
- An account must not be considered connected until the authorization exchange and account validation succeed.

### AC-ACCOUNT-002 — Account identification

Priority: P0

- The connected account's platform and display identity must be visible.
- The application must store only required account metadata.
- Account ownership and destination identity must be retained.
- Tokens must not be exposed to the frontend.

### AC-ACCOUNT-003 — Token management

Priority: P0

- Access tokens and refresh tokens must be protected using secure storage.
- Token expiration must be tracked where available.
- Refresh operations must use the official supported mechanism.
- Expired or revoked credentials must be reported.
- Failed token refresh must not cause an unauthorized publishing attempt.

### AC-ACCOUNT-004 — Account disconnection

Priority: P1

- Users must be able to disconnect an account.
- Disconnection must revoke or remove credentials where supported.
- The application must prevent new publishing attempts using disconnected credentials.
- Existing publishing history must remain accessible.
- Scheduled jobs targeting a disconnected account must be paused, cancelled, or flagged for user intervention according to the documented policy.

### AC-ACCOUNT-005 — Permission validation

Priority: P0

- Required permissions must be checked before enabling publishing features.
- Missing permissions must be clearly reported.
- The application must not claim an integration is fully functional when required platform approval is missing.
- Permission changes or revocations must be handled safely.

## 11. Content Approval Workflow

### AC-APPROVAL-001 — Draft and approval states

Priority: P0

- New content must begin in draft status.
- Users must be able to submit eligible variants for approval.
- Approval must be explicit.
- Manual approval must be the default publishing policy.
- Draft or rejected content must not be published.

### AC-APPROVAL-002 — Revision-bound approval

Priority: P0

- Approval must be associated with the exact variant revision.
- Any material edit after approval must invalidate the approval.
- The publishing engine must verify that approval still applies immediately before execution.
- Approval for one destination must not automatically approve another destination's independent variant.

### AC-APPROVAL-003 — Rejection

Priority: P1

- Users must be able to reject a variant.
- Rejected content must not be published.
- Rejection reasons should be retained where provided.
- Rejected content must remain editable.

### AC-APPROVAL-004 — Approval audit

Priority: P0

- Approval and rejection actions must be recorded.
- Records must include the relevant content revision and timestamp.
- The application must preserve sufficient audit history to investigate publishing decisions.

## 12. Publishing Engine

### AC-PUBLISH-001 — Pre-publishing validation

Priority: P0

Before publishing, the system must verify:

- Target account is connected.
- Credentials are valid.
- Required permissions are available.
- Content variant exists.
- Variant revision is current.
- Required approval is valid.
- Media is supported.
- Platform-specific validation passes.
- The publishing operation is not already completed.

If any required condition fails, publishing must be blocked with an actionable reason.

### AC-PUBLISH-002 — Manual publishing

Priority: P0

- Users must be able to initiate publishing manually.
- The application must display the selected destination.
- The application must display the content being published.
- The system must create a destination-specific publishing job.
- Publishing must not proceed without the required approval policy being satisfied.

### AC-PUBLISH-003 — Multi-platform publishing

Priority: P0

- Each selected destination must receive its own publishing job.
- Each job must have an independent state.
- A failed destination must not erase successful publishing results.
- The application must display partial success accurately.
- Overall campaign status must reflect individual destination results.

### AC-PUBLISH-004 — Idempotency

Priority: P0

- Each publishing operation must have a stable idempotency identity.
- Repeated requests for the same logical operation must not create duplicate jobs or posts.
- Job creation and execution must be protected against concurrent duplicate requests.
- Intentional reposts must remain possible through an explicitly new publishing operation.
- Idempotency behavior must be verified by automated tests.

### AC-PUBLISH-005 — Publishing attempt history

Priority: P0

- Every publishing attempt must be recorded.
- Attempt history must include destination, timestamp, outcome, and relevant provider/platform response metadata.
- Sensitive information must be redacted.
- Previous attempts must not be silently overwritten.
- Users must be able to inspect failure details.

### AC-PUBLISH-006 — Unknown publishing outcome

Priority: P0

- A network timeout or interrupted response must not automatically be interpreted as a failed publication.
- The system must mark uncertain outcomes for reconciliation.
- The system must check the platform for an existing published result where the API supports it.
- Blind retries must be prohibited while the outcome remains unknown.
- If reconciliation is impossible, the user must receive a clear manual intervention requirement.

### AC-PUBLISH-007 — Retry behavior

Priority: P0

- Retry must be available only for eligible failed or reconciled jobs.
- Retry must respect platform rate limits and retry policies.
- Retry must not create a duplicate post.
- The previous attempt must remain in history.
- Permanent failures must not be retried indefinitely.

### AC-PUBLISH-008 — Publishing result verification

Priority: P0

- Successful publication must require an authoritative platform response or documented verification mechanism.
- Published post identifiers must be stored when returned.
- Published timestamps must be stored.
- Permalinks must be stored when available.
- A locally completed request must not be represented as a confirmed publication without evidence.

### AC-PUBLISH-009 — Platform adapter compliance

Priority: P0

- Each platform adapter must implement only officially supported operations.
- Platform-specific authorization, content formatting, media upload, and publication flows must be handled independently.
- API restrictions must be documented.
- Integration tests must distinguish mocked responses from real platform verification.
- API access limitations must be reported as external dependencies rather than hidden implementation failures.

## 13. Scheduling System

### AC-SCHEDULE-001 — Schedule creation

Priority: P0

- Users must be able to schedule approved content variants.
- Scheduling must validate the destination account and publishing readiness.
- Scheduling time must be stored consistently in UTC.
- The interface must display the relevant local time zone.
- Invalid or past scheduling times must be rejected or handled according to documented rules.

### AC-SCHEDULE-002 — Persistent scheduling

Priority: P0

- Scheduled jobs must persist in SQLite.
- Scheduled jobs must survive application restart.
- The scheduler must not depend exclusively on an in-memory timer.
- Startup recovery must identify due jobs.
- Duplicate job execution must be prevented.

### AC-SCHEDULE-003 — Execution conditions

Priority: P0

- The desktop application or its supported background execution component must be active for scheduled publishing.
- The system must communicate this limitation to the user.
- A powered-off or sleeping machine must not be represented as capable of executing a local scheduled job.
- Missed schedules must be reconciled according to a documented policy.

### AC-SCHEDULE-004 — Schedule modification

Priority: P1

- Users must be able to edit or cancel eligible scheduled jobs.
- Changes must be persisted.
- Changes must not modify an already executing job without an explicit supported cancellation mechanism.
- A scheduled job must be revalidated before execution.

### AC-SCHEDULE-005 — Pause and resume

Priority: P1

- Users must be able to pause eligible scheduling operations.
- Paused jobs must not execute.
- Resuming must restore eligible jobs without creating duplicates.
- The user must be able to distinguish paused, scheduled, overdue, and failed jobs.

## 14. Publishing Calendar

### AC-CALENDAR-001 — Calendar display

Priority: P1

- The calendar must display scheduled publishing jobs.
- Calendar entries must identify the relevant platform and account.
- The displayed schedule must respect the configured time zone.
- Calendar status must reflect the actual publishing job state.

### AC-CALENDAR-002 — Calendar navigation

Priority: P1

- Users must be able to navigate between supported calendar periods.
- Calendar data must load from persistent records.
- Empty periods must display an appropriate empty state.
- Calendar filtering must not modify the underlying publishing records.

### AC-CALENDAR-003 — Calendar actions

Priority: P1

- Eligible scheduled items must support inspection, editing, cancellation, or navigation to the relevant content.
- Actions must respect publishing state and authorization rules.
- Invalid actions must be rejected with a clear explanation.

## 15. Dashboard and Activity

### AC-DASH-001 — Dashboard accuracy

Priority: P0

- Dashboard values must be derived from actual application records or clearly labeled demo data.
- Scheduled, published, failed, and draft counts must be consistent with underlying records.
- Dashboard summaries must not fabricate platform metrics.
- Empty states must be handled correctly.

### AC-DASH-002 — Activity history

Priority: P1

- Relevant content, account, AI, scheduling, and publishing operations must appear in activity history.
- Events must include timestamps and relevant references.
- Sensitive values must not be exposed.
- Activity history must not misrepresent a failed or uncertain operation as successful.

### AC-DASH-003 — Filtering

Priority: P1

- Users must be able to filter relevant dashboard or activity information.
- Filters must not modify source records.
- Combined filters must produce consistent results.
- Clearing filters must restore the default view.

## 16. Analytics and Reporting

### AC-ANALYTICS-001 — Data source integrity

Priority: P1

- Analytics must use actual platform metrics or locally recorded operational data.
- Unsupported metrics must be omitted or clearly marked unavailable.
- Demo data must be explicitly labeled.
- Missing metrics must not be displayed as real zero values.

### AC-ANALYTICS-002 — Platform analytics

Priority: P2

- Platform-specific analytics must use authorized API capabilities.
- Metric definitions must be documented.
- Data retrieval failures must be reported.
- Historical snapshots must retain their collection timestamps.
- Analytics must not fabricate engagement, impressions, or reach.

### AC-ANALYTICS-003 — Reporting

Priority: P2

- Users must be able to inspect available performance information.
- Reports must identify the platform and collection period.
- Exported reports must preserve metric labels and units.
- Incomplete reports must clearly indicate missing data.

## 17. Settings and Data Management

### AC-SETTINGS-001 — Application settings

Priority: P0

- Application settings must persist after restart.
- Invalid values must be rejected.
- Settings must have documented defaults.
- Changing settings must not unexpectedly alter existing content or publishing history.

### AC-SETTINGS-002 — Backup

Priority: P0

- Users must be able to create a backup of application data.
- Backup scope must be documented.
- Required database and media references must be preserved.
- Backup files must be stored in a user-accessible location.
- Backup completion or failure must be reported accurately.

### AC-SETTINGS-003 — Restore

Priority: P0

- Users must be able to restore a valid backup.
- Restore must validate backup integrity before modifying active data.
- The application must protect existing data against incomplete restore operations.
- A failed restore must not leave the database in an inconsistent state.
- Restore procedures must be tested on a clean application installation.

### AC-SETTINGS-004 — Data deletion

Priority: P1

- Users must be able to delete eligible content and media.
- Destructive operations must require appropriate confirmation.
- Referential integrity must be maintained.
- Deletion must not remove unrelated records.
- Audit and published-post history retention policies must be respected.

### AC-SETTINGS-005 — Data export

Priority: P2

- Users should be able to export supported content and metadata.
- Exported data must use documented formats.
- Export must not include raw credentials or access tokens.
- Export errors must not alter the original records.

## 18. Security and Privacy

### AC-SEC-001 — Authentication and local authorization

Priority: P0

- Protected local API routes must reject unauthorized requests.
- Authentication secrets must be generated and stored securely.
- Authorization checks must be enforced server-side.
- Frontend-only permission checks must not be treated as security controls.

### AC-SEC-002 — Secret protection

Priority: P0

- API keys, OAuth tokens, and other credentials must use OS-backed secure storage.
- Secrets must not be included in source control.
- Secrets must not be included in diagnostic bundles by default.
- Logs must redact credentials and authorization headers.
- Error reporting must not expose secret values.

### AC-SEC-003 — OAuth security

Priority: P0

- OAuth state must be unpredictable and validated.
- Redirect URI handling must follow the platform's registered configuration.
- PKCE must be used where supported and required.
- Authorization codes and tokens must not be written to logs.
- Callback requests must be protected against replay and state mismatch.

### AC-SEC-004 — File security

Priority: P0

- Uploaded files must be validated.
- Path traversal must be prevented.
- File access must be restricted to approved application directories.
- Unsafe or unsupported formats must be rejected.
- Media processing must not execute uploaded files as code.

### AC-SEC-005 — Prompt injection and AI output security

Priority: P0

- External content and AI-generated output must be treated as untrusted.
- AI instructions must not bypass application authorization.
- AI output must not independently trigger publishing, credential access, or destructive operations.
- Tool execution must require explicit policy authorization.
- Structured output must be validated before being used by downstream components.

### AC-SEC-006 — Audit logging

Priority: P0

- Security-relevant operations must be auditable.
- Audit records must include event type, timestamp, and relevant entity reference.
- Sensitive data must be excluded or redacted.
- Audit history must distinguish user actions from automated system operations.

### AC-SEC-007 — Dependency and vulnerability management

Priority: P0

- Dependencies must be pinned or constrained through reproducible dependency management.
- Known critical and high-severity vulnerabilities must be reviewed before release.
- Unmaintained or unnecessary dependencies must be avoided.
- Security findings must be documented and resolved or formally accepted before release.

## 19. User Interface and Experience

### AC-UI-001 — Visual consistency

Priority: P1

- The application must use a consistent design system.
- Layout, typography, spacing, buttons, dialogs, and form controls must be consistent.
- Dark theme must remain readable across all primary screens.
- Visual components must communicate actual application states.

### AC-UI-002 — Loading and error states

Priority: P0

- Long-running operations must show a loading or progress state.
- Failed operations must show actionable errors.
- Empty states must be informative.
- Users must not be left with an indefinite loading indicator when an operation has failed.

### AC-UI-003 — Publishing status visibility

Priority: P0

- Publishing states must be visually distinguishable.
- Users must be able to distinguish queued, publishing, published, failed, cancelled, and unknown outcomes.
- A success indicator must only be shown after publication is confirmed.
- Partial multi-platform success must be represented accurately.

### AC-UI-004 — Responsive desktop layout

Priority: P1

- Core screens must remain usable at supported desktop window sizes.
- Important actions must not become inaccessible when resizing.
- Forms and content editors must handle long text.
- Scroll behavior must be consistent.

### AC-UI-005 — Accessibility

Priority: P1

- Interactive controls must have meaningful labels.
- Keyboard navigation must support core workflows.
- Focus states must be visible.
- Color must not be the only means of communicating status.
- Text and controls must meet reasonable contrast expectations.

## 20. API and Backend

### AC-API-001 — API versioning

Priority: P0

- Application APIs must use the documented `/api/v1` prefix.
- Breaking changes must be versioned or handled through a documented migration.
- API contracts must be maintained in OpenAPI.

### AC-API-002 — Request validation

Priority: P0

- API requests must be validated using typed schemas.
- Invalid payloads must return consistent error responses.
- Unexpected fields must be handled according to the documented schema policy.
- Validation errors must not expose internal implementation details.

### AC-API-003 — Error handling

Priority: P0

- API errors must use a consistent response structure.
- Error responses must include a useful error code and correlation identifier where applicable.
- Sensitive details must not be returned to the frontend.
- Internal exceptions must be logged safely.

### AC-API-004 — Database integrity

Priority: P0

- Foreign-key constraints must be enabled and enforced.
- Database migrations must be versioned.
- Critical state transitions must be transactional.
- Database records must not become inconsistent during concurrent operations.
- Migration tests must cover upgrades from the previous supported schema version.

### AC-API-005 — Pagination and filtering

Priority: P1

- List endpoints must support documented pagination where required.
- Filtering and sorting must be validated.
- Pagination must return stable, predictable results.
- Large collections must not require unrestricted full-table retrieval.

### AC-API-006 — Correlation and idempotency

Priority: P0

- Relevant operations must support correlation IDs.
- Publishing operations must support idempotency.
- Correlation identifiers must be retained across related backend operations where practical.
- Duplicate requests must not produce duplicate side effects.

## 21. Performance and Reliability

### AC-PERF-001 — Resource consumption

Priority: P1

- The desktop application must remain usable on the documented baseline hardware configuration.
- The application must avoid unnecessary background polling.
- The initial desktop release must not require local LLM inference.
- Worker concurrency must be configurable and conservative by default.
- Media processing must not block the main user interface.

### AC-PERF-002 — Application responsiveness

Priority: P1

- Routine navigation must not wait for unrelated AI or publishing operations.
- Long-running requests must execute asynchronously.
- The interface must remain responsive during background tasks.
- Large media operations must provide progress feedback.

### AC-PERF-003 — Network resilience

Priority: P0

- Temporary network failures must be handled safely.
- Network timeouts must be configured.
- Retry policies must distinguish transient and permanent failures.
- Uncertain publishing outcomes must be reconciled before retry.

### AC-PERF-004 — Restart recovery

Priority: P0

- Scheduled jobs must survive application restart.
- In-progress jobs must be inspected on startup.
- Completed jobs must not be re-executed.
- Unknown outcomes must enter reconciliation.
- Recovery must not silently discard publishing history.

### AC-PERF-005 — Data consistency

Priority: P0

- Content revisions, approvals, jobs, and attempts must maintain consistent relationships.
- Concurrent updates must not overwrite newer revisions without detection.
- Publishing operations must use a stable content snapshot.
- Database transaction failures must not produce partially committed critical state changes.

## 22. Platform-Specific Integration Acceptance

Platform integrations must be accepted independently. A working mock adapter does not qualify as a verified production integration.

### AC-PLATFORM-001 — Instagram

Priority: P0 for any Instagram production release

- Supported Professional account types must be documented.
- Required Meta app permissions and review requirements must be satisfied.
- Media publishing must follow the current official API workflow.
- Required public media hosting or URL accessibility requirements must be met.
- Unsupported personal-account publishing must not be advertised as supported.
- Successful publishing must be verified through an authoritative API response or supported lookup.

### AC-PLATFORM-002 — Facebook

Priority: P0 for any Facebook production release

- Initial scope must focus on supported Facebook Page publishing.
- Required Page permissions must be documented and obtained.
- Personal profile publishing must not be claimed unless officially supported.
- Published Page content must be verified where the API supports it.

### AC-PLATFORM-003 — LinkedIn

Priority: P0 for any LinkedIn production release

- Member and organization publishing permissions must be handled separately.
- Required API products and permissions must be documented.
- The connected identity must be validated.
- Unsupported publishing operations must be blocked.
- Successful publishing must be verified.

### AC-PLATFORM-004 — Threads

Priority: P1

- Official authorization and publishing workflows must be implemented.
- Required account permissions must be validated.
- Content constraints must be enforced.
- Publishing outcomes must be stored accurately.

### AC-PLATFORM-005 — Pinterest

Priority: P1

- Board access and required permissions must be validated.
- Pin media and metadata must satisfy current API requirements.
- Board selection must be explicit.
- Published Pin identifiers and URLs must be stored when available.

### AC-PLATFORM-006 — X

Priority: P1

- Current API access, pricing, and applicable rate limits must be verified before implementation.
- Required authorization must be validated.
- Unsupported or unavailable API capabilities must not be advertised.
- Publishing must respect current API policies and usage limits.

### AC-PLATFORM-007 — Reddit

Priority: FUTURE / External Approval Gate

- Reddit API access and applicable developer terms must be reviewed.
- Commercial-use restrictions must be investigated before including Reddit in a commercial offering.
- Required approval or agreement must be obtained where applicable.
- Publishing must not be enabled based solely on a successful OAuth connection.
- The integration must remain disabled if legal or platform authorization requirements are unmet.

**Platform acceptance rule:** Platform API policies, permissions, pricing, and technical constraints must be revalidated at implementation and release time. This document does not guarantee platform approval or API access.

## 23. Future SaaS Acceptance

The following criteria are outside the initial local-first desktop release.

### AC-SAAS-001 — Multi-tenant isolation

Priority: FUTURE

- Every tenant-owned record must be scoped to the authorized tenant.
- Cross-tenant access must be rejected.
- Tenant isolation must be verified through security tests.
- Tenant identity must be enforced server-side.

### AC-SAAS-002 — Cloud deployment

Priority: FUTURE

- Production secrets must use managed secret storage.
- Database backups must be automated.
- Object storage must protect media assets.
- Background workers must support durable job processing.
- Deployment and rollback procedures must be documented.

### AC-SAAS-003 — Collaboration

Priority: FUTURE

- Workspace roles must be enforced.
- Approval permissions must be configurable.
- Audit history must identify the acting user.
- Concurrent editing must detect conflicting updates.

### AC-SAAS-004 — SaaS billing and subscription

Priority: FUTURE

- Subscription state must be authoritative.
- Billing events must be processed idempotently.
- Entitlements must be enforced server-side.
- Payment information must not be stored unnecessarily.

## 24. End-to-End Acceptance Scenarios

The following scenarios are release-critical. They must be implemented as automated tests where practical, supplemented by controlled real-platform tests.

### E2E-001 — Complete manual publishing workflow

Priority: P0

**Given:**
- A configured workspace.
- A configured brand.
- A valid AI provider.
- A connected and authorized social account.

**When:**
1. The user creates content.
2. The user generates or writes content.
3. The user creates a platform variant.
4. The user validates the variant.
5. The user approves the variant.
6. The user initiates publishing.

**Then:**
- The correct content revision must be published.
- The correct destination must receive the content.
- A publishing job and attempt record must exist.
- The published post identifier must be saved when returned.
- The UI must display a confirmed published state only after verification.

### E2E-002 — Multi-platform partial failure

Priority: P0

**Given:** Content is prepared for three destinations.

**When:** Two destinations succeed and one fails.

**Then:**
- Successful posts must remain published.
- The failed destination must show its failure state.
- Successful jobs must not be repeated.
- The user must be able to inspect and retry the eligible failed job.
- Overall status must indicate partial success.

### E2E-003 — Duplicate publishing protection

Priority: P0

**Given:** A publishing job has been submitted.

**When:** The same operation is submitted multiple times or concurrent requests arrive.

**Then:**
- Only one logical publishing operation must execute.
- Duplicate requests must return or reference the existing operation.
- No duplicate post must be created.

### E2E-004 — Unknown publishing outcome

Priority: P0

**Given:** A platform accepts a publishing request but the response is lost.

**When:** The application detects a timeout.

**Then:**
- The job must be marked as unknown or pending reconciliation.
- An automatic blind retry must not occur.
- The system must attempt supported reconciliation.
- The user must receive a clear status if reconciliation cannot be completed.

### E2E-005 — Application restart recovery

Priority: P0

**Given:** Approved publishing jobs are scheduled.

**When:** The application closes and restarts.

**Then:**
- Scheduled jobs must remain present.
- Due jobs must be reconciled and processed according to policy.
- Completed jobs must not execute again.
- In-progress or uncertain jobs must be handled safely.

### E2E-006 — AI provider failure isolation

Priority: P0

**Given:** Multiple providers are configured.

**When:** One provider fails and another succeeds.

**Then:**
- Successful output must remain accessible.
- The failed provider must show its error.
- No existing content must be overwritten by an empty failure result.
- Provider identity must remain attached to each output.

### E2E-007 — OAuth token expiration

Priority: P0

**Given:** A connected social account has an expired or revoked token.

**When:** The application attempts an operation.

**Then:**
- Supported token refresh must be attempted when appropriate.
- Failed refresh must block publishing.
- The user must be informed that reauthorization is required.
- Credentials must not be exposed in errors.

### E2E-008 — Approval invalidation

Priority: P0

**Given:** A variant has been approved.

**When:** The user edits its content.

**Then:**
- The old approval must no longer authorize publishing.
- The updated variant must require a new approval.
- The publishing engine must reject the stale approval.

### E2E-009 — Backup and restore

Priority: P0

**Given:** The application contains brands, content, variants, media, accounts, and publishing history.

**When:** A backup is created and restored into a test installation.

**Then:**
- Supported records must be restored.
- Media references must resolve.
- Publishing history must remain consistent.
- Credentials must be restored only through the documented secure-storage mechanism, or explicitly require reconnection if secure credentials are not included.
- Restore integrity must be verified.

### E2E-010 — Data transmission disclosure

Priority: P0

**Given:** A user selects a cloud AI provider.

**When:** The user initiates generation using workspace content.

**Then:**
- The selected provider and model must be identified.
- Relevant data categories must be disclosed.
- The user must be able to make the required consent decision.
- No unrelated workspace data or secrets must be transmitted.

## 25. Test Strategy

### 25.1 Unit testing

Required coverage areas:

- Business logic.
- Content validation.
- Variant revision management.
- Approval state transitions.
- Publishing state transitions.
- Idempotency calculations.
- Scheduler decisions.
- Provider capability checks.
- Credential redaction.
- API request validation.

### 25.2 Integration testing

Required coverage areas:

- FastAPI and SQLite.
- SQLAlchemy models and transactions.
- Database migrations.
- OS-backed credential storage.
- AI provider adapters.
- Social platform adapters.
- Media storage and processing.
- Scheduler and worker execution.
- Backup and restore.

### 25.3 Contract testing

- API requests and responses must match documented schemas.
- Provider adapters must satisfy their declared interfaces.
- Social adapters must satisfy common publishing interface contracts.
- Unsupported platform capabilities must fail explicitly.
- Database schema changes must pass migration tests.

### 25.4 Security testing

Required tests:

- Unauthorized local API requests.
- Invalid authentication secret.
- OAuth state mismatch.
- Token exposure in logs.
- Path traversal attempts.
- Malformed media uploads.
- Invalid structured AI output.
- Prompt injection attempts.
- Unauthorized publishing attempts.
- Stale approval attempts.
- Cross-workspace access attempts.

### 25.5 End-to-end testing

- Complete manual publishing.
- Multi-platform partial failure.
- Duplicate publishing protection.
- Unknown outcome reconciliation.
- Scheduled publishing.
- Restart recovery.
- Provider failure.
- Token expiration.
- Approval invalidation.
- Backup and restore.

### 25.6 Real API testing

Mock tests are insufficient for production integration acceptance.

For each production-enabled platform:

- Use an authorized test account.
- Verify the OAuth flow.
- Verify required permissions.
- Verify the real publishing workflow.
- Verify success and error responses.
- Verify rate-limit behavior where practical.
- Verify stored platform identifiers.
- Record API version and test date.

Tests must not publish to public accounts without explicit authorization.

## 26. Quality Gates

A release candidate must pass all mandatory gates below.

| Gate | Requirement | Release rule |
|---|---|---|
| QG-001 | Unit tests | All required tests pass |
| QG-002 | Integration tests | All required tests pass |
| QG-003 | API contracts | No unresolved breaking contract failures |
| QG-004 | Database migrations | Upgrade and rollback/recovery procedures verified |
| QG-005 | Security | No unresolved critical or high-severity findings |
| QG-006 | Credential protection | No secrets exposed in logs, frontend, or plaintext configuration |
| QG-007 | Publishing integrity | Idempotency and unknown-outcome tests pass |
| QG-008 | Recovery | Restart recovery and backup restoration pass |
| QG-009 | Platform integrations | Every enabled platform passes its required real API tests |
| QG-010 | UX | Critical workflows have no release-blocking usability defects |
| QG-011 | Documentation | Setup, configuration, limitations, and recovery procedures documented |
| QG-012 | Packaging | Clean installation and upgrade tests pass |

### 26.1 Mandatory release blockers

The release must be rejected if any of the following is true:

- Publishing can occur without the required approval.
- Duplicate publishing can occur through ordinary retries.
- Unknown publishing outcomes are blindly retried.
- OAuth tokens or AI credentials are exposed.
- Unauthorized local API access is possible.
- Workspace data can be accessed across unauthorized boundaries.
- Database corruption or silent data loss is reproducible.
- Scheduled jobs cannot recover safely after restart.
- The application reports unverified publication as confirmed success.
- An enabled platform integration violates its required authorization or API workflow.

## 27. Performance Baseline

The following are initial engineering targets, not claims of measured performance. They must be benchmarked on the documented minimum hardware.

| Metric | Initial target |
|---|---|
| Cold application startup | Under 10 seconds |
| Routine local API response | Under 500 ms at the 95th percentile for lightweight operations |
| Dashboard initial rendering | Under 3 seconds after backend readiness |
| Local database operations | No unnecessary full-table scans for routine views |
| Background workers | 1–2 by default |
| UI responsiveness | No blocking during AI, media, or publishing operations |
| Memory usage | Measure and optimize for the 8 GB baseline |
| AI request duration | Provider-dependent; display progress and timeout handling |

Performance measurements must record the machine specification, dataset size, application build, and test procedure. Targets must not be marked passed without benchmark evidence.

## 28. Requirement Traceability

Each implemented feature must be traceable through:

1. Product requirement.
2. User story.
3. Acceptance criteria.
4. Implementation module.
5. Automated or manual test.
6. Test evidence.
7. Release decision.

Suggested traceability structure:

| Requirement ID | User Story ID | Module | Test ID | Priority | Status |
|---|---|---|---|---|---|
| AC-APP-001 | Relevant US ID | Application | TEST-APP-001 | P0 | Pending |
| AC-AI-002 | Relevant US ID | AI Providers | TEST-AI-002 | P0 | Pending |
| AC-COMPOSER-002 | Relevant US ID | Composer | TEST-COMP-002 | P0 | Pending |
| AC-APPROVAL-002 | Relevant US ID | Approval | TEST-APR-002 | P0 | Pending |
| AC-PUBLISH-004 | Relevant US ID | Publishing | TEST-PUB-004 | P0 | Pending |
| AC-SCHEDULE-002 | Relevant US ID | Scheduler | TEST-SCH-002 | P0 | Pending |
| AC-SEC-002 | Relevant US ID | Security | TEST-SEC-002 | P0 | Pending |

The exact user-story mapping must be populated from `USER_STORIES.md`. Do not infer story IDs from module order.

## 29. Definition of Done

A feature is considered complete only when all applicable conditions are met:

- [ ] Functional implementation is complete.
- [ ] Acceptance criteria are satisfied.
- [ ] Input validation is implemented.
- [ ] Error handling is implemented.
- [ ] Authorization and security controls are implemented.
- [ ] Database persistence is verified.
- [ ] Loading, success, empty, and failure states are implemented.
- [ ] Unit tests are written and passing.
- [ ] Integration tests are written and passing where applicable.
- [ ] API contracts and documentation are updated.
- [ ] Relevant user-story traceability is maintained.
- [ ] No unresolved critical defects remain.
- [ ] Manual verification is completed for critical workflows.
- [ ] Test evidence is available for review.

A frontend-only implementation, mock-only integration, or hardcoded demonstration is not sufficient for acceptance of a production feature.

## 30. MVP Acceptance Scope

The initial PostFlow MVP must prioritize the following capabilities:

| Module | MVP requirement | Priority |
|---|---|---|
| Application foundation | Startup, workspace, local API | P0 |
| Brand management | Basic brand configuration | P1 |
| AI providers | Secure configuration and generation | P0 |
| AI Content Studio | Create, generate, edit, regenerate | P0 |
| Media library | Upload, storage, validation, preview | P0 |
| Multi-platform composer | Independent variants and validation | P0 |
| Social accounts | OAuth and secure token handling | P0 |
| Approval workflow | Revision-bound manual approval | P0 |
| Publishing engine | Destination jobs, idempotency, history | P0 |
| Scheduler | Persistent local scheduling and recovery | P0 |
| Publishing calendar | Basic schedule visibility | P1 |
| Dashboard | Accurate operational status | P1 |
| Analytics | Limited verified metrics | P2 |
| SaaS collaboration | Multi-user and tenant support | FUTURE |

### 30.1 MVP completion conditions

The MVP is accepted only when:

1. Users can create and manage a workspace.
2. Users can configure at least one supported cloud AI provider securely.
3. Users can create and edit content.
4. Users can generate content through the configured provider.
5. Users can create independent platform variants.
6. Users can connect at least one production-authorized social platform.
7. Users can validate and approve content.
8. Users can publish through an authorized platform API.
9. Publishing operations are idempotent and independently tracked.
10. Scheduled jobs persist and recover safely.
11. Users can inspect publishing results and failures.
12. Backup and restore are verified.
13. Mandatory security and release quality gates pass.

A platform must not be counted as production-supported until its actual authorization and publishing workflows have passed real API testing.

## 31. External Dependencies and Risks

The following items are not entirely controlled by PostFlow's implementation:

- Social platform developer account approval.
- OAuth application review.
- Platform API permissions.
- API pricing and usage quotas.
- Platform rate limits.
- Platform policy changes.
- AI provider availability and pricing.
- AI provider model retirement.
- External network availability.
- Reddit commercial-use authorization, where applicable.

Each dependency must have an owner, status, and mitigation plan.

A blocked external dependency must not be hidden by a mock integration or a false production-ready label.

## 32. Acceptance Sign-off

Before production release, the following roles must review the applicable evidence:

| Role | Responsibility | Approval |
|---|---|---|
| Product Owner | Product scope and business requirements | Pending |
| Technical Lead | Architecture and implementation quality | Pending |
| QA Engineer | Functional and regression testing | Pending |
| Security Reviewer | Security and privacy controls | Pending |
| Integration Owner | Real platform API verification | Pending |
| Release Owner | Packaging and release readiness | Pending |

### Final acceptance decision

- [ ] Accepted for production release.
- [ ] Accepted with documented non-blocking limitations.
- [ ] Rejected — mandatory criteria not satisfied.
- [ ] Blocked — external dependencies remain unresolved.

**Release version:**  
**Build identifier:**  
**Test execution date:**  
**Outstanding defects:**  
**Accepted limitations:**  
**Approver:**  
**Approval date:**  

---

## 33. Final Acceptance Statement

PostFlow may be considered production-ready only when its core content creation, AI integration, account authorization, approval, publishing, scheduling, persistence, recovery, and security requirements have been verified.

The application must never prioritize publishing convenience over data integrity, account security, user authorization, or platform compliance.

**The acceptance standard is operational correctness, not feature count.**

## M0 Reconciliation — Controlling Acceptance Overrides

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. This addendum supersedes conflicting MVP scope and priorities in this document. The target is a single-user, local-first Windows desktop MVP. Windows 11 is the production support baseline; Windows 10 is best-effort development only. P0 includes Tauri 2/Rust, React/TypeScript, supervised FastAPI, SQLite/SQLAlchemy/Alembic, local media, source content and independent revisioned variants, one AI provider, exact human approval, durable per-destination publishing jobs, idempotency/immutable attempts/unknown-outcome reconciliation, one-time local scheduling, privacy, backup and restore. At most one official social-platform integration may be enabled, and only after a documented PASS feasibility gate. Scheduling requires the app/worker active, device awake and internet available. Campaigns, team membership/roles, collaboration, billing, SaaS, cloud scheduling, public API, cloud media relay, additional AI providers/platforms, multi-provider comparison/fallback and advanced social analytics are P1/Future, not MVP requirements.

Additional P0 criteria: (1) FastAPI binds to 127.0.0.1 only; protected requests are authenticated through a Rust-owned proxy; React never receives the installation secret; CORS is not authentication. (2) AI transmission identifies provider, purpose and data categories; credentials are OS-backed; no silent fallback; structured output is validated. (3) Approval binds exact variant revision, destination, media and material payload; any material change invalidates it and backend rechecks before submission. (4) Unknown publish outcomes require reconciliation, never blind retry; attempts are immutable. (5) One-time schedules persist in UTC with IANA timezone; UI discloses local worker/device/network requirements. (6) External publishing is conditional on platform PASS, including OAuth, scopes, review, media upload and controlled publish evidence.
