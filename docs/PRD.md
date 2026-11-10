# PostFlow - Product Requirements Document (PRD)

| Document Information | Details |
|---|---|
| Product Name | PostFlow |
| Document | `PRD.md` |
| Document Type | Product Requirements Document |
| Version | 1.0 |
| Status | Draft - Pending Approval |
| Product Category | AI-Powered Social Media Management Platform |
| Initial Platform | Windows Desktop |
| Future Platform | Commercial SaaS |
| Primary Audience | Creators, Developers, Marketers and Businesses |
| Product Owner | PostFlow Product Owner |

---

# 1. Executive Summary

## 1.1 Product Overview

PostFlow is an AI-powered social media content creation, management, scheduling and publishing platform.

The application centralizes the complete social media content lifecycle, allowing users to generate content through multiple AI providers, adapt content for different social platforms, manage media assets, connect social accounts, approve publications, schedule posts and monitor publishing performance.

PostFlow will support integrations with:

### AI Providers

- OpenAI ChatGPT.
- Google Gemini.
- Anthropic Claude.
- Perplexity.
- Additional providers through an extensible adapter architecture.

### Social Media Platforms

- Instagram.
- LinkedIn.
- Facebook.
- Threads.
- X.
- Pinterest.
- Reddit.

Integration availability and publishing capabilities depend on official platform APIs, account eligibility, application permissions, commercial terms and approval requirements.

## 1.2 Product Vision

Build a unified, AI-powered social media management platform that reduces fragmented workflows and enables users to create, adapt, manage, schedule and publish content across multiple platforms.

## 1.3 Product Mission

Simplify social media operations through multi-provider AI intelligence, centralized content management and reliable publishing automation.

## 1.4 Core Value Proposition

**Create once. Adapt everywhere. Publish smarter.**

PostFlow provides:

- One interface for multiple AI providers.
- One workspace for multiple social accounts.
- One source of content for multiple platform-specific variants.
- One publishing calendar for planned content.
- One controlled workflow for approval and publishing.

---

# 2. Product Objectives

## 2.1 Primary Objectives

| ID | Objective | Expected Outcome |
|---|---|---|
| OBJ-001 | Centralize social media operations | Reduce fragmented workflows |
| OBJ-002 | Integrate multiple AI providers | Avoid dependency on one AI vendor |
| OBJ-003 | Automate platform adaptation | Reduce repetitive content editing |
| OBJ-004 | Simplify media management | Centralize images and videos |
| OBJ-005 | Simplify publishing | Provide a unified publishing workflow |
| OBJ-006 | Improve publishing reliability | Prevent duplicate and lost publishing jobs |
| OBJ-007 | Preserve human control | Support approval before publication |
| OBJ-008 | Establish extensibility | Enable future provider and platform integrations |
| OBJ-009 | Prepare for SaaS expansion | Support future multi-user deployment |

## 2.2 Business Objectives

1. Deliver a functional local-first desktop MVP.
2. Validate the usefulness of multi-provider AI content generation.
3. Validate real publishing integrations.
4. Establish a reusable integration architecture.
5. Validate demand among individual creators and small businesses.
6. Prepare a sustainable commercial SaaS expansion strategy.

## 2.3 Product Success Metrics

The following are proposed targets for MVP validation, not current product performance.

| Metric | Target |
|---|---:|
| AI providers integrated | At least 3 |
| AI providers targeted | 4 |
| Social platforms targeted | 7 |
| Core user workflows passing acceptance tests | 100% |
| Duplicate publications in defined retry tests | 0 |
| Recoverable scheduled jobs lost during restart tests | 0 |
| Critical security vulnerabilities at release | 0 |
| Successful backup restoration tests | 100% |
| Platform integrations represented accurately | 100% |

Platform support must be measured by verified capabilities, not the number of platform logos displayed in the interface.

---

# 3. Target Audience

## 3.1 Primary Users

### USER-001: Individual Content Creators

**Description:** Individuals who regularly publish content across social media platforms.

Requirements:

- Generate captions and descriptions.
- Create hashtags and keywords.
- Adapt content for multiple platforms.
- Manage media.
- Schedule publications.
- Track publication status.

### USER-002: Developers and Technical Content Creators

**Description:** Developers publishing programming tutorials, technical articles, project demonstrations and educational content.

Requirements:

- Generate technical content.
- Convert documentation into social posts.
- Maintain technical accuracy.
- Generate platform-specific descriptions.
- Reuse project content.
- Maintain a consistent technical brand voice.

### USER-003: Digital Marketers

**Description:** Marketing professionals managing campaigns and publishing content across multiple channels.

Requirements:

- Manage multiple brands.
- Create campaign content.
- Schedule posts.
- Maintain brand consistency.
- Compare AI-generated outputs.
- Monitor publishing performance.

### USER-004: Small Businesses

**Description:** Businesses managing their own social media presence.

Requirements:

- Connect business accounts.
- Create promotional content.
- Manage media assets.
- Schedule posts.
- Maintain a content calendar.
- Track available analytics.

### USER-005: Marketing Agencies

**Description:** Agencies managing social media operations for multiple clients.

Requirements:

- Multiple client workspaces.
- Brand-specific content.
- Multi-account management.
- Team approvals.
- Publishing coordination.
- Reporting.

Agency requirements are primarily future SaaS requirements and are not mandatory for the initial desktop MVP.

## 3.2 Initial Target Audience Priority

| Priority | User Segment |
|---|---|
| P0 | Individual content creators |
| P0 | Developers and technical creators |
| P1 | Freelancers |
| P1 | Small businesses |
| P2 | Digital marketing teams |
| P3 | Agencies and enterprises |

---

# 4. Product Scope

## 4.1 MVP Scope

The first release must focus on the following modules:

1. Application foundation.
2. Workspace and brand management.
3. AI provider management.
4. AI Content Studio.
5. Media Library.
6. Multi-Platform Composer.
7. Social Account Management.
8. Publishing Engine.
9. Scheduling System.
10. Publishing Calendar.
11. Application settings.
12. Backup and recovery.

## 4.2 Future Scope

The following features are planned for later releases:

- Commercial SaaS deployment.
- Multi-user collaboration.
- Advanced analytics.
- Campaign performance reporting.
- Team approval workflows.
- Subscription management.
- Usage-based billing.
- Advanced AI content evaluation.
- Automated content research.
- Intelligent publishing-time recommendations.
- Public API.
- Agency management.
- Advanced workflow automation.

## 4.3 Out of Scope

The initial MVP must not implement:

- Automated likes.
- Automated follows or unfollows.
- Automated comments.
- Automated direct messages.
- Fake engagement.
- Unauthorized scraping.
- CAPTCHA bypassing.
- Circumvention of platform restrictions.
- Autonomous publishing without configured authorization.
- Foundation model training.
- Full professional video editing.
- Unapproved browser automation for social publishing.

---

# 5. Product Architecture Requirements

## 5.1 Initial Technology Stack

| Layer | Technology |
|---|---|
| Desktop framework | Tauri 2 |
| Frontend | React |
| Frontend language | TypeScript |
| UI styling | CSS / Tailwind CSS |
| Backend | Python |
| API framework | FastAPI |
| Data validation | Pydantic |
| ORM | SQLAlchemy |
| Database | SQLite |
| Database migrations | Alembic |
| AI integrations | Official provider APIs |
| Image processing | Pillow |
| Video processing | FFmpeg |
| Testing | Pytest and frontend testing tools |
| Version control | Git |
| Repository hosting | GitHub |

Future SaaS infrastructure:

- PostgreSQL.
- Redis.
- Distributed background workers.
- Cloud media storage.
- Multi-tenant authentication.
- Centralized job processing.

## 5.2 Architectural Requirements

| ID | Requirement | Priority |
|---|---|---|
| ARC-001 | Implement modular application architecture | Must |
| ARC-002 | Separate frontend, backend and integration layers | Must |
| ARC-003 | Support independent AI provider adapters | Must |
| ARC-004 | Support independent social platform adapters | Must |
| ARC-005 | Maintain persistent publishing jobs | Must |
| ARC-006 | Use SQLite for initial desktop storage | Must |
| ARC-007 | Support database migrations | Must |
| ARC-008 | Keep platform-specific logic outside core publishing services | Must |
| ARC-009 | Support future PostgreSQL deployment | Should |
| ARC-010 | Support future SaaS deployment without replacing the domain model | Should |

---

# 6. Functional Requirements

Priority definitions:

- **P0 - Must:** Required for MVP release.
- **P1 - Should:** Important but can follow the core MVP.
- **P2 - Could:** Optional enhancement.
- **Future:** Planned for later product releases.

## 6.1 Module A - Application and Workspace Management

### Description

Manage application initialization, workspaces, brand profiles and general settings.

| ID | Functional Requirement | Priority |
|---|---|---|
| APP-001 | The application shall launch as a Windows desktop application | P0 |
| APP-002 | The application shall display a dashboard after initialization | P0 |
| APP-003 | Users shall be able to create a workspace | P0 |
| APP-004 | Users shall be able to edit workspace details | P0 |
| APP-005 | Users shall be able to create brand profiles | P0 |
| APP-006 | Users shall be able to edit and delete brand profiles | P0 |
| APP-007 | Each brand shall support a name, description and default language | P0 |
| APP-008 | Each brand shall support a configurable tone of voice | P0 |
| APP-009 | Users shall be able to configure application preferences | P0 |
| APP-010 | The application shall display system and integration status | P1 |
| APP-011 | Users shall be able to switch between workspaces | P1 |
| APP-012 | The application shall support multiple users and memberships | Future |

### Brand Profile Fields

- Brand name.
- Description.
- Website.
- Industry.
- Target audience.
- Brand voice.
- Preferred language.
- Keywords.
- Content guidelines.
- Prohibited terms.
- Default CTA.
- Logo and media assets.

### Acceptance Criteria

- A user can create, edit and delete a workspace or brand subject to its data dependencies.
- Brand settings are persisted after application restart.
- Generated content can reference the selected brand profile.
- Deleting a brand must not silently delete unrelated content or publication history.

---

## 6.2 Module B - AI Provider Management

### Description

Provide a unified interface for connecting and managing multiple AI providers.

### Initial Providers

1. OpenAI.
2. Google Gemini.
3. Anthropic Claude.
4. Perplexity.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| AI-001 | The system shall support an independent provider adapter architecture | P0 |
| AI-002 | Users shall be able to configure an OpenAI API credential | P0 |
| AI-003 | Users shall be able to configure a Gemini API credential | P0 |
| AI-004 | Users shall be able to configure a Claude API credential | P0 |
| AI-005 | Users shall be able to configure a Perplexity API credential | P1 |
| AI-006 | Users shall be able to select an available model | P0 |
| AI-007 | The system shall validate provider connectivity | P0 |
| AI-008 | The system shall display provider connection status | P0 |
| AI-009 | Users shall be able to select a default provider | P0 |
| AI-010 | Users shall be able to select a default model | P0 |
| AI-011 | The system shall support structured AI responses | P0 |
| AI-012 | The system shall track usage metadata | P1 |
| AI-013 | The system shall estimate API costs where pricing data is available | P1 |
| AI-014 | Users shall be able to compare outputs from multiple models | P1 |
| AI-015 | The system shall support provider fallback | P1 |
| AI-016 | The system shall support task-based model routing | P2 |
| AI-017 | Users shall be able to configure AI usage limits | P1 |
| AI-018 | The system shall maintain a provider request history | P1 |
| AI-019 | The system shall support additional providers without changing the content domain model | P0 |

### Provider Adapter Interface

Each provider adapter should implement a common internal contract:

- `validate_credentials()`
- `list_models()`
- `generate_text()`
- `generate_structured()`
- `analyze_image()` where supported
- `get_usage()` where supported
- `health_check()`

Actual operations must be capability-checked. Do not assume every provider supports identical models, inputs, structured output or usage reporting.

### AI Provider Configuration

Each provider configuration must include:

- Provider identifier.
- Display name.
- API credential reference.
- Selected model.
- Enabled status.
- Connection status.
- Supported capabilities.
- Last successful request.
- Last error.
- Usage metadata.

### Acceptance Criteria

- A user can connect at least one supported AI provider.
- Invalid credentials produce a clear error.
- Provider failures do not crash the application.
- A provider can be disabled without deleting previously generated content.
- API keys are never exposed in frontend responses or logs.
- Switching providers does not require changing the content-generation interface.

---

## 6.3 Module C - AI Content Studio

### Description

Generate, edit, refine and manage content through multiple AI providers.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| CST-001 | Users shall be able to create a content item | P0 |
| CST-002 | Users shall be able to enter a topic or content brief | P0 |
| CST-003 | Users shall be able to select a brand profile | P0 |
| CST-004 | Users shall be able to select an AI provider | P0 |
| CST-005 | Users shall be able to select an AI model | P0 |
| CST-006 | Users shall be able to generate a title | P0 |
| CST-007 | Users shall be able to generate descriptions | P0 |
| CST-008 | Users shall be able to generate captions | P0 |
| CST-009 | Users shall be able to generate hashtags | P0 |
| CST-010 | Users shall be able to generate keywords | P0 |
| CST-011 | Users shall be able to generate CTAs | P0 |
| CST-012 | Users shall be able to generate alt text | P0 |
| CST-013 | Users shall be able to regenerate content | P0 |
| CST-014 | Users shall be able to refine existing content | P0 |
| CST-015 | Users shall be able to save generated content as a draft | P0 |
| CST-016 | Users shall be able to compare multiple AI outputs | P1 |
| CST-017 | Users shall be able to generate content from uploaded images | P1 |
| CST-018 | Users shall be able to generate content from existing text or URLs | P1 |
| CST-019 | Users shall be able to save reusable prompt templates | P1 |
| CST-020 | Users shall be able to configure brand-specific generation instructions | P1 |
| CST-021 | Users shall be able to generate multilingual content | P2 |

### Content Generation Inputs

- Topic.
- Content objective.
- Content type.
- Target audience.
- Brand.
- Tone.
- Language.
- Platform selection.
- Keywords.
- CTA.
- Additional instructions.
- Optional media attachments.

### Content Generation Outputs

- Title.
- Main content.
- Description.
- Caption.
- Hashtags.
- Keywords.
- CTA.
- Alt text.
- Suggested content format.
- Sources, where applicable.
- Provider and model metadata.

### Content Generation Rules

1. AI-generated content must be editable.
2. Generated content must not be published automatically merely because generation succeeded.
3. AI outputs must be validated before persistence.
4. Source attribution must be retained when research results are used.
5. AI-generated factual claims must not be treated as verified facts.
6. Provider failures must preserve existing content.
7. Each generation operation must record its provider, model and prompt-template version.

### Acceptance Criteria

- A user can generate a draft using a connected provider.
- A user can edit and save the result.
- A user can regenerate without unintentionally overwriting an existing approved variant.
- The application clearly identifies the provider and model used.
- Structured output validation rejects malformed responses and handles them safely.

---

## 6.4 Module D - AI Research and Content Intelligence

### Description

Support research-driven content creation using AI search and research providers.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| RES-001 | Users shall be able to research a content topic | P1 |
| RES-002 | The system shall support Perplexity API integration | P1 |
| RES-003 | Research results shall retain source references where available | P1 |
| RES-004 | Users shall be able to review research findings | P1 |
| RES-005 | Users shall be able to use approved research as content-generation context | P1 |
| RES-006 | The system shall distinguish sourced information from AI-generated suggestions | P1 |
| RES-007 | The system shall support reusable research briefs | P2 |

### Acceptance Criteria

- Research results are not automatically considered verified.
- Source references are preserved when returned by the provider.
- Users can inspect and edit research before using it.
- Research failures do not block ordinary content generation.

---

## 6.5 Module E - Media Library

### Description

Provide centralized storage and management of images and videos.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| MED-001 | Users shall be able to upload images | P0 |
| MED-002 | Users shall be able to upload videos | P0 |
| MED-003 | The system shall validate file types | P0 |
| MED-004 | The system shall validate file sizes | P0 |
| MED-005 | Users shall be able to preview supported media | P0 |
| MED-006 | Users shall be able to organize media assets | P0 |
| MED-007 | Users shall be able to associate media with content | P0 |
| MED-008 | The system shall preserve original uploaded files | P0 |
| MED-009 | Users shall be able to resize supported images | P1 |
| MED-010 | Users shall be able to compress supported media | P1 |
| MED-011 | Users shall be able to generate thumbnails | P1 |
| MED-012 | Users shall be able to search media assets | P1 |
| MED-013 | The system shall store media metadata | P0 |
| MED-014 | Users shall be able to delete media assets safely | P0 |

### Media Metadata

- Asset ID.
- Filename.
- MIME type.
- File size.
- Width.
- Height.
- Duration for video.
- Storage path.
- Checksum.
- Creation timestamp.
- Processing status.
- Associated content.
- Platform compatibility metadata.

### Acceptance Criteria

- Unsupported files are rejected with a clear error.
- Original assets are preserved when transformations are performed.
- File references remain valid after application restart.
- Deleting an asset referenced by scheduled or published content requires dependency-aware handling.
- File paths cannot be manipulated to access files outside authorized storage.

---

## 6.6 Module F - Multi-Platform Composer

### Description

Allow users to transform a source content item into separate platform-specific variants.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| CMP-001 | Users shall be able to select multiple social platforms | P0 |
| CMP-002 | Users shall be able to generate platform-specific variants | P0 |
| CMP-003 | Each platform variant shall be independently editable | P0 |
| CMP-004 | Each variant shall support separate captions | P0 |
| CMP-005 | Each variant shall support separate hashtags | P0 |
| CMP-006 | Each variant shall support media selection | P0 |
| CMP-007 | The system shall validate content against platform capabilities | P0 |
| CMP-008 | The system shall display a platform-specific preview | P0 |
| CMP-009 | Users shall be able to duplicate a variant | P1 |
| CMP-010 | Users shall be able to compare platform variants | P1 |
| CMP-011 | The system shall preserve source content independently of variants | P0 |
| CMP-012 | The system shall track variant revisions | P0 |

### Platform Adaptation

The application should adapt content based on:

- Text limits.
- Supported media types.
- Aspect ratio requirements.
- Platform-specific content structures.
- Hashtag conventions.
- Account capabilities.
- Publishing permissions.

Platform requirements must be driven by a versioned capability registry rather than hardcoded UI assumptions.

### Acceptance Criteria

- Editing one platform variant does not modify another.
- The source content remains unchanged when platform variants are edited.
- Unsupported media combinations are rejected before publishing.
- Validation errors explain the required correction.
- Platform previews clearly identify their limitations.

---

## 6.7 Module G - Social Account Management

### Description

Connect and manage supported social media accounts.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| ACC-001 | Users shall be able to initiate an account connection | P0 |
| ACC-002 | The system shall use official platform authentication mechanisms | P0 |
| ACC-003 | The system shall validate OAuth callback state | P0 |
| ACC-004 | The system shall store credentials securely | P0 |
| ACC-005 | Users shall be able to view connected accounts | P0 |
| ACC-006 | Users shall be able to view account connection status | P0 |
| ACC-007 | Users shall be able to disconnect accounts | P0 |
| ACC-008 | The system shall track token expiration where available | P0 |
| ACC-009 | The system shall support token refresh where supported | P0 |
| ACC-010 | The system shall display available account capabilities | P0 |
| ACC-011 | The system shall identify missing permissions | P0 |
| ACC-012 | The system shall support multiple accounts where permitted | P1 |

### Account Metadata

- Platform.
- Account identifier.
- Account name.
- Account type.
- Profile image URL where available.
- Granted scopes.
- Token expiry.
- Connection status.
- Available capabilities.
- Last successful API operation.

### Acceptance Criteria

- An account cannot be marked connected until the authentication process succeeds.
- Missing permissions are clearly displayed.
- Expired credentials produce actionable errors.
- Disconnecting an account prevents future jobs from using its credentials.
- Credentials are not returned through ordinary account APIs.

---

## 6.8 Module H - Publishing Engine

### Description

Publish approved platform-specific variants through official platform APIs.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| PUB-001 | Users shall be able to validate content before publishing | P0 |
| PUB-002 | Users shall be able to publish immediately | P0 |
| PUB-003 | Users shall be able to publish through approved scheduled jobs | P0 |
| PUB-004 | Each platform destination shall have an independent publishing job | P0 |
| PUB-005 | The system shall maintain publication attempt history | P0 |
| PUB-006 | The system shall record platform response identifiers | P0 |
| PUB-007 | The system shall track publishing status | P0 |
| PUB-008 | The system shall support retry policies | P0 |
| PUB-009 | The system shall support cancellation where execution has not passed the safe cancellation point | P0 |
| PUB-010 | The system shall prevent duplicate publication through idempotency and reconciliation | P0 |
| PUB-011 | The system shall handle rate limits | P0 |
| PUB-012 | The system shall handle expired credentials | P0 |
| PUB-013 | The system shall isolate platform failures | P0 |
| PUB-014 | Users shall be able to view publication history | P0 |
| PUB-015 | The system shall support publication reconciliation after uncertain outcomes | P0 |

### Publishing Rules

1. Publishing must use official platform APIs.
2. Every destination must have an independent job.
3. A failed platform must not block successful publication to other destinations.
4. Every attempt must be recorded.
5. Retry operations must not blindly repeat a possibly successful create operation.
6. Unknown outcomes must be reconciled before another create request.
7. Platform response IDs must be persisted.
8. Publishing must respect platform rate limits and permission requirements.

### Job States

- Draft.
- Awaiting approval.
- Approved.
- Scheduled.
- Queued.
- Publishing.
- Published.
- Retry pending.
- Failed.
- Cancelled.
- Outcome unknown.

### Acceptance Criteria

- A valid approved variant can be submitted for publishing.
- Independent destinations have independent job states.
- A failure on one platform does not invalidate successful results on another.
- Retry attempts preserve previous attempt history.
- An uncertain outcome is reconciled before another publication request.
- Duplicate publication is prevented in defined idempotency test scenarios.

---

## 6.9 Module I - Approval Workflow

### Description

Provide explicit user control over publication authorization.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| APR-001 | Users shall be able to review generated content | P0 |
| APR-002 | Users shall be able to approve a variant | P0 |
| APR-003 | Users shall be able to reject a variant | P0 |
| APR-004 | Users shall be able to edit content before approval | P0 |
| APR-005 | The system shall record approval timestamps | P0 |
| APR-006 | The system shall associate approval with an exact content revision | P0 |
| APR-007 | Editing an approved variant shall invalidate approval for the changed revision | P0 |
| APR-008 | The system shall support approval policies | P1 |
| APR-009 | The system shall support multi-user approvals | Future |

### Approval Policies

**Manual Approval**

Every publication requires explicit user approval.

**Approved Scheduling**

Users approve content before it enters the scheduled publishing queue.

**Configured Automatic Publishing**

Users may explicitly enable an automation policy for eligible content and destinations. Policy scope, permissions and safeguards must be visible.

Default behavior: manual approval required.

### Acceptance Criteria

- AI generation cannot implicitly authorize publication.
- Approval is linked to a specific content revision.
- Editing an approved revision invalidates its approval.
- Rejected content cannot be published through the normal publishing workflow.

---

## 6.10 Module J - Scheduling System

### Description

Provide persistent scheduling and background job execution.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| SCH-001 | Users shall be able to schedule posts | P0 |
| SCH-002 | Users shall be able to select publication date and time | P0 |
| SCH-003 | Users shall be able to select a timezone | P0 |
| SCH-004 | Users shall be able to view scheduled jobs | P0 |
| SCH-005 | Users shall be able to pause eligible jobs | P1 |
| SCH-006 | Users shall be able to resume paused jobs | P1 |
| SCH-007 | Users shall be able to cancel pending jobs | P0 |
| SCH-008 | The system shall persist jobs in the database | P0 |
| SCH-009 | The system shall recover eligible jobs after application restart | P0 |
| SCH-010 | The system shall prevent concurrent execution of the same job | P0 |
| SCH-011 | The system shall track execution attempts | P0 |
| SCH-012 | The system shall support configurable retry delays | P1 |
| SCH-013 | The system shall report missed schedules | P0 |

### Scheduling Rules

- Store timestamps in UTC.
- Preserve the selected display timezone.
- Handle daylight-saving changes where applicable.
- Prevent duplicate job execution.
- Persist the next execution time.
- Do not silently publish expired or invalid jobs.
- Require the desktop service to be operational at the scheduled time.

### Operational Limitation

The initial desktop application cannot guarantee publication while the computer is shut down, disconnected or the application/background service is unavailable.

The UI must communicate this limitation clearly.

### Acceptance Criteria

- Scheduled jobs survive application restarts.
- The scheduler does not execute a job more than once concurrently.
- Jobs missed while the application is offline are handled according to a documented recovery policy.
- Timezone conversion is tested.
- A job cannot be scheduled without a valid destination, content revision and authorization.

---

## 6.11 Module K - Publishing Calendar

### Description

Display content and publishing jobs in a calendar interface.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| CAL-001 | Users shall be able to view a monthly calendar | P0 |
| CAL-002 | Users shall be able to view scheduled posts | P0 |
| CAL-003 | Users shall be able to view publication statuses | P0 |
| CAL-004 | Users shall be able to filter by platform | P1 |
| CAL-005 | Users shall be able to filter by brand | P1 |
| CAL-006 | Users shall be able to open content from the calendar | P0 |
| CAL-007 | Users shall be able to reschedule eligible jobs | P1 |
| CAL-008 | Users shall be able to view daily and weekly schedules | P1 |

### Acceptance Criteria

- Scheduled posts appear at their correct local times.
- Calendar status matches the publishing job state.
- Rescheduling updates the persistent job.
- Published records remain visible as historical entries.

---

## 6.12 Module L - Analytics and Reporting

### Description

Display analytics obtained from supported platform APIs.

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| ANA-001 | The application shall record available publication metrics | P1 |
| ANA-002 | Users shall be able to view analytics by platform | P1 |
| ANA-003 | Users shall be able to view metrics by published post | P1 |
| ANA-004 | Users shall be able to view available engagement metrics | P1 |
| ANA-005 | The system shall store analytics snapshots | P1 |
| ANA-006 | The system shall display metric collection timestamps | P1 |
| ANA-007 | The system shall identify unavailable metrics | P0 |
| ANA-008 | Users shall be able to filter analytics by date range | P1 |
| ANA-009 | Users shall be able to export reports | P2 |

### Analytics Rules

- Only actual API-returned or otherwise verifiably sourced metrics may be displayed as real metrics.
- Missing data must not be represented as zero unless zero was actually reported.
- Metrics must identify their platform and collection timestamp.
- Different platform metrics must not be combined without defining their meaning.
- Analytics availability depends on platform permissions and API support.

---

## 6.13 Module M - Settings and Data Management

### Functional Requirements

| ID | Functional Requirement | Priority |
|---|---|---|
| SET-001 | Users shall be able to configure application preferences | P0 |
| SET-002 | Users shall be able to configure default timezone | P0 |
| SET-003 | Users shall be able to configure default AI provider | P0 |
| SET-004 | Users shall be able to configure content defaults | P1 |
| SET-005 | Users shall be able to create local backups | P0 |
| SET-006 | Users shall be able to restore valid backups | P0 |
| SET-007 | Users shall be able to inspect application logs | P1 |
| SET-008 | Users shall be able to export content data | P1 |
| SET-009 | Users shall be able to delete selected local data | P0 |
| SET-010 | The system shall provide application version information | P0 |

### Acceptance Criteria

- Backup operations preserve database consistency.
- Restoration validates backup integrity.
- Restore operations do not silently overwrite data without confirmation.
- Sensitive credentials are handled separately from ordinary data exports.

---

# 7. User Interface Requirements

## 7.1 Main Navigation

The application shall provide the following primary navigation:

1. Dashboard.
2. AI Content Studio.
3. AI Providers.
4. Media Library.
5. Composer.
6. Publishing Calendar.
7. Publishing Queue.
8. Connected Accounts.
9. Analytics.
10. Campaigns.
11. Brand Management.
12. Settings.

## 7.2 Dashboard

The dashboard should display:

- Total content drafts.
- Scheduled posts.
- Published posts.
- Failed publishing jobs.
- Connected account status.
- AI provider status.
- Upcoming scheduled publications.
- Recent activity.

Any sample or placeholder metrics must be visibly identified as demo data and must never be represented as real production analytics.

## 7.3 AI Content Studio

The interface should include:

- Topic or brief input.
- Brand selection.
- AI provider selector.
- Model selector.
- Tone selection.
- Language selection.
- Platform selection.
- Media attachment.
- Generate action.
- Generated content editor.
- Regenerate and refine actions.
- Save draft action.

## 7.4 Composer

The composer should support:

- Multi-platform selection.
- Separate platform variants.
- Individual caption editors.
- Hashtag editors.
- Media previews.
- Platform validation.
- Approval status.
- Publishing options.

## 7.5 Design Requirements

Use the PostFlow dark technical design system.

| Design Token | Value |
|---|---|
| Background | `#010D18` |
| Surface | `#151E2C` |
| Elevated Surface | `#18283A` |
| Primary Text | `#FFFFFF` |
| Body Text | `#B7C1CB` |
| Muted Text | `#8E9AAB` |
| Orange Accent | `#E54415` |
| Teal Accent | `#19BAAF` |

Requirements:

- Consistent navigation.
- Clear visual hierarchy.
- Responsive layouts.
- Accessible contrast.
- Clear loading and error states.
- No unnecessary decorative animations.
- No misleading provider or platform status indicators.
- Consistent design tokens across all modules.

---

# 8. Non-Functional Requirements

## 8.1 Performance

| ID | Requirement | Target |
|---|---|---|
| NFR-001 | Application startup | Target under 5 seconds on reference hardware after initial setup |
| NFR-002 | Local database queries | Target under 500 ms for ordinary indexed queries |
| NFR-003 | UI interaction | Target under 200 ms for ordinary local interactions |
| NFR-004 | AI operations | Display progress and allow cancellation where supported |
| NFR-005 | Media processing | Run asynchronously without freezing the UI |
| NFR-006 | Background execution | Avoid unnecessary continuous resource consumption |
| NFR-007 | Memory | Target under 1 GB application memory during normal idle/light workflows, subject to measurement |

Performance targets must be benchmarked on the actual reference hardware. Network and third-party API latency are outside the application's direct control.

## 8.2 Reliability

| ID | Requirement |
|---|---|
| NFR-008 | Persist critical publishing state |
| NFR-009 | Recover eligible jobs after application restart |
| NFR-010 | Prevent duplicate concurrent job execution |
| NFR-011 | Preserve publication attempt history |
| NFR-012 | Handle network interruption |
| NFR-013 | Handle provider downtime |
| NFR-014 | Handle expired OAuth credentials |
| NFR-015 | Preserve existing content when generation fails |

## 8.3 Security

| ID | Requirement |
|---|---|
| NFR-016 | Protect API credentials using OS-backed secure storage |
| NFR-017 | Never expose credentials to the frontend |
| NFR-018 | Protect local backend endpoints |
| NFR-019 | Validate OAuth state |
| NFR-020 | Validate uploaded files |
| NFR-021 | Prevent path traversal |
| NFR-022 | Redact sensitive data from logs |
| NFR-023 | Record security-relevant actions |
| NFR-024 | Enforce approval before publishing |
| NFR-025 | Protect against unauthorized publishing requests |

## 8.4 Privacy

| ID | Requirement |
|---|---|
| NFR-026 | Keep local application data local by default |
| NFR-027 | Disclose when content or media is sent to cloud AI providers |
| NFR-028 | Identify the configured AI provider |
| NFR-029 | Explain provider-specific data handling and retention policies |
| NFR-030 | Do not transmit content to unselected providers |
| NFR-031 | Allow users to disconnect providers and social accounts |
| NFR-032 | Support local data export and deletion |

## 8.5 Maintainability

| ID | Requirement |
|---|---|
| NFR-033 | Maintain modular backend services |
| NFR-034 | Maintain independent integration adapters |
| NFR-035 | Use database migrations |
| NFR-036 | Maintain automated tests |
| NFR-037 | Document public API contracts |
| NFR-038 | Maintain structured logging |
| NFR-039 | Use version-controlled configuration |
| NFR-040 | Document architectural decisions |

## 8.6 Scalability

| ID | Requirement |
|---|---|
| NFR-041 | Separate domain logic from desktop infrastructure |
| NFR-042 | Support PostgreSQL migration |
| NFR-043 | Support future distributed job processing |
| NFR-044 | Prepare the domain model for tenant isolation |
| NFR-045 | Avoid embedding local filesystem assumptions in core domain services |

---

# 9. Integration Requirements

## 9.1 AI Provider Integrations

| Provider | Integration | Primary Use |
|---|---|---|
| OpenAI | Official API | Content generation and structured outputs |
| Google Gemini | Official API | Multimodal generation and image analysis |
| Anthropic Claude | Official API | Content refinement and brand voice |
| Perplexity | Official API | Research and source-backed content |

The application must use provider-specific adapters and normalize responses into internal schemas.

## 9.2 Social Platform Integrations

| Platform | Intended MVP capability | Important dependency |
|---|---|---|
| Instagram | Eligible professional-account publishing | Meta permissions and media requirements |
| LinkedIn | Member or organization publishing where approved | Product access and scopes |
| Facebook | Page publishing | Page permissions and token requirements |
| Threads | Supported post publishing | Threads API access |
| X | Supported post publishing | Developer access, rate limits and pricing |
| Pinterest | Pin creation | Board and Pin permissions |
| Reddit | Supported submission workflows where authorized | API terms, commercial-use restrictions and subreddit rules |

### Integration Priority

Recommended implementation order:

1. LinkedIn.
2. Facebook.
3. Instagram.
4. Threads.
5. Pinterest.
6. X.
7. Reddit.

The actual order must be revised based on API access, user demand, implementation feasibility and cost.

## 9.3 Integration Architecture Requirements

- Each provider must have an independent adapter.
- Provider-specific authentication must be isolated.
- API versions must be configurable where appropriate.
- Rate limits must be respected.
- Errors must be normalized without losing useful provider details.
- Integration tests must use official sandbox or authorized test environments where available.
- Unsupported operations must be explicitly reported.

---

# 10. Core User Workflows

## 10.1 Workflow A - Generate Content

1. User opens AI Content Studio.
2. User selects a brand.
3. User enters a topic or brief.
4. User selects an AI provider.
5. User selects an available model.
6. User selects content settings.
7. User submits a generation request.
8. Backend validates the request.
9. AI provider generates structured content.
10. Backend validates the response.
11. Content is saved as a draft.
12. User reviews and edits the result.

**Expected result:** A saved, editable content draft.

## 10.2 Workflow B - Generate Multi-Platform Content

1. User selects a source content item.
2. User chooses destination platforms.
3. System checks supported capabilities.
4. AI generates individual variants.
5. System validates each variant.
6. User edits platform-specific content.
7. User saves the variants.

**Expected result:** Separate editable variants linked to one source item.

## 10.3 Workflow C - Publish Content

1. User selects a platform variant.
2. User selects a connected social account.
3. System validates account permissions.
4. System validates content and media.
5. System checks approval state.
6. User confirms publishing.
7. System creates a publishing job.
8. Publishing worker executes the job.
9. Platform response is recorded.
10. User sees the final status.

**Expected result:** A recorded publishing attempt and an accurate outcome.

## 10.4 Workflow D - Schedule Content

1. User selects a valid platform variant.
2. User selects an eligible account.
3. User chooses publication date and time.
4. System validates the schedule.
5. System checks approval.
6. System creates a persistent scheduled job.
7. Calendar displays the scheduled post.
8. Scheduler executes the job when due.
9. User can inspect the result.

**Expected result:** A persistent scheduled publishing job.

## 10.5 Workflow E - Recover Publishing Jobs

1. Application or background service restarts.
2. Scheduler loads persisted jobs.
3. System identifies overdue and interrupted jobs.
4. System examines previous attempts.
5. System reconciles uncertain outcomes where possible.
6. Safe jobs return to the eligible queue.
7. User sees unrecoverable or ambiguous jobs.

**Expected result:** No silent loss or blind duplicate execution.

---

# 11. Data Requirements

## 11.1 Core Entities

The initial data model should include:

- User.
- Workspace.
- Workspace Member.
- Brand.
- Social Account.
- OAuth Credential Reference.
- AI Provider Configuration.
- AI Model Metadata.
- Content Item.
- Media Asset.
- Post Variant.
- Prompt Template.
- Publish Job.
- Publish Attempt.
- Published Post.
- Campaign.
- Analytics Snapshot.
- Audit Log.
- Application Setting.

## 11.2 Data Integrity Rules

1. Every content item must belong to a workspace.
2. Every post variant must reference a source content item.
3. Every publishing job must reference a specific variant revision.
4. Every publishing job must reference a destination account.
5. Approval must be linked to the exact variant revision.
6. Publication attempts must be immutable historical records.
7. A successful platform publication must retain its platform response identifier where available.
8. Credentials must be stored separately from ordinary business records.
9. Deleting an account must not erase publication history.
10. A database migration must preserve existing data.
11. Publication idempotency must distinguish retries from intentional reposts.
12. A source content item must remain independent of its platform-specific variants.

---

# 12. Application States and Error Handling

## 12.1 Content States

- Draft.
- Generating.
- Generated.
- Needs Review.
- Approved.
- Rejected.
- Archived.

## 12.2 Publishing States

- Draft.
- Awaiting Approval.
- Approved.
- Scheduled.
- Queued.
- Publishing.
- Published.
- Retry Pending.
- Failed.
- Cancelled.
- Outcome Unknown.

## 12.3 Error Categories

- Authentication Error.
- Permission Error.
- Validation Error.
- Rate Limit Error.
- Provider Unavailable.
- Network Error.
- Media Processing Error.
- Publishing Error.
- Database Error.
- Unknown Error.

## 12.4 Error Handling Requirements

- Display actionable error messages.
- Preserve user-entered data.
- Do not expose access tokens or API keys.
- Record correlation IDs for troubleshooting.
- Retry only when safe.
- Distinguish transient and permanent errors.
- Preserve full attempt history.
- Never silently report a failed job as successful.

---

# 13. Authentication and Authorization Requirements

## 13.1 Local Desktop Authentication

The initial desktop version must protect local backend communication.

Requirements:

- Backend binds to localhost only.
- Random per-installation local API secret.
- Secure storage of sensitive configuration.
- Restricted desktop capabilities.
- Validated request origins and authorization.
- No public backend exposure by default.

## 13.2 Social Account Authorization

- Use official OAuth workflows.
- Validate callback state.
- Use PKCE where supported.
- Request only required permissions.
- Encrypt or securely reference tokens.
- Refresh credentials where supported.
- Allow explicit disconnection.

## 13.3 Future SaaS Authorization

Future requirements:

- User authentication.
- Role-based access control.
- Workspace membership.
- Tenant isolation.
- Team permissions.
- Audit trails.
- Secure session management.

---

# 14. Deployment and Operational Requirements

## 14.1 Desktop Deployment

- Windows installer.
- Application configuration management.
- Local database initialization.
- Local media storage.
- Backend lifecycle management.
- Background scheduler lifecycle management.
- Application logging.
- Database backups.
- Application update mechanism.

## 14.2 Desktop Runtime Constraints

The initial application must be optimized for systems with limited memory and processing capacity.

Requirements:

- Avoid local LLM inference.
- Avoid unnecessary background workers.
- Use asynchronous I/O.
- Limit concurrent media processing.
- Limit concurrent AI requests.
- Avoid unnecessary local infrastructure.
- Avoid requiring Docker or Kubernetes for normal desktop usage.

## 14.3 Future SaaS Deployment

- Cloud-hosted backend.
- PostgreSQL.
- Redis-backed job processing.
- Object storage.
- Multi-tenant authentication.
- Monitoring.
- Centralized logs.
- Usage and billing controls.
- Backup and disaster recovery.

---

# 15. Testing Requirements

## 15.1 Unit Testing

Test:

- Domain services.
- AI adapter normalization.
- Platform validation.
- Content transformations.
- Database operations.
- Scheduler logic.
- Idempotency.
- Permission checks.

## 15.2 Integration Testing

Test:

- SQLite integration.
- AI provider integrations.
- OAuth workflows.
- Media processing.
- Publishing adapters.
- Job persistence.
- Retry handling.
- Backup and restoration.

## 15.3 End-to-End Testing

Validate:

- Workspace creation.
- Brand configuration.
- AI provider connection.
- Content generation.
- Platform adaptation.
- Media upload.
- Account connection.
- Approval.
- Scheduling.
- Publishing.
- Application restart recovery.

## 15.4 Security Testing

Validate:

- Secret leakage.
- Unauthorized local API requests.
- OAuth state validation.
- Path traversal.
- Malicious uploads.
- Prompt injection handling.
- Publishing authorization.
- Data isolation.
- Backup security.

## 15.5 Release Quality Gates

A release must not proceed if:

- Critical or high-severity unresolved security issues remain.
- Database migrations fail.
- Core acceptance tests fail.
- Duplicate publication prevention tests fail.
- Credential leakage is detected.
- Backup restoration is unverified.
- Publishing jobs can be silently lost.
- A platform is presented as supported without verified API capability.

---

# 16. MVP Release Criteria

The MVP is ready for release when all of the following are satisfied.

### Product

- [ ] Application launches successfully.
- [ ] Workspace and brand management work.
- [ ] At least one AI provider is integrated and tested.
- [ ] AI-generated content can be saved and edited.
- [ ] Platform-specific variants can be created.
- [ ] Media can be uploaded and managed.
- [ ] At least one social platform can be connected.
- [ ] At least one real publishing workflow is verified.
- [ ] Approval workflow works.
- [ ] Scheduling and recovery work.
- [ ] Publishing history is available.
- [ ] Backup and restoration work.

### Engineering

- [ ] Database migrations are verified.
- [ ] Automated unit tests pass.
- [ ] Integration tests pass.
- [ ] Core E2E tests pass.
- [ ] API contracts are documented.
- [ ] Security review is complete.
- [ ] Logs do not expose secrets.
- [ ] Application startup and resource usage are benchmarked.
- [ ] Installer and update behavior are tested.

### Platform Integrations

- [ ] Supported operations are documented per platform.
- [ ] Required permissions are documented.
- [ ] Account eligibility is validated.
- [ ] Error handling is implemented.
- [ ] Rate limits are respected.
- [ ] Real API integration tests pass.

---

# 17. Product Roadmap

| Phase | Name | Primary Deliverables |
|---|---|---|
| Phase 0 | Engineering Foundation | Repository, configuration, CI, architecture baseline |
| Phase 1 | Desktop Foundation | Tauri, React, FastAPI, SQLite, workspace |
| Phase 2 | Media Management | Upload, validation, processing, library |
| Phase 3 | AI Content Engine | Provider adapters, prompts, generation |
| Phase 4 | Composer | Platform variants, preview, validation |
| Phase 5 | Social Integrations | OAuth, account management, platform adapters |
| Phase 6 | Publishing Engine | Publishing jobs, approval, retries |
| Phase 7 | Scheduling and Calendar | Persistent scheduling, recovery, calendar |
| Phase 8 | Analytics and Quality | Metrics, reporting, advanced testing |
| Phase 9 | SaaS Foundation | Multi-tenancy, PostgreSQL, cloud workers, billing |

Phases may be adjusted after platform feasibility research. Each phase must have independent acceptance criteria and a release gate.

---

# 18. Dependencies and Constraints

## 18.1 External Dependencies

- AI provider API availability.
- AI provider account and billing access.
- Social platform developer accounts.
- Platform application approval.
- OAuth permissions.
- Media hosting requirements.
- Platform API rate limits.
- Platform commercial usage terms.
- FFmpeg availability and licensing review.

## 18.2 Technical Constraints

- Initial deployment is local-first.
- Initial database is SQLite.
- AI inference is cloud-based.
- Desktop scheduling depends on the machine and scheduler being operational.
- Publishing capabilities vary by platform.
- Analytics depend on API access.
- Future SaaS requirements must not compromise desktop data security.

## 18.3 Business Constraints

- Avoid expensive infrastructure in the initial release.
- Validate real user demand before SaaS expansion.
- Monitor AI API usage costs.
- Consider BYOK for future commercial plans.
- Evaluate platform-specific licensing and commercial restrictions before monetization.

---

# 19. Risks and Mitigation

| Risk ID | Risk | Impact | Mitigation |
|---|---|---|---|
| RISK-001 | Social platform API restrictions | High | Early feasibility validation |
| RISK-002 | AI provider cost escalation | High | BYOK, quotas and usage tracking |
| RISK-003 | OAuth implementation complexity | High | Independent integration adapters |
| RISK-004 | Duplicate publications | Critical | Idempotency and outcome reconciliation |
| RISK-005 | Desktop scheduler downtime | High | Persistent queue and recovery |
| RISK-006 | AI-generated misinformation | High | Research citations and human review |
| RISK-007 | Credential compromise | Critical | OS-backed secure storage |
| RISK-008 | Media incompatibility | Medium | Capability-based validation |
| RISK-009 | Platform API changes | High | Versioned adapters and maintenance |
| RISK-010 | SaaS complexity | High | Separate deployment profile and phased expansion |

---

# 20. Assumptions Requiring Validation

The following assumptions must be verified before their corresponding implementation begins:

1. Required API access can be obtained for the target social platforms.
2. The selected accounts are eligible for the intended publishing operations.
3. The selected AI providers support the required API capabilities.
4. AI API costs are commercially sustainable.
5. Media hosting requirements can be met within the initial architecture.
6. Local scheduling behavior meets the intended desktop use case.
7. Platform API terms permit the intended personal and commercial usage.
8. Analytics permissions are available for the intended metrics.
9. Future SaaS tenant isolation can be achieved without compromising local-first architecture.

Unverified assumptions must remain explicitly marked as unverified in project documentation.

---

# 21. Product Decisions and Open Questions

## 21.1 Proposed Decisions

| Decision | Proposed Direction |
|---|---|
| Product name | PostFlow |
| Initial deployment | Windows desktop |
| Future deployment | SaaS |
| Frontend | React + TypeScript |
| Backend | FastAPI |
| Desktop framework | Tauri 2 |
| Database | SQLite |
| AI architecture | Multi-provider adapters |
| Initial AI providers | OpenAI, Gemini, Claude, Perplexity |
| Social platforms | Instagram, LinkedIn, Facebook, Threads, X, Pinterest, Reddit |
| Publishing authorization | Manual approval by default |
| Scheduler | Persistent local job execution |
| Media storage | Local-first |
| SaaS database | PostgreSQL |
| AI billing strategy | BYOK initially where appropriate |

## 21.2 Open Questions

These questions require product-owner approval:

1. Should the first MVP support all four AI providers, or launch with OpenAI and Gemini before adding Claude and Perplexity?
2. Which social platform should be the first fully verified publishing integration?
3. Should users be able to provide their own external media-hosting credentials when required by publishing APIs?
4. Should multi-model comparison be included in the first MVP or a later release?
5. Should the initial desktop release support only one workspace or multiple workspaces?
6. Should campaign management be included in the MVP?
7. Should the desktop application support automatic publishing policies, or should the initial release require manual approval for every post?

---

# 22. Definition of Done

A feature is considered complete only when:

1. Requirements are implemented.
2. UI behavior is verified.
3. Backend logic is tested.
4. Data persistence is verified.
5. Error handling is implemented.
6. Security requirements are checked.
7. Documentation is updated.
8. Relevant automated tests pass.
9. Acceptance criteria are satisfied.
10. No unresolved release-blocking defect remains.

A feature is not complete merely because its UI has been generated or its code compiles.

---

# 23. Final Product Requirement Statement

PostFlow must provide a reliable, secure and extensible environment for managing the complete social media content lifecycle.

The MVP must establish the foundation for:

- Multi-provider AI content generation.
- Brand-aware content management.
- Platform-specific content adaptation.
- Media asset management.
- Official social account integrations.
- Human-controlled publishing.
- Persistent scheduling.
- Publication status tracking.
- Reliable recovery and data integrity.

The first release must prioritize a working end-to-end workflow over a large number of incomplete integrations.

**Product principle: Build a reliable publishing workflow first. Expand the automation and intelligence layer after the core workflow is proven.**

---

# 24. Document Approval

| Role | Responsibility | Status |
|---|---|---|
| Product Owner | Approve requirements and MVP scope | Pending |
| Product Architect | Validate system boundaries | Pending |
| Engineering Lead | Validate technical feasibility | Pending |
| Security Reviewer | Review security requirements | Pending |
| QA Lead | Review testability and acceptance criteria | Pending |

**Next document:** `USER_STORIES.md` - Detailed user stories, actors, workflows, preconditions, postconditions and edge cases.

## M0 Reconciliation — Controlling MVP Scope

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. This addendum supersedes conflicting MVP scope and priorities in this document. The target is a single-user, local-first Windows desktop MVP. Windows 11 is the production support baseline; Windows 10 is best-effort development only. P0 includes Tauri 2/Rust, React/TypeScript, supervised FastAPI, SQLite/SQLAlchemy/Alembic, local media, source content and independent revisioned variants, one AI provider, exact human approval, durable per-destination publishing jobs, idempotency/immutable attempts/unknown-outcome reconciliation, one-time local scheduling, privacy, backup and restore. At most one official social-platform integration may be enabled, and only after a documented PASS feasibility gate. Scheduling requires the app/worker active, device awake and internet available. Campaigns, team membership/roles, collaboration, billing, SaaS, cloud scheduling, public API, cloud media relay, additional AI providers/platforms, multi-provider comparison/fallback and advanced social analytics are P1/Future, not MVP requirements.

Remove provider-count and platform-count targets as MVP success metrics. Measure verified outcomes: clean Windows 11 install, secure local API, persistence/restore, source/variant isolation, exact-approval enforcement, no blind retry of unknown outcomes, one live AI-provider workflow and verified live publishing only if the platform gate passes. PRD approval remains pending until product-owner acceptance is recorded.
