# PostFlow - Test Plan

**Document:** `TEST_PLAN.md`  
**Product:** PostFlow  
**Version:** 1.1  
**Status:** Baseline QA Specification  
**Platform:** Windows 10 / Windows 11 Desktop  
**Architecture:** Tauri 2 + React + TypeScript + Python FastAPI + SQLite  
**Related Documents:**
- `PRODUCT_VISION.md`
- `PRD.md`
- `USER_STORIES.md`
- `ACCEPTANCE_CRITERIA.md`

---

# 1. Purpose

This document defines the software testing strategy, test scope, test cases, automation requirements, test environments, execution procedures, and release quality gates for PostFlow.

The objective is to verify that PostFlow:

- Implements the documented product requirements.
- Produces correct and predictable results.
- Protects user credentials and social account access.
- Handles AI provider failures safely.
- Publishes content without unintended duplication.
- Preserves content, media, and publishing history.
- Recovers correctly after interruptions and application restarts.
- Complies with supported social platform API workflows.
- Remains usable on the target Windows desktop environment.

Testing must cover both successful workflows and failure conditions.

A feature is not accepted simply because its primary happy path works.

# 2. Testing Objectives

| ID | Objective | Expected outcome |
|---|---|---|
| OBJ-001 | Functional correctness | Features behave according to requirements |
| OBJ-002 | Data integrity | No unintended data loss or corruption |
| OBJ-003 | Security | Credentials and account access remain protected |
| OBJ-004 | AI reliability | Provider failures and invalid output are handled safely |
| OBJ-005 | Publishing reliability | No unintended duplicate posts |
| OBJ-006 | Scheduling reliability | Scheduled jobs survive restart |
| OBJ-007 | Platform compliance | Integrations use supported official APIs |
| OBJ-008 | Performance | Application remains usable on baseline hardware |
| OBJ-009 | Recoverability | Interrupted operations can be reconciled |
| OBJ-010 | Release readiness | All mandatory quality gates pass |

# 3. Testing Scope

## 3.1 In scope

The initial desktop release must test:

1. Application initialization.
2. Workspace management.
3. Brand management.
4. AI provider configuration.
5. AI content generation.
6. AI output validation.
7. Multi-provider comparison.
8. Media upload and processing.
9. Multi-platform content composition.
10. Social account authorization.
11. OAuth token management.
12. Content approval.
13. Publishing engine.
14. Publishing attempt history.
15. Idempotency and duplicate prevention.
16. Scheduling and persistent job recovery.
17. Publishing calendar.
18. Dashboard and activity history.
19. Settings and data management.
20. Backup and restore.
21. Security and privacy.
22. API and database integrity.
23. Desktop packaging and installation.

## 3.2 Out of scope for initial MVP

Unless explicitly included in an approved release:

- Multi-tenant SaaS isolation.
- Multi-user collaboration.
- Team approval workflows.
- Subscription billing.
- Enterprise SSO.
- Advanced analytics.
- Large-scale distributed job processing.
- Kubernetes deployment.
- Local LLM inference.
- Production Reddit publishing without required authorization.

These areas may receive architectural or prototype testing, but they are not initial MVP release requirements.

# 4. Testing Levels

| Level | Purpose | Primary responsibility |
|---|---|---|
| Unit testing | Validate isolated functions and business logic | Developers |
| Component testing | Validate frontend components and interactions | Frontend developers |
| Integration testing | Validate communication between modules | Developers / QA |
| API testing | Validate HTTP contracts and backend behavior | Backend developers / QA |
| Contract testing | Validate provider and platform adapter interfaces | Developers |
| Database testing | Validate schema, migrations, transactions, and integrity | Backend developers |
| Security testing | Identify authorization, credential, and input-handling vulnerabilities | Security / QA |
| End-to-end testing | Validate complete user journeys | QA |
| Performance testing | Measure resource usage and responsiveness | QA / Engineering |
| Compatibility testing | Verify supported Windows environments | QA |
| Release testing | Verify packaged application readiness | Release owner |

# 5. Test Environment

## 5.1 Minimum development environment

| Component | Configuration |
|---|---|
| Operating system | Windows 10 / Windows 11 |
| CPU | AMD Ryzen 5 3450U or equivalent |
| RAM | 8 GB baseline |
| Storage | SSD recommended |
| Desktop framework | Tauri 2 |
| Frontend | React + TypeScript |
| Backend | Python + FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Media processing | Pillow + FFmpeg |
| Testing framework | Pytest |
| Frontend testing | Vitest + React Testing Library |
| Browser automation | Playwright where applicable |

## 5.2 Test environments

Maintain separate environments.

### DEV - Development

Purpose:
- Unit tests.
- Component tests.
- Local integration tests.
- Mock provider tests.
- Database migration tests.

Restrictions:
- No real public publishing.
- No production credentials.
- No production user data.

### QA - Quality Assurance

Purpose:
- Complete regression testing.
- Desktop application testing.
- Controlled OAuth integration.
- Controlled social platform publishing.
- Backup and restore validation.

Restrictions:
- Use authorized test accounts.
- Use non-production content.
- Restrict external publishing to approved test destinations.

### STAGING - Release Candidate

Purpose:
- Validate the packaged release.
- Verify production-like configuration.
- Run final security and integration tests.
- Verify upgrade and recovery procedures.

Restrictions:
- No unapproved public posts.
- No embedded credentials.
- No unverified integrations.

### PROD - Production

Purpose:
- Actual user operations.
- Operational monitoring.
- Controlled smoke tests.

Restrictions:
- Never execute destructive test cases.
- Never run duplicate-post tests against public accounts.
- Never use production credentials in automated test fixtures.

# 6. Test Data Strategy

## 6.1 Test workspaces

Prepare the following workspaces:

| Workspace ID | Name | Purpose |
|---|---|---|
| WS-001 | Default Workspace | Normal workflow testing |
| WS-002 | Test Workspace | Workspace isolation |
| WS-003 | Recovery Workspace | Backup and restore testing |

## 6.2 Test brands

Create brands with different configurations:

- Technology education brand.
- Professional business brand.
- Creative content brand.
- Empty brand configuration.
- Invalid or incomplete brand configuration.

## 6.3 Test content

Prepare the following content types:

- Short text post.
- Long-form content.
- Content with hashtags.
- Content with links.
- Content containing Unicode characters.
- Content containing emoji.
- Content with unsupported characters or malformed input.
- Image-based post.
- Video-based post.
- Empty content.
- Content exceeding platform constraints.
- Content with prompt injection text.
- Content containing potentially sensitive information.

## 6.4 Test media

Include:

- Valid JPEG.
- Valid PNG.
- Valid WebP where supported.
- Valid MP4 where supported.
- Unsupported file extension.
- Incorrect MIME type.
- Corrupted image.
- Corrupted video.
- Oversized file.
- File with misleading extension.
- Filename containing special characters.
- Path traversal test filename.

Never use executable malware or destructive payloads in the normal QA environment.

## 6.5 Test AI provider responses

Prepare mocked provider responses for:

1. Successful text generation.
2. Successful structured generation.
3. Authentication failure.
4. Rate-limit response.
5. Timeout.
6. Network failure.
7. Malformed JSON.
8. Empty response.
9. Unsupported model.
10. Unsupported capability.
11. Provider outage.
12. Invalid or incomplete output.
13. Multiple-provider partial success.

## 6.6 Test account configurations

Include:

- Valid connected account.
- Expired access token.
- Revoked authorization.
- Missing publishing permissions.
- Disconnected account.
- Invalid account metadata.
- Account with an unavailable API capability.

Use test credentials and authorized test accounts only.

# 7. Test Case Format

Every test case must include:

| Field | Description |
|---|---|
| Test ID | Unique test identifier |
| Requirement ID | Related acceptance criterion |
| Priority | P0 / P1 / P2 |
| Test type | Unit / Integration / API / E2E / Security |
| Preconditions | Required initial conditions |
| Test data | Inputs and test fixtures |
| Execution steps | Actions to perform |
| Expected result | Verifiable expected behavior |
| Actual result | Recorded execution outcome |
| Status | Not Run / Pass / Fail / Blocked |
| Evidence | Logs, screenshots, reports, or test output |

Test cases must be repeatable and independent wherever practical.

# 8. Unit Test Plan

## 8.1 Application and workspace

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-APP-001 | AC-APP-001 | Initialize application configuration | Valid default configuration created | P0 |
| UT-APP-002 | AC-APP-002 | Validate local API host configuration | Remote binding rejected by default | P0 |
| UT-APP-003 | AC-APP-003 | Create workspace with valid data | Workspace created | P0 |
| UT-APP-004 | AC-APP-003 | Create workspace with empty name | Validation error | P0 |
| UT-APP-005 | AC-APP-003 | Create duplicate workspace identifier | Operation rejected | P0 |
| UT-APP-006 | AC-APP-004 | Switch between workspaces | Correct workspace context loaded | P1 |
| UT-APP-007 | AC-APP-004 | Attempt cross-workspace resource access | Access rejected | P0 |

## 8.2 Brand management

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-BRAND-001 | AC-BRAND-001 | Create valid brand | Brand persisted | P1 |
| UT-BRAND-002 | AC-BRAND-001 | Update brand configuration | Changes persisted | P1 |
| UT-BRAND-003 | AC-BRAND-001 | Delete brand with related content | Referential integrity preserved | P1 |
| UT-BRAND-004 | AC-BRAND-002 | Build AI brand context | Correct brand instructions included | P1 |
| UT-BRAND-005 | AC-BRAND-002 | Switch selected brand | Previous brand context excluded | P0 |

## 8.3 AI provider management

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-AI-001 | AC-AI-001 | Configure supported provider | Provider configuration saved | P0 |
| UT-AI-002 | AC-AI-001 | Select unsupported model | Validation error | P0 |
| UT-AI-003 | AC-AI-002 | Store API credential | Credential sent to secure storage | P0 |
| UT-AI-004 | AC-AI-002 | Serialize application settings | No raw API key present | P0 |
| UT-AI-005 | AC-AI-004 | Check provider capability | Correct capability returned | P0 |
| UT-AI-006 | AC-AI-005 | Simulate provider failure | Error isolated to provider request | P0 |
| UT-AI-007 | AC-AI-007 | Generate through multiple providers | Independent results returned | P1 |
| UT-AI-008 | AC-AI-008 | Attempt unauthorized fallback | Fallback blocked | P0 |
| UT-AI-009 | AC-AI-006 | Build transmission disclosure | Provider and data categories identified | P0 |
| UT-AI-010 | AC-CONTENT-005 | Validate malformed structured response | Invalid response rejected | P0 |

## 8.4 Content management

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-CONTENT-001 | AC-CONTENT-001 | Create content | Draft created | P0 |
| UT-CONTENT-002 | AC-CONTENT-001 | Create content without required fields | Validation error | P0 |
| UT-CONTENT-003 | AC-CONTENT-002 | Process successful generation response | Content associated correctly | P0 |
| UT-CONTENT-004 | AC-CONTENT-003 | Regenerate content | New revision/result created | P1 |
| UT-CONTENT-005 | AC-CONTENT-004 | Edit approved variant | Approval invalidated | P0 |
| UT-CONTENT-006 | AC-CONTENT-004 | Edit published historical content | Historical snapshot preserved | P0 |
| UT-CONTENT-007 | AC-CONTENT-005 | Validate invalid JSON | Validation failure returned | P0 |
| UT-CONTENT-008 | AC-CONTENT-005 | Validate missing required output field | Invalid result rejected | P0 |

## 8.5 Media management

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-MEDIA-001 | AC-MEDIA-001 | Upload valid image | Asset accepted | P0 |
| UT-MEDIA-002 | AC-MEDIA-001 | Upload unsupported file | Rejected | P0 |
| UT-MEDIA-003 | AC-MEDIA-001 | Upload oversized file | Rejected | P0 |
| UT-MEDIA-004 | AC-MEDIA-002 | Generate safe storage path | Path remains inside media directory | P0 |
| UT-MEDIA-005 | AC-MEDIA-003 | Generate preview | Original asset unchanged | P1 |
| UT-MEDIA-006 | AC-MEDIA-004 | Resize image | Valid transformed image created | P1 |
| UT-MEDIA-007 | AC-MEDIA-005 | Validate platform media rules | Unsupported media blocked | P0 |

## 8.6 Composer and approval

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-COMP-001 | AC-COMPOSER-001 | Select supported account | Account accepted | P0 |
| UT-COMP-002 | AC-COMPOSER-002 | Update one platform variant | Other variants unchanged | P0 |
| UT-COMP-003 | AC-COMPOSER-003 | Exceed configured content limit | Validation failure | P0 |
| UT-COMP-004 | AC-COMPOSER-004 | Switch platform preview | Correct variant displayed | P1 |
| UT-APR-001 | AC-APPROVAL-001 | Approve eligible variant | Approval recorded | P0 |
| UT-APR-002 | AC-APPROVAL-002 | Modify approved variant | Approval invalidated | P0 |
| UT-APR-003 | AC-APPROVAL-003 | Reject variant | Publishing prohibited | P0 |
| UT-APR-004 | AC-APPROVAL-004 | Record approval event | Audit entry created | P0 |

## 8.7 Publishing and scheduling logic

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| UT-PUB-001 | AC-PUBLISH-001 | Validate unapproved content | Publishing blocked | P0 |
| UT-PUB-002 | AC-PUBLISH-001 | Validate expired account token | Publishing blocked | P0 |
| UT-PUB-003 | AC-PUBLISH-004 | Generate idempotency identity | Stable identity for same operation | P0 |
| UT-PUB-004 | AC-PUBLISH-004 | Submit duplicate operation | Duplicate logical job prevented | P0 |
| UT-PUB-005 | AC-PUBLISH-006 | Process unknown outcome | Reconciliation required | P0 |
| UT-PUB-006 | AC-PUBLISH-007 | Retry permanent failure | Retry prohibited | P0 |
| UT-PUB-007 | AC-PUBLISH-008 | Process confirmed success | Published record created | P0 |
| UT-SCH-001 | AC-SCHEDULE-001 | Convert local schedule to UTC | Correct instant preserved | P0 |
| UT-SCH-002 | AC-SCHEDULE-001 | Submit invalid schedule | Validation error | P0 |
| UT-SCH-003 | AC-SCHEDULE-003 | Evaluate paused job | Execution prevented | P0 |
| UT-SCH-004 | AC-SCHEDULE-004 | Reschedule eligible job | Updated schedule persisted | P1 |

# 9. Integration Test Plan

## 9.1 Backend and database integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-DB-001 | AC-API-004 | Initialize SQLite database | Schema created correctly | P0 |
| IT-DB-002 | AC-API-004 | Execute Alembic migration | Migration succeeds | P0 |
| IT-DB-003 | AC-API-004 | Upgrade previous schema | Existing records preserved | P0 |
| IT-DB-004 | AC-API-004 | Insert invalid foreign-key reference | Transaction rejected | P0 |
| IT-DB-005 | AC-API-004 | Simulate transaction failure | No partial critical commit | P0 |
| IT-DB-006 | AC-API-004 | Run concurrent updates | Conflict detected or serialized safely | P0 |
| IT-DB-007 | AC-API-004 | Delete referenced records | Documented deletion policy enforced | P0 |

## 9.2 AI provider integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-AI-001 | AC-AI-001 | Send valid request to provider adapter | Valid response received | P0 |
| IT-AI-002 | AC-AI-002 | Retrieve credential through backend | Credential not exposed to frontend | P0 |
| IT-AI-003 | AC-AI-003 | Test invalid credential | Authentication failure reported | P1 |
| IT-AI-004 | AC-AI-004 | Call unsupported capability | Explicit unsupported response | P0 |
| IT-AI-005 | AC-AI-005 | Simulate provider outage | Other providers remain usable | P0 |
| IT-AI-006 | AC-AI-007 | Compare two provider results | Results remain independent | P1 |
| IT-AI-007 | AC-AI-008 | Trigger fallback without consent | No secondary request sent | P0 |
| IT-AI-008 | AC-AI-006 | Inspect outgoing request | Only disclosed data transmitted | P0 |

Use mocked HTTP responses for deterministic tests. Run authorized live-provider smoke tests separately.

## 9.3 Media integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-MEDIA-001 | AC-MEDIA-001 | Upload file through API | Valid media record created | P0 |
| IT-MEDIA-002 | AC-MEDIA-002 | Persist uploaded asset | Database and filesystem agree | P0 |
| IT-MEDIA-003 | AC-MEDIA-003 | Retrieve preview | Valid preview returned | P1 |
| IT-MEDIA-004 | AC-MEDIA-004 | Transform uploaded image | Original preserved | P1 |
| IT-MEDIA-005 | AC-MEDIA-002 | Simulate interrupted upload | Incomplete asset handled safely | P0 |

## 9.4 OAuth integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-OAUTH-001 | AC-ACCOUNT-001 | Start OAuth flow | Valid authorization URL created | P0 |
| IT-OAUTH-002 | AC-ACCOUNT-001 | Receive valid callback | Callback validated | P0 |
| IT-OAUTH-003 | AC-ACCOUNT-001 | Receive mismatched state | Callback rejected | P0 |
| IT-OAUTH-004 | AC-ACCOUNT-003 | Refresh expired token | Supported refresh succeeds | P0 |
| IT-OAUTH-005 | AC-ACCOUNT-003 | Refresh revoked token | Reauthorization required | P0 |
| IT-OAUTH-006 | AC-ACCOUNT-004 | Disconnect account | Credentials removed or revoked as supported | P1 |
| IT-OAUTH-007 | AC-ACCOUNT-005 | Missing permission | Integration marked unavailable for affected operation | P0 |

## 9.5 Publishing integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-PUB-001 | AC-PUBLISH-001 | Validate all publishing prerequisites | Eligible job accepted | P0 |
| IT-PUB-002 | AC-PUBLISH-002 | Submit approved content | Publishing job created | P0 |
| IT-PUB-003 | AC-PUBLISH-003 | Create jobs for three destinations | Three independent jobs | P0 |
| IT-PUB-004 | AC-PUBLISH-005 | Record failed attempt | Attempt history preserved | P0 |
| IT-PUB-005 | AC-PUBLISH-006 | Simulate timeout after request submission | Job enters reconciliation | P0 |
| IT-PUB-006 | AC-PUBLISH-007 | Retry eligible failed job | New attempt recorded | P0 |
| IT-PUB-007 | AC-PUBLISH-008 | Process platform success response | Published identity stored | P0 |
| IT-PUB-008 | AC-PUBLISH-004 | Submit concurrent duplicate requests | One logical operation | P0 |

## 9.6 Scheduler integration

| Test ID | Requirement | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| IT-SCH-001 | AC-SCHEDULE-002 | Persist scheduled job | Job stored in SQLite | P0 |
| IT-SCH-002 | AC-SCHEDULE-002 | Restart scheduler | Existing jobs recovered | P0 |
| IT-SCH-003 | AC-SCHEDULE-003 | Execute due approved job | Eligible job dispatched | P0 |
| IT-SCH-004 | AC-SCHEDULE-003 | Process paused job | No publishing operation | P0 |
| IT-SCH-005 | AC-SCHEDULE-004 | Update schedule | Existing job updated safely | P1 |
| IT-SCH-006 | AC-SCHEDULE-005 | Resume paused scheduler | Eligible jobs restored without duplication | P1 |

# 10. API Test Plan

All API tests must validate HTTP status, response schema, authorization, database side effects, and error behavior.

## 10.1 Application and workspace APIs

| Test ID | Endpoint | Test | Expected result |
|---|---|---|---|
| API-001 | `/health` | Backend health check | Healthy status returned |
| API-002 | `/system/status` | Application status | Valid operational status |
| API-003 | Workspace creation route | Valid workspace request | Created |
| API-004 | Workspace creation route | Invalid request | Validation error |
| API-005 | Workspace list route | List workspaces | Correct records returned |

## 10.2 AI APIs

| Test ID | Endpoint | Test | Expected result |
|---|---|---|---|
| API-010 | Provider configuration route | Create provider configuration | Configuration saved without plaintext credential |
| API-011 | Provider test route | Test valid provider | Connectivity result returned |
| API-012 | Content generation route | Generate valid content | Structured response returned |
| API-013 | Content generation route | Invalid provider | Clear validation error |
| API-014 | Content generation route | Provider timeout | Controlled timeout response |
| API-015 | Variant regeneration route | Regenerate variant | New revision/result |
| API-016 | Variant revision route | Revise content | Updated revision |

## 10.3 Media APIs

| Test ID | Endpoint | Test | Expected result |
|---|---|---|---|
| API-020 | Media upload route | Upload supported file | Asset created |
| API-021 | Media upload route | Upload unsupported file | Rejected |
| API-022 | Media list route | List media | Paginated response |
| API-023 | Media preview route | Retrieve preview | Valid preview |
| API-024 | Media delete route | Delete asset | Documented deletion behavior |

## 10.4 Account and publishing APIs

| Test ID | Endpoint | Test | Expected result |
|---|---|---|---|
| API-030 | OAuth connect route | Initiate OAuth | Authorization URL returned |
| API-031 | OAuth callback route | Valid callback | Account connected |
| API-032 | Account list route | List connected accounts | Correct identities returned |
| API-033 | Account disconnect route | Disconnect account | Credentials handled securely |
| API-034 | Publishing validation route | Validate variant | Validation result returned |
| API-035 | Publishing route | Submit valid job | Job created |
| API-036 | Publishing history route | List attempts | History returned |
| API-037 | Publishing retry route | Retry eligible failure | Retry accepted |
| API-038 | Publishing cancel route | Cancel eligible job | Job cancelled |
| API-039 | Schedule route | Create scheduled job | Job persisted |
| API-040 | Calendar route | Retrieve calendar entries | Correct entries returned |

The final endpoint paths must match the approved API specification. The endpoint labels above are logical test targets, not permission to invent route implementations.

## 10.5 API negative testing

Test:

- Missing authentication.
- Invalid local API secret.
- Malformed JSON.
- Missing required fields.
- Invalid UUID.
- Invalid date/time.
- Unsupported content type.
- Oversized request.
- Unauthorized workspace reference.
- Duplicate idempotency key.
- Invalid pagination values.
- Invalid sorting parameters.
- Unexpected internal exception.

Expected outcome: controlled error response, no unintended side effect, and no sensitive data disclosure.

# 11. Frontend Component Testing

Use Vitest and React Testing Library.

| Test ID | Component | Scenario | Expected result |
|---|---|---|---|
| FE-001 | Workspace selector | Switch workspace | Correct workspace displayed |
| FE-002 | Brand form | Submit valid form | Brand saved |
| FE-003 | Provider configuration | Configure provider | Secure configuration workflow |
| FE-004 | AI generation panel | Submit generation request | Loading and result states displayed |
| FE-005 | AI result editor | Edit generated content | Updated revision reflected |
| FE-006 | Media uploader | Upload valid media | Asset displayed |
| FE-007 | Platform selector | Change platform | Correct variant loaded |
| FE-008 | Approval controls | Approve variant | Correct approval state displayed |
| FE-009 | Publishing controls | Publish approved variant | Correct job state displayed |
| FE-010 | Calendar | Load scheduled entries | Correct entries displayed |
| FE-011 | Dashboard | Load actual records | Accurate counts displayed |
| FE-012 | Error component | Simulate API failure | Useful error displayed |
| FE-013 | Confirmation dialog | Cancel destructive action | Operation not executed |
| FE-014 | Settings | Change setting | Persisted value displayed |

Frontend tests must not be used as a substitute for backend authorization or data-integrity tests.

# 12. End-to-End Test Plan

## 12.1 E2E publishing workflow

### E2E-001 - Create and publish content

Priority: P0

**Preconditions:**
- Application installed.
- Workspace configured.
- AI provider connected.
- Social test account connected.
- Publishing permissions available.

**Execution:**
1. Launch PostFlow.
2. Open the workspace.
3. Select a brand.
4. Create a content item.
5. Generate content using an AI provider.
6. Review and edit the result.
7. Create a platform-specific variant.
8. Validate content.
9. Approve the variant.
10. Publish the content.
11. Inspect the publishing history.

**Expected result:**
- Content is persisted.
- Provider and model metadata are stored.
- Platform variant is independently stored.
- Approval references the correct revision.
- One destination-specific publishing job is created.
- Successful publication is confirmed.
- Platform post identifier is stored when returned.

## 12.2 Multi-platform publishing

### E2E-002 - Partial success

Priority: P0

**Preconditions:**
- Three authorized destination accounts.
- Valid content variants.

**Execution:**
1. Select all three destinations.
2. Validate all variants.
3. Approve each required variant.
4. Initiate multi-platform publishing.
5. Simulate two successes and one failure.

**Expected result:**
- Two destinations show confirmed success.
- One destination shows failure.
- Successful jobs are not repeated.
- Failed job retains its attempt history.
- Overall result is shown as partial success.

## 12.3 Duplicate publishing

### E2E-003 - Duplicate submission protection

Priority: P0

**Execution:**
1. Submit a publishing request.
2. Submit the same request again.
3. Trigger concurrent submissions.
4. Inspect job and attempt records.

**Expected result:**
- Duplicate logical operations are prevented.
- Only the intended operation is executed.
- Duplicate requests do not produce duplicate posts.

Use mocked platform adapters or an isolated test environment. Do not repeatedly publish duplicate content to public production accounts.

## 12.4 Unknown publishing outcome

### E2E-004 - Timeout after platform acceptance

Priority: P0

**Execution:**
1. Submit a publishing request.
2. Simulate platform acceptance.
3. Drop the response before the client receives confirmation.
4. Restart the application.
5. Inspect the job state.
6. Trigger reconciliation.

**Expected result:**
- Job is marked as uncertain.
- Blind retry is prohibited.
- Reconciliation is attempted through supported platform capabilities.
- Confirmed publication is recorded without duplication.
- Unresolvable status is presented for manual intervention.

## 12.5 Restart recovery

### E2E-005 - Application restart during scheduling

Priority: P0

**Execution:**
1. Create multiple scheduled jobs.
2. Close the application before the execution time.
3. Restart the application.
4. Inspect recovered jobs.
5. Allow due jobs to execute under the configured policy.

**Expected result:**
- Jobs remain persisted.
- Eligible jobs execute once.
- Completed jobs do not execute again.
- Uncertain jobs require reconciliation.
- Failed jobs retain their attempt history.

## 12.6 AI provider failure

### E2E-006 - Provider outage

Priority: P0

**Execution:**
1. Configure two providers.
2. Initiate generation through both.
3. Simulate one provider outage.
4. Allow the second provider to respond.

**Expected result:**
- Successful output remains available.
- Failed provider reports its error.
- Existing content is preserved.
- No unapproved fallback request is made.

## 12.7 Approval invalidation

### E2E-007 - Edit after approval

Priority: P0

**Execution:**
1. Create a platform variant.
2. Approve the variant.
3. Edit its content.
4. Attempt publishing.

**Expected result:**
- Old approval is invalidated.
- Publishing is blocked.
- Updated content requires approval.

## 12.8 Backup and restore

### E2E-008 - Full application recovery

Priority: P0

**Execution:**
1. Create brands, content, variants, media, and publishing history.
2. Create backup.
3. Validate backup integrity.
4. Restore to an isolated test installation.
5. Inspect restored records and media.

**Expected result:**
- Supported records are restored.
- Media references resolve.
- Publishing history remains consistent.
- Credentials follow the documented secure restoration policy.
- The original installation remains unaffected.

# 13. Security Test Plan

Security testing must include positive and negative authorization cases.

| Test ID | Security area | Test scenario | Expected result | Priority |
|---|---|---|---|---|
| SEC-001 | Local API | Send request without secret | Rejected | P0 |
| SEC-002 | Local API | Send invalid secret | Rejected | P0 |
| SEC-003 | Network exposure | Attempt remote access | No unintended remote access | P0 |
| SEC-004 | Credential storage | Inspect SQLite and settings | No plaintext credentials | P0 |
| SEC-005 | Logging | Trigger authentication error | Secrets redacted | P0 |
| SEC-006 | OAuth | Mismatched state | Callback rejected | P0 |
| SEC-007 | OAuth | Replay callback | Replay rejected or safely handled | P0 |
| SEC-008 | File upload | Misleading file extension | Content validation rejects unsafe file | P0 |
| SEC-009 | File upload | Path traversal attempt | Outside-directory access prevented | P0 |
| SEC-010 | AI | Prompt injection attempts unauthorized action | Action blocked | P0 |
| SEC-011 | Approval | Publish without approval | Rejected | P0 |
| SEC-012 | Revision | Publish stale approval | Rejected | P0 |
| SEC-013 | Workspace | Access another workspace's record | Rejected | P0 |
| SEC-014 | Error handling | Trigger internal exception | No sensitive stack trace returned | P0 |
| SEC-015 | Dependencies | Run dependency vulnerability scan | Findings documented and reviewed | P0 |
| SEC-016 | Tauri | Attempt unauthorized frontend capability | Access denied | P0 |

## 13.1 Security test rules

- Use synthetic credentials.
- Do not expose real OAuth tokens in test output.
- Do not use production user data.
- Do not perform destructive tests against production accounts.
- Record findings with severity and reproduction steps.
- Retest every resolved security defect.

## 13.2 Security severity

| Severity | Definition | Release action |
|---|---|---|
| Critical | Direct compromise, unauthorized publishing, credential theft, or severe data exposure | Release blocked |
| High | Serious exploitable security or data-integrity weakness | Release blocked |
| Medium | Limited impact requiring remediation | Review and document |
| Low | Minor security weakness | Track for remediation |
| Informational | Hardening recommendation | Document |

# 14. Performance Test Plan

Performance testing must use realistic workloads and the baseline hardware configuration.

## 14.1 Performance scenarios

| Test ID | Scenario | Measurement | Initial target |
|---|---|---|---|
| PERF-001 | Cold application startup | Time to usable interface | Under 10 seconds |
| PERF-002 | Dashboard load | Time after backend readiness | Under 3 seconds |
| PERF-003 | Lightweight API operation | p95 response time | Under 500 ms |
| PERF-004 | Workspace switching | UI response | No blocking |
| PERF-005 | Large content listing | Query and rendering time | No unnecessary full-table scans |
| PERF-006 | Media upload | Progress and memory usage | Stable operation |
| PERF-007 | Media transformation | CPU and memory usage | No UI freeze |
| PERF-008 | AI generation | Request and response handling | Non-blocking UI |
| PERF-009 | Scheduler idle operation | CPU and memory usage | No excessive polling |
| PERF-010 | Application memory | Idle and representative workload | Measure and optimize for 8 GB RAM |

## 14.2 Performance test rules

- Record hardware configuration.
- Record application build identifier.
- Record dataset size.
- Repeat benchmarks to identify inconsistent results.
- Measure cold and warm startup separately.
- Avoid presenting network-dependent AI latency as local application performance.
- Identify CPU-heavy media operations.
- Track memory growth during repeated operations.

## 14.3 Resource constraints

The initial product must:

- Avoid requiring local LLM inference.
- Avoid unnecessary background services.
- Avoid heavyweight local infrastructure.
- Use one or two background workers by default.
- Keep database operations lightweight.
- Execute media and AI work asynchronously.

# 15. Database and Migration Testing

## 15.1 Migration tests

| Test ID | Scenario | Expected result |
|---|---|---|
| DB-001 | Fresh database initialization | All expected tables created |
| DB-002 | Upgrade from previous schema | Migration succeeds |
| DB-003 | Upgrade with populated records | Existing data preserved |
| DB-004 | Invalid migration state | Migration fails safely |
| DB-005 | Foreign-key enforcement | Invalid relationships rejected |
| DB-006 | Transaction rollback | No partial critical changes |
| DB-007 | Backup database | Valid backup created |
| DB-008 | Restore backup | Database integrity verified |

## 15.2 Data integrity invariants

The following must always hold:

1. Every platform variant references a valid content item.
2. Every publishing job references a valid destination account and variant.
3. Every publishing attempt references a valid job.
4. Approval references the exact approved revision.
5. Published records retain the relevant historical content snapshot.
6. Workspace-owned records remain correctly scoped.
7. Deleted or disconnected accounts cannot authorize new publishing.
8. Duplicate logical operations cannot create duplicate posts.
9. UTC timestamps are stored consistently.
10. Media references must resolve or be explicitly marked unavailable.

## 15.3 Database integrity verification

After critical workflows, run appropriate integrity checks, including:

- SQLite `PRAGMA integrity_check`.
- SQLite `PRAGMA foreign_key_check`.
- Record-count reconciliation.
- Media file existence checks.
- Job and attempt relationship checks.
- Migration version checks.

# 16. Platform Integration Testing

Every social platform must have two distinct test stages.

## 16.1 Stage A - Adapter tests

Purpose:
- Validate request construction.
- Validate authentication handling.
- Validate response parsing.
- Validate rate-limit handling.
- Validate errors.
- Validate retries and reconciliation decisions.

Use mocked HTTP responses and deterministic fixtures.

## 16.2 Stage B - Real API tests

Purpose:
- Verify actual OAuth authorization.
- Verify actual permissions.
- Verify actual media requirements.
- Verify actual publication.
- Verify actual platform response.
- Verify stored post identifiers and links.

Use approved test accounts and controlled publishing destinations.

## 16.3 Platform test matrix

| Platform | OAuth test | Publish test | Media test | Error test | Production gate |
|---|---|---|---|---|---|
| Instagram | Required | Required | Required | Required | Meta permissions and API review |
| Facebook Pages | Required | Required | Required | Required | Page permissions |
| LinkedIn | Required | Required | Required where applicable | Required | Member/organization permissions |
| Threads | Required | Required | Required where applicable | Required | Official API authorization |
| Pinterest | Required | Required | Required | Required | Board and Pin permissions |
| X | Required | Required | Required where applicable | Required | Current API access and pricing |
| Reddit | Required if enabled | Required if enabled | Applicable | Required | Developer and commercial-use approval |

An integration must remain disabled or explicitly labeled unavailable until its production gates are met.

# 17. Regression Testing

Regression testing must be executed after changes to:

- Database models.
- API contracts.
- Authentication.
- OAuth handling.
- Credential storage.
- Provider adapters.
- Platform adapters.
- Content revision logic.
- Approval workflow.
- Publishing state machine.
- Idempotency logic.
- Scheduler.
- Media processing.
- Backup and restore.
- Tauri capabilities.
- Application packaging.

## 17.1 Mandatory regression suite

The following tests must run before every release candidate:

- [ ] Application startup.
- [ ] Workspace creation and switching.
- [ ] AI provider configuration.
- [ ] AI generation.
- [ ] AI failure isolation.
- [ ] Content revision.
- [ ] Media upload and validation.
- [ ] Independent platform variants.
- [ ] OAuth authorization.
- [ ] Credential protection.
- [ ] Approval invalidation.
- [ ] Publishing validation.
- [ ] Duplicate publishing prevention.
- [ ] Unknown outcome reconciliation.
- [ ] Multi-platform partial failure.
- [ ] Scheduler persistence.
- [ ] Restart recovery.
- [ ] Backup and restore.
- [ ] Database integrity.
- [ ] Local API authorization.
- [ ] Security regression tests.

# 18. Test Automation Strategy

## 18.1 Backend automation

Recommended tools:

| Tool | Purpose |
|---|---|
| Pytest | Python unit and integration tests |
| HTTPX | FastAPI endpoint testing |
| pytest-asyncio | Async test execution |
| pytest-cov | Coverage reporting |
| SQLAlchemy test fixtures | Database integration testing |
| Alembic | Migration verification |
| Hypothesis | Property-based testing for critical logic |

Recommended backend structure:

```text
tests/
├── backend/
│   ├── unit/
│   │   ├── test_workspace.py
│   │   ├── test_brand.py
│   │   ├── test_ai_provider.py
│   │   ├── test_content.py
│   │   ├── test_variants.py
│   │   ├── test_approval.py
│   │   ├── test_publishing.py
│   │   ├── test_idempotency.py
│   │   ├── test_scheduler.py
│   │   └── test_security.py
│   ├── integration/
│   │   ├── test_database.py
│   │   ├── test_ai_adapters.py
│   │   ├── test_oauth.py
│   │   ├── test_media.py
│   │   ├── test_publishing.py
│   │   └── test_recovery.py
│   ├── api/
│   │   ├── test_workspaces_api.py
│   │   ├── test_content_api.py
│   │   ├── test_media_api.py
│   │   ├── test_accounts_api.py
│   │   ├── test_publish_api.py
│   │   └── test_schedule_api.py
│   └── conftest.py
```

## 18.2 Frontend automation

Recommended tools:

- Vitest.
- React Testing Library.
- Playwright for supported desktop workflow automation.

Suggested structure:

```text
tests/
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   └── fixtures/
└── e2e/
    ├── application.spec.ts
    ├── workspace.spec.ts
    ├── content.spec.ts
    ├── composer.spec.ts
    ├── approval.spec.ts
    ├── publishing.spec.ts
    ├── calendar.spec.ts
    └── recovery.spec.ts
```

For Tauri-specific native behavior, test the packaged desktop application using an appropriate supported desktop automation setup. Browser-based Playwright tests alone do not validate all native desktop capabilities.

## 18.3 CI automation

Recommended pipeline:

```text
Commit / Pull Request
        |
        v
Static Analysis
        |
        v
Dependency and Secret Scanning
        |
        v
Frontend Unit Tests
        |
        v
Backend Unit Tests
        |
        v
Database Migration Tests
        |
        v
API and Integration Tests
        |
        v
Contract Tests
        |
        v
Security Regression Tests
        |
        v
Build Desktop Application
        |
        v
Packaging and Smoke Tests
        |
        v
Release Candidate
```

### CI release rules

- Critical tests must not be skipped silently.
- Failed mandatory tests must block release.
- Test reports must be retained.
- Secrets must be injected through secure CI configuration.
- Real platform publishing tests must run in a separately authorized controlled environment.
- External API outages must be reported as blocked or inconclusive, not passed.

# 19. Test Execution and Reporting

## 19.1 Test execution statuses

| Status | Meaning |
|---|---|
| NOT RUN | Test has not been executed |
| PASS | Actual result matches expected result |
| FAIL | Actual result differs from expected result |
| BLOCKED | External dependency prevents execution |
| SKIPPED | Explicitly excluded with documented justification |
| RETEST | Failed test has been fixed and requires verification |

## 19.2 Defect classification

| Severity | Description | Release impact |
|---|---|---|
| Critical | Data loss, credential exposure, unauthorized publishing, duplicate publishing | Block |
| High | Core publishing, authorization, recovery, or integrity failure | Block |
| Medium | Important feature malfunction with limited impact | Review |
| Low | Minor UI or usability defect | Track |
| Cosmetic | Visual inconsistency without functional impact | Track |

## 19.3 Defect report template

```text
Defect ID:
Title:
Related Test ID:
Related Acceptance Criterion:
Build Version:
Environment:
Severity:
Priority:

Preconditions:

Steps to Reproduce:

Expected Result:

Actual Result:

Reproducibility:
Frequency:

Logs / Screenshots:
Correlation ID:

Root Cause:
Proposed Fix:

Retest Result:
Resolution Status:
```

## 19.4 Test summary report

Each test execution must record:

```text
Test Execution ID:
Application Version:
Build Identifier:
Operating System:
Hardware Configuration:
Database Version:
Test Environment:
Execution Date:
Executed By:

Total Tests:
Passed:
Failed:
Blocked:
Skipped:

Critical Defects:
High Defects:
Medium Defects:
Low Defects:

Security Findings:
Performance Findings:
Platform Integration Status:

Release Recommendation:
Approver:
```

# 20. Release Quality Gates

A release candidate must satisfy all mandatory conditions.

| Gate ID | Requirement | Mandatory |
|---|---|---|
| RG-001 | All P0 unit tests pass | Yes |
| RG-002 | All P0 integration tests pass | Yes |
| RG-003 | All mandatory API contract tests pass | Yes |
| RG-004 | Database migrations and integrity checks pass | Yes |
| RG-005 | No unresolved critical security findings | Yes |
| RG-006 | No unresolved high-severity security findings | Yes |
| RG-007 | No credential exposure | Yes |
| RG-008 | Idempotency and duplicate prevention verified | Yes |
| RG-009 | Unknown outcome reconciliation verified | Yes |
| RG-010 | Restart recovery verified | Yes |
| RG-011 | Backup and restore verified | Yes |
| RG-012 | Enabled platform integrations pass real API tests | Yes |
| RG-013 | Critical E2E workflows pass | Yes |
| RG-014 | Packaged application smoke tests pass | Yes |
| RG-015 | Installation and upgrade procedures verified | Yes |
| RG-016 | Required documentation updated | Yes |

A release must not be approved based solely on an aggregate test pass percentage. A single failed P0 security or publishing-integrity test is sufficient to block release.

# 21. MVP Test Completion Checklist

## Application foundation

- [ ] Windows installation verified.
- [ ] Application startup verified.
- [ ] Local backend binding verified.
- [ ] Local API authorization verified.
- [ ] Workspace persistence verified.
- [ ] Restart recovery verified.

## AI integration

- [ ] Provider configuration verified.
- [ ] Secure credential storage verified.
- [ ] Provider capability validation verified.
- [ ] AI generation verified.
- [ ] AI structured-output validation verified.
- [ ] Provider failure isolation verified.
- [ ] Data transmission disclosure verified.

## Content and media

- [ ] Content creation verified.
- [ ] Content revision verified.
- [ ] Platform variants verified.
- [ ] Media upload verified.
- [ ] File validation verified.
- [ ] Media processing verified.
- [ ] Platform constraints verified.

## Account and publishing

- [ ] OAuth authorization verified.
- [ ] Token refresh and revocation verified.
- [ ] Required permissions verified.
- [ ] Approval workflow verified.
- [ ] Approval invalidation verified.
- [ ] Publishing validation verified.
- [ ] Publishing idempotency verified.
- [ ] Unknown outcome handling verified.
- [ ] Publishing history verified.
- [ ] Multi-platform partial failure verified.

## Scheduling and recovery

- [ ] Schedule persistence verified.
- [ ] Time-zone handling verified.
- [ ] Application restart recovery verified.
- [ ] Duplicate job prevention verified.
- [ ] Backup verified.
- [ ] Restore verified.

## Release readiness

- [ ] Security regression suite passed.
- [ ] Database integrity passed.
- [ ] Performance baseline recorded.
- [ ] Desktop packaging verified.
- [ ] Installation verified.
- [ ] Upgrade verified.
- [ ] All mandatory quality gates passed.

# 22. Definition of Test Completion

Testing for a feature or release is complete only when:

1. All applicable test cases have been executed.
2. Expected and actual results have been recorded.
3. Failed tests have associated defects.
4. Fixed defects have been retested.
5. Regression tests have passed.
6. Mandatory security tests have passed.
7. Required platform integrations have been verified.
8. Evidence is available for critical workflows.
9. Known limitations are documented.
10. The release recommendation is approved.

# 23. Final QA Acceptance Statement

PostFlow must be evaluated as a persistent, security-sensitive publishing system-not merely a content editor with AI functionality.

The most important testing priorities are:

1. Prevent unauthorized publishing.
2. Prevent duplicate posts.
3. Preserve content and revision history.
4. Protect AI and social account credentials.
5. Recover scheduled and interrupted jobs safely.
6. Isolate provider and platform failures.
7. Verify actual platform integration behavior.
8. Preserve user data through backup and restore.

**Release principle:** No P0 failure in authorization, security, publishing integrity, database integrity, or recovery is acceptable in a production release.

---

**Document owner:** Product / Engineering  
**QA owner:** Quality Assurance  
**Review frequency:** Every major release and whenever a critical workflow or integration changes  
**Approval status:** Pending implementation and test evidence


---

# 24. Roadmap-aligned milestone verification

This section supplements the existing baseline test plan; it does not replace existing cases or acceptance-criteria references. Milestone sequencing is in ROADMAP.md and the detailed implementation backlog is in TASK_BREAKDOWN.md.

| Milestone | Required verification | Exit evidence | Release impact |
|---|---|---|---|
| M0 Scope/architecture | Requirements consistency, platform feasibility, OS decision, risk review | Approved scope, decision log, platform evidence | Blocks implementation commitment |
| M1 Desktop/persistence | Startup, loopback API, auth, migrations, workspace persistence, backup/restore | CI, migration, security and restore reports | P0 |
| M2 Content/UI | CRUD, independent variants, revision conflicts, approval invalidation, accessibility | API/component/E2E reports | P0 |
| M3 AI/media | Adapter contracts, secret redaction, disclosure, failure isolation, malicious media | Mock/live reports, secret scan, media fixtures | P0 for selected scope |
| M4 OAuth/platform | State/PKCE, token lifecycle, scopes, account eligibility, real API capability | Sanitized OAuth and platform evidence | P0 for enabled platform |
| M5 Publishing | Preflight, approval recheck, idempotency, immutable attempts, reconciliation | Fault injection and controlled publish evidence | P0 |
| M6 Scheduler | Restart recovery, leases, concurrency, timezone/DST, missed-run behavior | Restart/concurrency/DST report | P0 |
| M7 Release | Regression, security, backup, privacy, performance, installer, upgrade | Signed QA/release checklist | P0 |
| M8 Expansion | New platform/provider contract and integration suite | Per-integration readiness record | Per feature |
| M9 SaaS | Tenant isolation, identity, cloud security, privacy and operations | Separate SaaS threat model and release evidence | SaaS blocker |

## 24.1 Milestone completion rules

- UI presence or mocked success responses do not complete a milestone.
- External tests blocked by app review/access must be marked BLOCKED, not PASS, with owner and next action.
- A platform remains disabled for production publishing until live tests and permissions are verified.
- A security control is complete only when negative tests prove prohibited actions are rejected.
- A migration passes only after clean install and populated upgrade tests.
- A scheduler passes only after restart, concurrent claim, timezone and uncertain-outcome tests.

# 25. Additional critical test cases

These additive cases strengthen coverage for SECURITY.md and THREAT_MODEL.md.

### 25.1 Desktop runtime and local API

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| REL-API-001 | Configure API bind to non-loopback | Unsafe bind rejected | P0 |
| REL-API-002 | Request from untrusted Origin | Rejected unless exact trusted desktop origin | P0 |
| REL-API-003 | Rotate installation secret | Old rejected; new works | P0 |
| REL-API-004 | Backend startup failure | UI shows unavailable state; mutations disabled | P0 |
| REL-API-005 | Flood local API within configured limits | Requests bounded; process remains responsive | P1 |

### 25.2 Credential storage and privacy

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| PRIV-001 | Store synthetic AI key; inspect DB/config/logs/API | No raw key found | P0 |
| PRIV-002 | Store synthetic OAuth token; inspect DB/diagnostics | No raw token found | P0 |
| PRIV-003 | OS credential store unavailable | Fail closed; no plaintext fallback | P0 |
| PRIV-004 | Export backup | No plaintext credentials included | P0 |
| PRIV-005 | Build support bundle | No prompts/content/media/secrets by default | P0 |
| PRIV-006 | Generate without required provider disclosure | Request blocked | P0 |
| PRIV-007 | Provider error contains synthetic secret | Error and audit log redact it | P0 |
| PRIV-008 | Disconnect social account | Local secret removed; remote revoke attempted where supported | P0 |

### 25.3 OAuth and platform readiness

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| OAUTH-008 | Replay OAuth state after success | Rejected | P0 |
| OAUTH-009 | Wrong platform or redirect callback | Rejected | P0 |
| OAUTH-010 | Callback after state expiry | Rejected; user can restart | P0 |
| OAUTH-011 | Concurrent refresh with token rotation | Only valid current token remains | P0 |
| OAUTH-012 | Account lacks publish scope | Capability unavailable; preflight blocks | P0 |
| PLATFORM-001 | Adapter claims unsupported operation | Capability registry rejects/marks unavailable | P0 |
| PLATFORM-002 | Platform returns 429 with Retry-After | Retry honors server delay | P0 |
| PLATFORM-003 | API version/permission changes | Integration degrades or disables; no false success | P1 |

### 25.4 Approval, idempotency and reconciliation

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| PUB-009 | Edit caption after approval | Approval invalidated; publish blocked | P0 |
| PUB-010 | Change media association after approval | Reapproval required | P0 |
| PUB-011 | Change destination after approval | Reapproval required | P0 |
| PUB-012 | Same idempotency key and same fingerprint twice | One logical job | P0 |
| PUB-013 | Same key with different payload | Conflict; no second job | P0 |
| PUB-014 | Platform accepts post but response is lost | Reconciliation; no blind retry | P0 |
| PUB-015 | Worker crashes after external success before local commit | Reconcile before retry | P0 |
| PUB-016 | One destination succeeds, another fails | Success preserved; failure isolated | P0 |
| PUB-017 | Cancel after external submission begins | Cannot promise remote cancellation | P0 |

### 25.5 Media, URL and AI output

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| MEDIA-008 | Misleading extension/magic-byte mismatch | Rejected or safely normalized | P0 |
| MEDIA-009 | Extreme dimensions/decompression bomb | Rejected within resource limits | P0 |
| MEDIA-010 | Traversal/Unicode filename | Generated path remains inside media root | P0 |
| MEDIA-011 | FFmpeg exceeds time/resource limit | Process terminated; partial asset not valid | P1 |
| AI-009 | Model returns script/HTML | Escaped text; never executed | P0 |
| AI-010 | Prompt injection asks for credentials/tool action | No credential/tool access; action blocked | P0 |
| AI-011 | Provider timeout | Content preserved; no silent fallback | P0 |
| SSRF-001 | URL import targets private/loopback address | Blocked; if feature absent, endpoint remains absent | P0 if implemented |

### 25.6 Scheduler and recovery

| Test ID | Scenario | Expected result | Priority |
|---|---|---|---|
| SCH-005 | Two workers claim same due job | Exactly one active claim | P0 |
| SCH-006 | App exits after claim before submission | Lease recovery returns safe state | P0 |
| SCH-007 | App exits after external submission before persistence | Reconcile; no blind retry | P0 |
| SCH-008 | Schedule crosses DST boundary | Defined timezone policy applied deterministically | P0 |
| SCH-009 | Device asleep at scheduled time | Missed-run policy applied and surfaced | P0 |
| SCH-010 | User pauses all publishing | No new submission after pause acknowledgement | P0 |

### 25.7 SaaS-only tests

Not desktop MVP gates; mandatory before SaaS launch:
- Client cannot override authenticated tenant context.
- Every resource route enforces object-level tenant authorization.
- Jobs and media enforce tenant boundaries.
- Role escalation and invitation abuse are tested.
- Session invalidation and MFA recovery are tested.
- Backup restore cannot cross tenant boundaries.
- Deletion, legal holds and retention are verified per tenant.
- Cloud secrets, service identities, egress and operational access are reviewed.

# 26. Quality gates and go/no-go rules

1. **P0:** All applicable P0 tests pass. No waiver for credential exposure, unauthorized publishing, stale approval, duplicate publishing, cross-workspace access, unrecoverable corruption or failed backup restore.
2. **Security:** No unresolved Critical or High exploitable finding. Accepted Medium risks require owner, rationale, mitigation, review date and approval.
3. **Publishing:** Fault injection covers lost response, process crash, concurrent duplicate request and partial destination success.
4. **Integrations:** Only integrations with verified official API access, scopes, account eligibility and live test evidence may be enabled.
5. **Data:** Clean migration, populated upgrade, integrity checks, backup and isolated restore pass.
6. **Privacy:** Shipped data flows, retention and deletion match the user-facing notice.
7. **Performance:** Record measurements on baseline supported hardware; do not report targets as achieved without measurements.
8. **Packaging:** Clean install, upgrade, signature verification, launch, shutdown and uninstall pass.
9. **Evidence:** Each gate has build ID, environment, report, owner and approval. Blocked external tests remain blocked.
10. **Decision:** Release owner records GO/NO-GO and accepted non-blocking limitations.

## 26.1 Required release evidence bundle

- CI run and commit/build identifiers.
- Unit, component, API, integration and E2E reports.
- Alembic migration and SQLite integrity output.
- Security/dependency scan reports.
- Secret-canary scan of database, logs, exports and package.
- OAuth and platform capability verification.
- Controlled publishing and reconciliation report.
- Scheduler restart/concurrency/DST report.
- Backup/restore evidence.
- Performance and compatibility report.
- Installer signature and install/upgrade smoke report.
- Privacy notice review and release sign-off.

## 26.2 Test ownership

| Area | Responsible | Approval |
|---|---|---|
| Unit/module | Feature developer | Technical lead |
| API/database/integration | Backend developer | Technical lead/QA |
| UI/E2E | Frontend developer/QA | QA owner |
| OAuth/platform live | Integration engineer | Product owner |
| Security/privacy | Security reviewer/QA | Product owner |
| Backup/restore | Backend/QA | Technical lead |
| Installer/update | Release owner | Product owner |
| Final go/no-go | QA owner compiles evidence | Product/release owner |

**Final principle:** PostFlow is a stateful system with authority to publish externally. The release bar is correctness under failure, not merely a successful demo.

## M0 Reconciliation — Test Scope Override

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. This addendum supersedes conflicting MVP scope and priorities in this document. The target is a single-user, local-first Windows desktop MVP. Windows 11 is the production support baseline; Windows 10 is best-effort development only. P0 includes Tauri 2/Rust, React/TypeScript, supervised FastAPI, SQLite/SQLAlchemy/Alembic, local media, source content and independent revisioned variants, one AI provider, exact human approval, durable per-destination publishing jobs, idempotency/immutable attempts/unknown-outcome reconciliation, one-time local scheduling, privacy, backup and restore. At most one official social-platform integration may be enabled, and only after a documented PASS feasibility gate. Scheduling requires the app/worker active, device awake and internet available. Campaigns, team membership/roles, collaboration, billing, SaaS, cloud scheduling, public API, cloud media relay, additional AI providers/platforms, multi-provider comparison/fallback and advanced social analytics are P1/Future, not MVP requirements.

P0 tests: Windows 11 install/startup; process supervision; loopback-only authenticated API and frontend-secret isolation; fresh/populated DB migrations and restore; source/variant/revision isolation; one AI adapter, disclosure, secret redaction, provider failure, invalid output and no fallback; media traversal/spoof/oversize/resource limits; approval invalidation; job idempotency, immutable attempts, retry classification and unknown-outcome reconciliation; one-time schedule restart recovery, concurrency and DST; privacy/export/deletion. OAuth and real publish tests are conditional on platform PASS and use controlled test accounts. Windows 10 is not a production release target. Multi-provider, extra platforms, campaigns, team workflows, SaaS, cloud scheduling and advanced analytics are deferred.
