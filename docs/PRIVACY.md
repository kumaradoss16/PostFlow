# PostFlow Privacy and Data Handling

**Document:** PRIVACY.md  
**Version:** 1.0  
**Status:** Proposed product privacy specification; not a public legal privacy notice  
**Product profile:** Local-first desktop MVP; future SaaS requires a separate notice and data-processing assessment  
**Related documents:** SECURITY.md, THREAT_MODEL.md, SYSTEM_DESIGN.md, DATABASE_SCHEMA.md

## 1. Purpose and status

This document defines PostFlow's intended data handling, user controls, external data disclosures, retention principles, and privacy requirements. It is an engineering and product specification. It is not legal advice, a binding privacy policy, or a claim of compliance with any law.

Before public distribution, the product owner must publish a user-facing privacy notice that accurately reflects implemented behavior, identify the responsible legal entity/contact, assess applicable jurisdictions (including India where relevant), and obtain legal review where appropriate. Do not claim a feature, deletion guarantee, or compliance status that the software cannot demonstrate.

## 2. Privacy principles

1. Local-first by default: user content and media remain on the device unless a user action or enabled integration transmits them.
2. Purpose limitation: send only data needed for the selected feature.
3. Transparency: disclose the destination, data category, and purpose before first use of an external provider or platform.
4. User control: allow users to disconnect accounts, remove credentials, export data, and delete local data.
5. Data minimization: do not collect telemetry or personal data that is not required.
6. No silent provider fallback: do not send content to another AI provider without explicit user choice.
7. No sale of personal data: the product must not sell personal data.
8. Security by design: protect credentials and sensitive local data according to SECURITY.md.
9. Accurate claims: distinguish local storage, third-party processing, and future SaaS processing.

## 3. Data categories

| Category | Examples | Default location | Sensitivity |
|---|---|---|---|
| Profile and workspace | Display name, workspace name, settings | Local SQLite | Personal/business context |
| Brand information | Voice, audience, brand guidelines | Local SQLite | Potentially confidential |
| Content | Drafts, captions, hashtags, campaign text | Local SQLite | User-generated content |
| Media | Images, video, thumbnails, metadata | Local filesystem | May contain personal data |
| Social account metadata | Platform, account ID/name, granted scopes | Local SQLite | Account-linked data |
| Social credentials | OAuth access/refresh tokens | OS secure store | Highly sensitive |
| AI credentials | Provider API keys | OS secure store | Highly sensitive |
| AI request/response | Prompt, selected source content, generated output | Transient by default; optional history if user enables/saves | May contain confidential data |
| Publishing records | Job state, timestamps, external post ID, permalink | Local SQLite | Account-linked activity |
| Analytics | Impressions, reach, likes, clicks, etc. | Local SQLite | Account-linked metrics |
| Audit events | Approval, credential change, publish action | Local SQLite | Security/accountability |
| Diagnostics | App version, error category, stack context | Local logs if enabled | May contain technical identifiers |
| Backups/exports | Database and media copies | User-selected local destination | Contains user content |

Do not collect government identifiers, precise location, contacts, or unrelated device data for the MVP.

## 4. Where data is stored

### 4.1 Local desktop storage

- Structured records: application-owned SQLite database.
- Media: application-owned local media directory.
- API keys and OAuth tokens: OS-backed credential store.
- Credential metadata: SQLite stores opaque references and non-secret status only.
- Logs: local application log directory with redaction and retention limits.
- Backups: user-selected destination, created only through an explicit backup action or clearly configured backup setting.

The product must document its actual data directory and provide an in-app action to open it. Do not imply that local data is encrypted at rest unless an encrypted database/filesystem feature has been implemented and verified. OS account permissions and credential-store encryption are not equivalent to encrypting every content/media file.

### 4.2 Data that leaves the device

| Feature/action | Recipient | Potential data transmitted | User control / disclosure |
|---|---|---|---|
| AI generation | User-selected AI provider | Prompt, selected source text, brand instructions, selected context; media only if explicitly supported and selected | Show provider and data categories before first use; explicit provider selection |
| AI research | Selected research/AI provider | Search query, topic, relevant context | Explain external search/provider processing |
| Social publishing | Selected social platform | Approved caption, media, hashtags, links, destination account metadata, required API metadata | User initiates or enables explicitly scoped automation; approval gate |
| Social analytics | Selected social platform | Authenticated metrics request and account identifiers | Connected account and requested analytics scope |
| OAuth connection | Platform authorization server | OAuth authorization request, app identifier, requested scopes, redirect/PKCE metadata | User chooses Connect and reviews scopes |
| Software update | Configured update service | Update request and technical version/platform metadata as implemented | Disclose update-check behavior in notice/settings |
| Optional diagnostics | Configured diagnostics endpoint, only if implemented and enabled | Minimized error/version data; no content or secrets | Opt-in, visible settings, preview/export where feasible |

The table is a design contract. The final privacy notice must be revised to match the actual providers, endpoints, payloads, and defaults in the shipped application.

### 4.3 AI data transmission

- The user must select the AI provider for a generation/research task.
- Before first use, disclose that the selected content will be sent to that provider.
- Show the provider name and the categories of data included.
- Provide a preview or summary of the context sent where feasible.
- Allow the user to remove unnecessary context before sending.
- Do not transmit local media unless the user explicitly selects a feature that requires it and the UI identifies the media.
- Do not silently retry with another provider after timeout, quota failure, or authentication failure.
- Provider-specific retention, training, and data processing terms are controlled by the provider and may differ by account tier and settings. Link to current provider terms in-product; do not make blanket claims that providers never retain or train on submitted data.
- Do not store full prompts/responses in diagnostics by default. If generation history is saved as product content, make that behavior visible and user-controllable.

### 4.4 Social platform transmission

Publishing sends the approved content and associated media to the selected platform. Platform operators process data under their own terms and privacy policies. OAuth grants account access within granted scopes. Disconnecting PostFlow does not necessarily delete posts already published on the platform; users must delete those posts through the platform or a supported API operation.

PostFlow must not claim that all platforms support every publishing or analytics operation. Availability depends on official APIs, account type, permission scopes, app review, and commercial terms.

## 5. Consent and user controls

### 5.1 Consent model

- Connecting an account requires an explicit user action and platform authorization.
- Granting an AI provider access requires adding the user's key or selecting a supported authenticated connection and confirming the provider.
- Sending content to an AI provider requires an intentional generation/research action and clear disclosure.
- Publishing requires approval of the exact variant revision by default.
- Auto-publishing is disabled by default. Enabling it requires a separate confirmation showing the rule scope, destination accounts, content eligibility, and how to pause it.
- Optional diagnostics/telemetry must be off by default unless a reviewed product decision and applicable law justify another model.
- Consent must not be bundled with unrelated settings or inferred from use of another feature.

### 5.2 User controls

Provide controls to:

- View connected social accounts, provider configuration, and granted scopes.
- Disconnect a social account and remove stored credential material.
- Replace, test, disable, and delete an AI provider key.
- Review which content/context will be sent to an AI provider.
- Pause scheduled publishing and disable automation.
- View publishing history and audit-relevant actions.
- Export workspace content, media, and settings in a documented format.
- Delete selected content, media, workspace data, or the local application profile.
- Clear local logs and diagnostics within the defined retention policy.
- Create and restore backups with explicit confirmation.

The UI must distinguish deleting local PostFlow data from deleting data already sent to external providers or platforms. Do not promise remote deletion unless the relevant provider/platform API supports it and the action has been completed and verified.

## 6. Retention and deletion

### 6.1 Proposed desktop defaults

| Data | Proposed retention |
|---|---|
| Drafts, variants, brands, campaigns | Until user deletes or exports and removes them |
| Media files | Until user deletes associated media or workspace data |
| OAuth and AI credentials | Until disconnected, replaced, revoked, or application data is reset |
| Publishing jobs and attempts | Retain operational history for 12 months by default; configurable if feasible |
| Analytics snapshots | Retain up to 24 months by default; configurable |
| Audit events | Retain 12 months by default; security events may require longer retention after legal/product review |
| Diagnostic logs | 30 days maximum by default, with size-based rotation; no content/secrets |
| Temporary files | Delete after task completion or within 24 hours; clean abandoned temporary data at startup |
| Backups | Retained until user deletes them or a clearly configured retention policy expires them |

These are proposed product defaults, not a statement of current behavior. Implement retention as a scheduled maintenance task and test it. Retention periods may be adjusted after user research and legal review.

### 6.2 Deletion semantics

- Deletion from the app removes the selected local record and related local files according to documented relationship/cascade rules.
- Before deleting a workspace or account, show the impact on drafts, media, scheduled jobs, credentials, and history.
- Cancel or pause affected future jobs before removing required account credentials.
- Remove secret-store entries and verify deletion where the OS API permits.
- Use database transactions for relational deletion and a recoverable filesystem deletion workflow for media.
- Explain that backups may contain prior copies until those backups expire or are manually deleted.
- Explain that data already transmitted to an AI provider or social platform is outside PostFlow's direct control.
- Do not claim secure erasure from SSDs, backups, OS snapshots, or provider systems unless a verifiable process supports that claim.

## 7. Analytics, telemetry, and diagnostics

### 7.1 Product analytics

The desktop MVP should not include third-party behavioral analytics by default. Local operational metrics required for dashboard functionality are stored locally and must not be conflated with telemetry.

If remote telemetry is later introduced:
- Make it opt-in and separately described.
- Collect only necessary app version, OS family/version, feature usage counts, and sanitized error codes.
- Never collect post text, prompts, media, OAuth tokens, API keys, account handles, or raw request/response bodies.
- Provide a preview of collected fields and a disable control.
- Define processor, purpose, retention, region, and deletion process before launch.

### 7.2 Diagnostics and support bundles

- Redact secrets and personal data before log serialization, not only at export time.
- Exclude database files, media, OAuth data, provider keys, and full content by default.
- Provide a preview before user exports a diagnostic bundle.
- Include only version, error codes, sanitized stack traces, and non-sensitive environment details needed for troubleshooting.
- Warn users before sharing logs with support.
- Define local log retention and size limits.

## 8. Backups, export, and portability

- Backups are local-first and user-initiated by default.
- A backup may include database records and media; it must never include plaintext credentials.
- Credential references may not be portable across devices. On restore to another device, require users to reconnect social accounts and re-enter AI keys.
- Show backup contents, destination, file size estimate, and whether media is included.
- Verify archive integrity and schema compatibility before restore.
- Create a pre-restore backup and require explicit confirmation before replacing current data.
- Export formats should be documented and reasonably portable (for example JSON/CSV for records and original media files).
- Do not upload backups to cloud storage without a distinct opt-in and a documented processor/data-transfer disclosure.

## 9. Children's privacy and sensitive content

PostFlow is not designed specifically for children. Do not knowingly target children or collect children's personal data as a product objective. If the product is made available to minors or used in a context involving children's data, obtain legal review and implement applicable age, consent, and safety requirements before processing.

Users may submit sensitive personal or business information in drafts and media. Warn users not to send unnecessary sensitive data to external AI providers or social platforms. Do not infer sensitive traits from content or use content for unrelated profiling.

## 10. Future SaaS privacy requirements

A SaaS deployment is a new processing context and must not inherit desktop privacy assumptions. Before launch, define:

- Controller/business and processor/service-provider roles.
- Tenant isolation and organization-level data access.
- Hosting regions, subprocessors, cross-border transfers, and data residency.
- Authentication, session, MFA, and account recovery.
- Data processing agreements and subprocessor disclosures where applicable.
- Retention schedules, deletion workflows, backup expiry, and legal holds.
- Subject access, correction, portability, objection, and deletion request processes as legally applicable.
- Incident response and breach notification process.
- Separate production analytics/telemetry consent and controls.
- Whether AI provider calls are made using PostFlow-managed credentials or user-supplied credentials, and who controls provider terms.
- A public privacy notice, terms, and contact for privacy requests.

Do not launch SaaS until a data protection impact/risk assessment appropriate to the actual processing has been completed.

## 11. Privacy acceptance checklist

- [ ] Actual local data directories and categories documented in-product.
- [ ] Credentials are stored in OS-backed secure storage, not database or files.
- [ ] First-use AI disclosure identifies the provider and data categories.
- [ ] No silent AI-provider fallback.
- [ ] Publishing and auto-publishing consent gates are enforced server-side.
- [ ] No remote telemetry by default; optional telemetry is separately opt-in.
- [ ] Logs and support bundles exclude content and credentials by default.
- [ ] User can disconnect accounts and remove provider credentials.
- [ ] Export and backup contents are documented and contain no plaintext secrets.
- [ ] Delete workflows cover DB rows, media, jobs, and credential references.
- [ ] UI distinguishes local deletion from third-party deletion.
- [ ] Retention tasks are implemented, observable, and tested.
- [ ] Public privacy notice accurately describes shipped behavior and has legal review.
- [ ] SaaS privacy assessment is complete before multi-tenant launch.

## 12. Privacy notice publication gate

Before public release, replace this engineering specification with a user-facing notice that states, in plain language:

1. Who operates PostFlow and how to contact them.
2. What data is processed and why.
3. Which data remains local and which leaves the device.
4. Which AI providers, social platforms, hosting, update, and diagnostic services receive data.
5. Legal bases or consent mechanisms where applicable.
6. Retention and deletion rules, including backups.
7. User rights and how to exercise them, where applicable.
8. International transfer and subprocessor information, where applicable.
9. Security limitations and incident contact.
10. Effective date and change history.

Do not publish this file as the final legal privacy policy without adapting it to the actual product behavior and obtaining appropriate review.
