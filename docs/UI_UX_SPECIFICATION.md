# PostFlow — UI/UX Specification

| Field | Value |
|---|---|
| Product | PostFlow |
| Document | `UI_UX_SPECIFICATION.md` |
| Version | 1.0 |
| Status | Proposed design baseline |
| Target release | Local-first desktop MVP |
| Primary platform | Windows desktop (Tauri 2) |
| Frontend | React + TypeScript |
| Reference documents | `PRODUCT_VISION.md`, `PRD.md`, `SYSTEM_DESIGN.md`, `ARCHITECTURE_DIAGRAMS.md` |

## 1. Purpose and design outcomes

This specification defines the product navigation model, screen information architecture, interaction contracts, visual system, responsive behavior, accessibility expectations and primary user journeys for PostFlow.

The UX must make the full content lifecycle understandable without hiding operational risk:

1. Create a source content item.
2. Generate or write platform-specific variants.
3. Attach and validate media.
4. Review and approve the exact variant revision.
5. Select a connected destination account.
6. Schedule or publish.
7. Monitor the job and reconcile uncertain outcomes.
8. Review platform-reported performance where available.

### Product design principles

- **Workflow-first:** navigation follows the user's work, not backend modules.
- **One source, many destinations:** a content item is the source; platform variants are independently editable.
- **Visible operational truth:** distinguish draft, approved, scheduled, publishing, published, failed and unknown outcomes.
- **Human control:** AI generation never silently approves or publishes.
- **Capability-aware UI:** only expose actions supported by the selected platform/account capability.
- **Local-first clarity:** communicate that scheduled work requires the desktop app and worker to be running, and the machine to be awake and online.
- **Progressive disclosure:** keep frequent actions visible; move advanced settings into contextual panels.
- **Recoverability:** destructive actions require confirmation; failed and uncertain jobs provide safe next steps.

## 2. Product assumptions and scope boundaries

### 2.1 Initial desktop MVP

Primary navigation and screens:

- Overview
- Calendar
- Content
- Composer
- Media Library
- Social Accounts
- AI Providers
- Analytics (only where real metrics are available)
- Settings

Workspace and brand context are persistent global selectors. Campaigns, team collaboration, agency/client switching, subscription billing and SaaS administration are future capabilities; do not make them appear implemented in the MVP.

### 2.2 Explicit non-goals

The UI must not imply support for automated engagement, scraping, unauthorized browser automation, unrestricted autonomous publishing, or guaranteed support for every feature on every social platform.

Platform availability, permissions, content limits and media rules are determined by the backend capability registry. Never hardcode a universal capability assumption into the UI.

### 2.3 Desktop scheduling disclosure

A persistent, dismissible status notice in the scheduler/calendar area must explain:

> PostFlow runs scheduled publishing from this desktop. The app and background worker must remain active, and the computer must be awake and connected to the internet at the scheduled time.

Do not claim cloud-like 24/7 execution for the local desktop profile.

## 3. Information architecture and navigation

### 3.1 Global application shell

**Desktop layout**

- Left navigation rail: 224–248 px expanded; 68–76 px collapsed.
- Top application bar: 60–68 px.
- Main content: flexible, max-width 1600 px for dense workspaces.
- Optional right inspector: 320–380 px, shown only on screens where contextual editing is useful.
- Persistent bottom-left runtime indicator: API/worker state and app version.
- Global toast region and modal layer.

### 3.2 Primary navigation

| Group | Route | Screen | Purpose |
|---|---|---|---|
| Workspace | `/overview` | Overview | Operational summary and next actions |
| Planning | `/calendar` | Calendar | Schedule and publication timeline |
| Creation | `/content` | Content Library | Search, filter and manage source content |
| Creation | `/composer/new` | Composer | Create source content and platform variants |
| Assets | `/media` | Media Library | Upload, search and manage media |
| Publishing | `/accounts` | Social Accounts | Connect and inspect destination accounts |
| Intelligence | `/ai-providers` | AI Providers | Configure and test AI providers |
| Intelligence | `/analytics` | Analytics | Inspect verified platform metrics |
| System | `/settings` | Settings | Preferences, privacy, backup and diagnostics |

The Publishing Queue is a contextual view reachable from Overview, Calendar and job detail. It may have a dedicated route `/publishing` if the implementation requires it, but must not duplicate the underlying job records.

### 3.3 Navigation behavior

- Active route is visually distinct and programmatically exposed.
- Collapse/expand state persists locally.
- On narrow windows, the navigation becomes a drawer opened by a menu control.
- Workspace and brand selectors remain available in the app bar.
- Route changes preserve unsaved composer state; warn before leaving only when autosave cannot guarantee recovery.
- Deep links to content, variants and jobs resolve to a detail view with a back path.
- Every screen has a clear title, concise description and one primary action.

## 4. Screen specifications

### 4.1 Overview

**User goal:** understand what needs attention and move directly into the next task.

**Layout**
- Header: “Overview”, active workspace/brand context and “Create post” primary CTA.
- KPI strip: scheduled, awaiting approval, published this period, failed/needs attention. Only show metrics supported by local records.
- Main column: upcoming schedule and recent activity.
- Secondary column: connected account health, AI provider health and quick actions.
- Local runtime banner when worker is stopped, app is in offline mode or scheduling is at risk.

**Interactions**
- KPI click applies a filter to the relevant list.
- Upcoming item opens the job/variant detail.
- “Create post” opens Composer.
- Failed/unknown outcome card opens a diagnostic detail; never offer a blind retry for an unknown outcome.
- Empty state explains how to connect an account or create the first post.

**States:** loading skeleton, populated, first-run empty, partial integration outage, worker stopped, offline, error with retry.

### 4.2 Calendar

**User goal:** plan, inspect and reschedule content.

**Layout**
- Header with date range, previous/next, Today and Create.
- View switcher: Month / Week / List. Default Week for desktop, List for narrow windows.
- Filter row: workspace/brand, platform, account and status.
- Calendar grid with compact cards showing time, platform icon, content title and status.
- Side inspector on selection: destination, schedule time, approval status and actions.

**Interactions**
- Selecting a card opens inspector; double-click or explicit Edit opens Composer.
- Drag-and-drop rescheduling is allowed only after backend capability and confirmation; keyboard-accessible reschedule action is mandatory.
- A moved job is not considered rescheduled until the API confirms it.
- Conflicts and invalid schedule times show inline errors.
- Calendar labels distinguish local timezone from UTC storage.
- Filters are reflected in the URL/query state where practical.

**States:** empty range, loading, dense schedule, failed job, unknown outcome, worker unavailable, offline.

### 4.3 Content Library

**User goal:** find, organize and reuse source content.

**Layout**
- Header and “New content” CTA.
- Search field, status filter, content type, brand and date filters.
- Table/list rows: title, brand, variant count, updated time, source status and overflow actions.
- Optional grid view for media-led content.
- Detail panel with source text, variants and activity history.

**Interactions**
- Search is debounced and supports clear.
- Row opens content detail.
- Duplicate creates a new source item; it does not mutate the original.
- Delete requires confirmation and explains dependent variants/jobs.
- Bulk operations must not bypass approval or publish safeguards.

**States:** empty library, no search results, loading, filtered results, API error.

### 4.4 Composer

**User goal:** create a source post and adapt it to selected social destinations.

**Layout**
- Header: Back, title/status, autosave indicator and primary Save/Review action.
- Main editor column (roughly 60–65%): source title, source text, brand voice/context, media attachments and AI assistance.
- Destination column (roughly 35–40%): platform/account selection and variant tabs/cards.
- Preview panel: platform-specific preview where reliable; otherwise label as an approximation.
- Variant editor includes body, hashtags, link/CTA, media, character/format guidance and revision indicator.

**Composer workflow**
1. Select workspace and brand.
2. Enter source content or invoke AI generation.
3. Select destination platforms/accounts.
4. Generate or edit one variant per destination.
5. Validate text, media and account capabilities.
6. Save draft or send for approval.
7. Schedule/publish only after approval policy is satisfied.

**Critical interaction rules**
- Source edits do not silently overwrite platform variants.
- Variant edits increment the variant revision.
- Any edit after approval invalidates approval for that revision.
- Approval action must submit the expected revision; stale approvals return a conflict.
- AI output is always editable and clearly identified as generated.
- AI provider selection and data-transmission disclosure appear before the first external request and when the destination/provider changes.
- Fallback to another AI provider requires explicit user consent.
- Generation is asynchronous where needed; show task progress and allow cancellation if supported.
- The UI must not show a successful publish state based only on a queued response.

**Validation**
- Inline field errors plus a summary.
- Character/media constraints sourced from backend capabilities.
- Unsupported feature is explained, not silently removed.
- “Preview” is never represented as an exact platform rendering unless the adapter can guarantee it.

**States:** pristine, dirty, autosaving, saved, save failed, generating, generation failed, validation failed, ready for approval, approved revision, stale approval, scheduling conflict, offline.

### 4.5 Media Library

**User goal:** upload, find and reuse approved assets.

**Layout**
- Upload drop zone and file picker.
- Search, media type and processing-status filters.
- Grid cards with thumbnail, filename, dimensions/duration, size and processing state.
- Detail inspector with metadata, usage references and safe actions.

**Interactions**
- Upload progress is visible and cancellable if supported.
- Processing status is distinct from upload status.
- Preview uses safe local asset handling.
- Delete is blocked or warns when an asset is referenced by scheduled/published content.
- Unsupported MIME type, file size, corrupt file and processing failure have actionable messages.

### 4.6 Social Accounts

**User goal:** connect and maintain publishing destinations.

**Layout**
- Connected account cards grouped by platform.
- Account identity, account type, permission summary, last verification and health state.
- “Connect account” opens a provider/platform-specific flow.
- Account detail shows granted scopes/capabilities, reauthorization and disconnect controls.

**Interactions and safety**
- OAuth starts in the system browser or approved secure flow; callback state is one-time and validated.
- Never render access/refresh tokens or secret values.
- Distinguish connected, permission-limited, expired, disconnected and error.
- Disconnect requires confirmation and explains effect on queued jobs.
- A connected account is not necessarily eligible for every publishing format.

### 4.7 AI Providers

**User goal:** configure and validate AI services.

**Layout**
- Provider cards for supported integrations.
- Connection status, configured model, last test and availability.
- Credential entry is write-only; show provider and masked status only.
- Model selection and capability controls are contextual.

**Interactions**
- Test connection does not imply the provider is enabled for all workflows.
- Changing provider/model can change data transmission; disclose provider, data categories and purpose.
- Never log or display credentials.
- Provider failure is isolated from other providers.
- Multi-provider comparison is an explicit user action with per-provider result/error panels.

### 4.8 Publishing Queue and Job Detail

**User goal:** inspect execution state and recover safely.

**Queue layout**
- Tabs/filters: Scheduled, Queued, Running, Failed, Needs reconciliation, Published, Cancelled.
- Rows show content, platform/account, scheduled time, status and last update.
- Job detail includes immutable attempt timeline, request correlation ID and redacted diagnostics.

**Job states**
- `scheduled`
- `queued`
- `claimed`
- `publishing`
- `retry_pending`
- `reconciling`
- `published`
- `failed`
- `cancelled`

**Rules**
- Unknown external outcome transitions to `reconciling`; no automatic blind retry.
- Retry is enabled only for definitively retryable failures.
- Cancel is available only where execution state and platform semantics permit it.
- Attempts are displayed chronologically and are immutable.
- Distinguish “accepted by PostFlow” from “confirmed published by platform”.

### 4.9 Analytics

**User goal:** review performance without misleading numbers.

**Layout**
- Date range and platform/account filters.
- Summary cards only for available metrics.
- Trend chart and post-level table.
- Metric provenance and last sync timestamp.

**Rules**
- Missing metric is “Not available”, not zero.
- No fabricated demo values in production.
- Explain platform API limitations and metric definitions.
- Empty state prompts the user to connect an eligible account or wait for metrics sync.

### 4.10 Settings

Sections:
- General: theme, language, timezone, startup behavior.
- Privacy: AI data disclosure and local data controls.
- AI: provider defaults and fallback consent.
- Publishing: worker behavior, notification preferences and retry policy visibility.
- Storage: data directory, backup and restore.
- Diagnostics: API/worker health, logs export with secrets redacted, app version.

Restore is a high-impact operation: require explicit confirmation, explain overwrite behavior and recommend a backup first.

## 5. Design system

### 5.1 Visual direction

A calm, high-contrast productivity interface. Use a dark navy navigation rail with a light neutral work canvas. Avoid decorative gradients, oversized marketing typography, excessive glass effects and generic AI-themed illustrations. The application is an operational tool; hierarchy and data clarity take priority.

### 5.2 Color tokens

| Token | Value | Usage |
|---|---|---|
| `--color-app-bg` | `#F4F6FA` | Main application background |
| `--color-surface` | `#FFFFFF` | Cards, panels, dialogs |
| `--color-surface-muted` | `#F8FAFC` | Subtle grouped areas |
| `--color-sidebar` | `#111827` | Navigation rail |
| `--color-sidebar-hover` | `#1F2937` | Navigation hover |
| `--color-text` | `#172033` | Primary text |
| `--color-text-muted` | `#667085` | Secondary text |
| `--color-border` | `#E4E7EC` | Dividers and borders |
| `--color-primary` | `#4F46E5` | Primary actions and focus |
| `--color-primary-hover` | `#4338CA` | Hover/active primary |
| `--color-success` | `#16845B` | Confirmed success |
| `--color-warning` | `#B7791F` | Attention required |
| `--color-danger` | `#C2413A` | Errors/destructive actions |
| `--color-info` | `#2563A6` | Informational states |

Status must use text labels and icons in addition to color.

### 5.3 Typography

- Primary typeface: system UI stack (Segoe UI on Windows).
- Page title: 24–28 px, semibold.
- Section title: 16–18 px, semibold.
- Body: 14 px, regular.
- Supporting metadata: 12–13 px.
- Dense tabular data: 13–14 px with tabular numerals.
- Line height: 1.4–1.55 for body content.

### 5.4 Spacing, radius and elevation

Use a 4 px base spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48.

- Control height: 36–40 px.
- Input radius: 8 px.
- Card radius: 12 px.
- Dialog radius: 14 px.
- Card border: 1 px neutral border.
- Shadows: subtle and reserved for floating overlays.
- Avoid nested cards where spacing and dividers communicate hierarchy more clearly.

### 5.5 Components

Required shared components:
- AppShell, Sidebar, TopBar, WorkspaceSelector
- PageHeader, Breadcrumbs, Tabs, FilterBar
- Button, IconButton, TextField, TextArea, Select, DateTimePicker
- StatusBadge, PlatformBadge, AccountAvatar
- DataTable, EmptyState, ErrorState, Skeleton
- Toast, Tooltip, DropdownMenu, ConfirmDialog, Drawer, Modal
- ContentCard, VariantEditor, PlatformPreview
- UploadDropzone, MediaCard, UploadProgress
- JobTimeline, RuntimeHealthIndicator

Use consistent component contracts and avoid one-off styling per screen.

### 5.6 Iconography

Use a consistent outline icon family. Platform logos should be official or clearly recognizable brand marks where licensing permits. Do not use emoji as the only platform identifier.

## 6. Responsive and adaptive behavior

Although the initial target is Windows desktop, the React UI must adapt to resizable windows and smaller screens.

| Viewport | Layout behavior |
|---|---|
| ≥ 1440 px | Expanded sidebar, multi-column dashboards, composer editor + inspector |
| 1200–1439 px | Expanded/collapsible sidebar, reduced secondary column |
| 900–1199 px | Collapsed sidebar, single main column where needed |
| 640–899 px | Navigation drawer, stacked panels, calendar defaults to list |
| < 640 px | Compact single-column layout; core workflows remain usable |

### Responsive rules

- Never require horizontal scrolling for primary workflows at 900 px or above.
- Tables convert to stacked rows/cards on narrow widths.
- Composer switches from side-by-side to tabs/stacked sections.
- Calendar switches Month/Week to List at narrow widths.
- Right inspectors become drawers.
- Dialogs become full-height sheets on narrow windows.
- Buttons remain touch-friendly (minimum 40 px target; 44 px preferred).
- Text zoom up to 200% must not hide critical actions.
- Keyboard navigation and focus order remain logical after layout changes.

Mobile browser support is not an MVP commitment; responsive behavior is primarily for narrow desktop windows and future portability.

## 7. User journeys

### Journey A — First-run setup

1. Launch PostFlow.
2. Welcome screen explains local-first storage and desktop scheduling constraints.
3. Create/select local workspace and brand.
4. Configure timezone.
5. Connect at least one social account or skip.
6. Configure an AI provider or skip.
7. Land on Overview with checklist and clear next action.

**Success:** user reaches the product without being forced to connect external services.

### Journey B — Create and schedule a multi-platform post

1. Select brand and click Create post.
2. Enter source text or request AI generation.
3. Review AI disclosure and select provider/model.
4. Select destination platforms/accounts.
5. Generate platform variants.
6. Edit each variant and inspect previews.
7. Attach media and run backend validation.
8. Save draft or approve exact revision.
9. Choose schedule date/time and timezone.
10. Confirm scheduling.
11. See each destination as an independent job in Calendar/Queue.

**Success:** all jobs persist with correct destination and exact approved revision; partial destination failure does not erase successful jobs.

### Journey C — Recover a failed publication

1. Overview shows a failed/attention-needed job.
2. User opens job detail and reads redacted reason and attempt history.
3. If failure is definitive and retryable, user chooses Retry.
4. If outcome is unknown, user chooses Reconcile.
5. PostFlow checks platform state where supported or requests manual resolution.
6. Only after reconciliation may a safe retry be offered.

**Success:** no duplicate publication caused by blind retry.

### Journey D — Manage an expired account

1. Account health changes to Reauthorization required.
2. User opens account detail.
3. User starts secure reauthorization.
4. OAuth state is validated and account identity is checked.
5. UI confirms restored connection and updated capabilities.
6. Affected jobs are revalidated before execution.

**Success:** credentials are renewed without exposing tokens or silently changing account identity.

### Journey E — Inspect analytics

1. User opens Analytics.
2. Selects date range and account.
3. UI shows only metrics returned by the platform.
4. User opens a post detail and sees metric provenance and last sync.
5. Missing metrics are explained.

**Success:** user can distinguish unavailable data from a measured zero.

## 8. Interaction and system states

Every data-driven screen must implement:
- Initial loading
- Refreshing
- Populated
- Empty (first-use and filtered-empty variants)
- Validation error
- Request failure
- Offline
- Partial integration failure
- Permission denied
- Stale data
- Destructive confirmation
- Success confirmation

### State presentation rules

- Keep user input when a request fails.
- Never clear the composer on an API error.
- Use inline errors for field-level problems and a page-level summary for multiple failures.
- Use toasts for transient confirmation, not for critical or actionable failures.
- Use persistent banners for worker stopped, offline and account reauthorization.
- Disable an action only with an explanation of why it is unavailable.
- Optimistic updates may be used only for reversible UI state; publishing and scheduling state changes wait for backend confirmation.
- Provide retry only when retry is safe and semantically correct.

## 9. Accessibility and usability requirements

Target WCAG 2.2 AA for the web-rendered UI where applicable.

- Full keyboard navigation.
- Visible focus ring with sufficient contrast.
- Semantic headings and landmarks.
- Labels for every input; placeholders are not labels.
- Accessible names for icon-only controls.
- Dialog focus trap and focus restoration.
- Screen-reader announcements for upload, generation and publishing state changes.
- Do not communicate state by color alone.
- Respect reduced-motion preferences.
- Contrast ratio: 4.5:1 for normal text and 3:1 for large text/UI components where applicable.
- Avoid time-only drag interactions; provide keyboard alternatives.

## 10. Frontend architecture and implementation guidance

Recommended feature structure:

```text
src/
  app/
    App.tsx
    router.tsx
    providers/
  components/
    layout/
    primitives/
    feedback/
    data-display/
  features/
    overview/
    calendar/
    content/
    composer/
    media/
    accounts/
    ai-providers/
    publishing/
    analytics/
    settings/
  services/
    api-client.ts
    query-client.ts
  hooks/
  styles/
    tokens.css
    globals.css
  types/
```

Implementation rules:
- Use typed API DTOs generated/validated against the FastAPI OpenAPI contract.
- Keep server state separate from local form state.
- Use a query/cache layer for server state and explicit invalidation after mutations.
- Use a form library only if it materially reduces validation complexity.
- Do not store secrets in localStorage, sessionStorage or frontend logs.
- Use route-level code splitting for non-core screens.
- Keep platform capability checks server-authoritative.
- Add stable test IDs only where semantic selectors are insufficient.

## 11. UX analytics and privacy

The local-first MVP should not introduce third-party behavioral analytics by default. Product telemetry, if introduced, must be opt-in and documented.

Operational audit events may be stored locally for security and recovery. Avoid logging full post text, prompts, media bytes, credentials, OAuth codes or provider response bodies unless explicitly required and safely redacted.

## 12. Acceptance criteria and release gates

### Navigation and layout
- [ ] Every MVP screen is reachable from the primary navigation or a contextual link.
- [ ] Active navigation state is correct for nested routes.
- [ ] Layout works at 1440, 1280, 1024, 900, 768 and 640 px widths.
- [ ] No primary workflow requires horizontal scrolling at desktop breakpoints.

### Composer and approval
- [ ] Source content and platform variants are visually distinct.
- [ ] Every destination has an independent variant and publish job.
- [ ] Variant edits invalidate approval for the prior revision.
- [ ] AI-generated content is editable and never auto-published.
- [ ] Validation uses backend platform/account capabilities.

### Publishing and recovery
- [ ] UI distinguishes queued, publishing, published, failed and unknown outcome.
- [ ] Unknown outcome offers reconciliation, not blind retry.
- [ ] Scheduling success is shown only after backend confirmation.
- [ ] Desktop worker limitations are disclosed.

### Security and privacy
- [ ] No credential/token value appears in UI, logs or API DTOs.
- [ ] AI data transmission is disclosed before external calls.
- [ ] Destructive actions require confirmation.
- [ ] Account permission and reauthorization states are clear.

### Quality
- [ ] Keyboard-only completion of core journeys is tested.
- [ ] Screen-reader labels and live status announcements are tested.
- [ ] Empty, loading, error, offline and partial-failure states exist.
- [ ] UI tests cover stale approval, job reconciliation and duplicate action prevention.

## 13. Open decisions

These items require product-owner confirmation before final visual implementation:
1. Final product logo and brand palette.
2. Default light/dark theme preference.
3. Whether campaigns are included in the first MVP navigation or deferred.
4. Exact platform capability matrix and account types after API verification.
5. Whether analytics is MVP or a later release depending on approved API access.
6. Final copy and interaction for worker lifecycle and Windows startup behavior.

**Design recommendation:** ship the light neutral work canvas with dark navigation as the initial default, retain a theme token architecture for a later dark theme, and prioritize Composer, Calendar, Queue and Account health over decorative dashboard widgets.

## M0 Reconciliation — UI Capability Boundaries

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. This addendum supersedes conflicting MVP scope and priorities in this document. The target is a single-user, local-first Windows desktop MVP. Windows 11 is the production support baseline; Windows 10 is best-effort development only. P0 includes Tauri 2/Rust, React/TypeScript, supervised FastAPI, SQLite/SQLAlchemy/Alembic, local media, source content and independent revisioned variants, one AI provider, exact human approval, durable per-destination publishing jobs, idempotency/immutable attempts/unknown-outcome reconciliation, one-time local scheduling, privacy, backup and restore. At most one official social-platform integration may be enabled, and only after a documented PASS feasibility gate. Scheduling requires the app/worker active, device awake and internet available. Campaigns, team membership/roles, collaboration, billing, SaaS, cloud scheduling, public API, cloud media relay, additional AI providers/platforms, multi-provider comparison/fallback and advanced social analytics are P1/Future, not MVP requirements.

Show one AI provider in P0; no comparison/fallback controls. Show no more than one social platform and only after PASS; otherwise offer platform-neutral export/manual assistance and state automated publishing is unavailable. Campaign, team/member, billing, SaaS and advanced analytics navigation are deferred. Dashboard metrics are local operational facts only. Distinguish queued/accepted from platform-confirmed published; unknown outcomes require reconciliation and must not offer blind retry. Disclose scheduler requirements persistently.
