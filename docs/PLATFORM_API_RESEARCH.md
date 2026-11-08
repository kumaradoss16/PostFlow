# PostFlow - Platform API Research

**Document:** `PLATFORM_API_RESEARCH.md`  
**Product:** PostFlow  
**Research date:** 8 November 2026  
**Status:** Technical research and integration planning  
**Scope:** LinkedIn, Facebook Pages, Instagram, Threads, Pinterest, X and Reddit  
**Target deployment:** Windows desktop application, with future SaaS support  
**Research standard:** Official platform documentation and developer policies take precedence over third-party implementation guides.

---

## 1. Executive Summary

### 1.1 Purpose

This document evaluates the official APIs required to integrate PostFlow with its target social media platforms.

It establishes:

- API availability and technical capabilities.
- Authentication and authorization requirements.
- OAuth implementation considerations.
- Account eligibility.
- Publishing and media workflows.
- API permissions and scopes.
- Rate limits and usage costs.
- Analytics availability.
- Platform approval and application review.
- Data retention and compliance requirements.
- Integration architecture.
- Implementation priorities.
- Testing and release requirements.
- Known technical and commercial risks.

The goal is to prevent PostFlow from building features around unsupported or unapproved API capabilities.

### 1.2 Executive assessment

| Platform | Official API | Publishing potential | Main dependency | Priority |
|---|---|---|---|---|
| LinkedIn | Yes | Text, images, video, documents and other supported formats | Community Management API approval and permissions | P0 |
| Facebook Pages | Yes | Page content publishing | Meta app permissions and access review | P0 |
| Instagram | Yes | Professional-account publishing | Eligible account, permissions and media delivery | P0 |
| Threads | Yes | Text and supported media publishing | Threads authorization and publishing permissions | P1 |
| Pinterest | Yes | Image and video Pins | API access tier and board permissions | P1 |
| X | Yes | Post creation and supported media | Developer access and consumption-based API costs | P2 |
| Reddit | Yes | Submission workflows subject to authorization | Commercial-use permission and applicable contract | Deferred |

<badge color="warning">Critical dependency</badge> Platform API access is not guaranteed merely because an endpoint exists in public documentation.

The product must distinguish:

1. API functionality documented by the platform.
2. Functionality available to an approved developer application.
3. Functionality available to a particular account.
4. Functionality actually implemented and tested by PostFlow.

These are four different levels of support.

### 1.3 Recommended strategy

Implement a provider-independent publishing architecture with one adapter per social network.

Use official APIs wherever authorized. Provide manual publishing assistance for destinations that cannot be connected or automatically published.

Do not build the application around browser automation, scraping, unofficial APIs or credential collection.

---

## 2. Research Methodology

### 2.1 Source hierarchy

Use the following source hierarchy when making implementation decisions:

1. Official platform API documentation.
2. Official developer policies and terms.
3. Official API reference and changelog.
4. Official developer support and application-review guidance.
5. Official platform Postman collections.
6. Reputable technical implementation references.
7. Community discussions for troubleshooting only.

Third-party examples may help explain an implementation, but they must not override official documentation.

### 2.2 Research classifications

Each integration uses the following classifications:

| Classification | Meaning |
|---|---|
| Documented | The platform documents the capability |
| Approval-dependent | Developer application approval or a higher API tier is required |
| Account-dependent | The social account must meet eligibility conditions |
| Permission-dependent | The OAuth authorization must include the required scopes |
| Cost-dependent | API consumption or infrastructure can incur costs |
| Unverified | Current implementation requirements need direct confirmation |
| Deferred | Excluded from the initial implementation |

### 2.3 Important limitation

This document is a research baseline, not a production API certification.

Before implementation and release, PostFlow must verify the exact current API version, scopes, permissions, rate limits, media requirements, developer application status and commercial terms.

---

## 3. Cross-Platform API Architecture

### 3.1 Architecture overview

All social platform integrations should implement a shared internal contract.

```text
                    POSTFLOW DESKTOP
                           |
                           v
                  SOCIAL ACCOUNT MODULE
                           |
                           v
                  INTEGRATION REGISTRY
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     LINKEDIN ADAPTER  META ADAPTER    THREADS ADAPTER
          |                |                |
          v                v                v
      LinkedIn API      Meta APIs       Threads API

          +----------------+----------------+
          |                |                |
          v                v                v
    PINTEREST ADAPTER    X ADAPTER     REDDIT ADAPTER
          |                |                |
          v                v                v
      Pinterest API      X API          Reddit API
                           |
                           v
                  PUBLISHING ORCHESTRATOR
                           |
                           v
                  PERSISTENT JOB QUEUE
                           |
                           v
                  PUBLISH ATTEMPT HISTORY
                           |
                           v
                   LOCAL SQLITE DATABASE
```

### 3.2 Adapter responsibilities

Every platform adapter should implement a common set of operations where supported.

| Operation | Description |
|---|---|
| `get_authorization_url` | Build the platform authorization URL |
| `exchange_authorization_code` | Exchange an authorization code for tokens |
| `refresh_access_token` | Refresh an expiring token where supported |
| `get_account_profile` | Retrieve authorized account information |
| `get_capabilities` | Return supported account and publishing capabilities |
| `validate_post` | Validate a destination-specific post |
| `upload_media` | Upload or prepare media |
| `create_post` | Publish content |
| `get_post_status` | Retrieve publication status where supported |
| `get_post_metrics` | Retrieve available analytics where authorized |
| `revoke_or_disconnect` | Disconnect the account and remove credentials |

Not every platform supports every operation.

Unsupported operations must return an explicit capability error instead of pretending that a universal implementation exists.

### 3.3 Recommended interface

```python
from typing import Protocol


class SocialPlatformAdapter(Protocol):

    platform_id: str

    async def get_authorization_url(self, state: str) -> str:
        ...

    async def exchange_authorization_code(
        self,
        code: str,
        redirect_uri: str
    ) -> dict:
        ...

    async def get_account_profile(self, token: str) -> dict:
        ...

    async def get_capabilities(self, account_id: str) -> dict:
        ...

    async def validate_post(
        self,
        account_id: str,
        payload: dict
    ) -> dict:
        ...

    async def upload_media(
        self,
        account_id: str,
        media: dict
    ) -> dict:
        ...

    async def create_post(
        self,
        account_id: str,
        payload: dict,
        idempotency_key: str
    ) -> dict:
        ...

    async def get_post_status(
        self,
        account_id: str,
        remote_post_id: str
    ) -> dict:
        ...

    async def get_post_metrics(
        self,
        account_id: str,
        remote_post_id: str
    ) -> dict:
        ...
```

The interface is a proposed internal abstraction. It does not imply that every platform exposes equivalent endpoints or idempotency guarantees.

### 3.4 Capability registry

Do not use a single boolean such as `supports_publishing`.

Maintain detailed account-specific capabilities.

Example:

```json
{
  "platform": "instagram",
  "account_type": "business",
  "capabilities": {
    "text": false,
    "image": true,
    "video": true,
    "reels": true,
    "carousel": true,
    "stories": "conditional",
    "publishing": true,
    "analytics": "permission_dependent"
  },
  "authorization_status": "connected",
  "approval_status": "approved",
  "last_verified_at": "2026-11-08T00:00:00Z"
}
```

Capability values should be derived from the actual integration, account type, authorization and platform policy.

They must not be hardcoded as universal platform properties.

---

## 4. OAuth and Authentication Architecture

### 4.1 Authentication model

All integrations should use official OAuth workflows wherever supported.

General authorization flow:

```text
User selects Connect Account
           |
           v
PostFlow generates state and PKCE verifier
           |
           v
Open platform authorization page
           |
           v
User authenticates and grants permissions
           |
           v
Platform redirects with authorization code
           |
           v
Validate state and callback
           |
           v
Exchange authorization code
           |
           v
Validate returned permissions
           |
           v
Retrieve account identity
           |
           v
Store tokens securely
           |
           v
Mark account as connected
```

### 4.2 OAuth security requirements

Implement:

- Cryptographically random OAuth state.
- PKCE with S256 where supported.
- Exact redirect URI validation.
- Authorization-code single-use handling.
- Token expiration tracking.
- Refresh-token rotation handling where applicable.
- Minimum necessary scopes.
- Token revocation handling.
- Account identity verification.
- Secure credential storage.
- OAuth error handling.
- Reauthorization workflows.

Do not assume all providers support identical OAuth features.

### 4.3 Desktop OAuth design

A distributed desktop application has an important security problem.

A desktop executable is a public client. It cannot safely protect an embedded application secret.

Therefore:

**Never embed confidential OAuth client secrets in the distributed PostFlow executable.**

Recommended production design:

- Keep provider client secrets on a controlled backend OAuth broker where required.
- Use PKCE and public-client flows when the provider supports them.
- Use a registered application redirect URI appropriate to the provider.
- Validate callback state.
- Exchange authorization codes through the appropriate secure flow.
- Store user tokens locally in Windows DPAPI or Credential Manager when using the desktop deployment.
- Never send provider tokens to an unrelated third party.

A minimal OAuth broker may be required even before PostFlow becomes a full SaaS product.

If a provider supports a suitable public-client authorization flow, a broker may not be required for that provider.

### 4.4 Token storage

Recommended local storage:

| Data | Storage |
|---|---|
| Access token | Windows secure credential storage |
| Refresh token | Windows secure credential storage |
| OAuth client secret | Backend secret manager, where applicable |
| Account metadata | SQLite |
| Token expiry | SQLite |
| Granted scopes | SQLite |
| Connection status | SQLite |
| Authorization history | Audit log |

Do not store plaintext access tokens in ordinary SQLite columns.

### 4.5 Token lifecycle

The application should handle:

- Valid token.
- Expiring token.
- Refresh required.
- Refresh failed.
- Permission revoked.
- Account disconnected.
- Invalid grant.
- Reauthorization required.

Token refresh must not trigger a duplicate publishing operation.

---

## 5. LinkedIn API Research

<badge color="success">P0 - First integration target</badge>

### 5.1 Official documentation

- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [Community Management API Overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview)
- [Community Management API Migration Guide](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide)

### 5.2 API overview

The Posts API supports creation and retrieval of organic and sponsored posts.

Supported organic post formats documented by LinkedIn include:

- Text.
- Images.
- Videos.
- Documents.
- Articles.
- Multi-image posts.
- Polls.
- Celebrations.

Carousels are not listed as supported organic posts in the current Posts API content-type matrix. Do not assume that a sponsored carousel capability is available for organic publishing.

### 5.3 Authentication

LinkedIn uses OAuth 2.0 authorization.

The integration must use the permissions appropriate to the intended member or organization workflow.

Relevant permissions documented for the Posts API include:

| Permission | Purpose | Consideration |
|---|---|---|
| `w_member_social` | Publish on behalf of an authenticated member | Access is subject to the applicable LinkedIn API product |
| `r_member_social` | Retrieve member social data | Closed permission; current documentation states requests are not being accepted |
| `w_organization_social` | Publish on behalf of an organization | Requires eligible organization role and API access |
| `r_organization_social` | Read organization social data | Requires eligible organization role and API access |

Organization posting is restricted to eligible company-page roles, including:

- Administrator.
- Direct Sponsored Content Poster.
- Content Admin.

The exact permission mapping must be checked against the current API version and access tier.

### 5.4 API versioning

LinkedIn Marketing APIs require a version header in the format:

```http
Linkedin-Version: YYYYMM
X-Restli-Protocol-Version: 2.0.0
```

Do not use an old hardcoded version indefinitely.

Maintain a configurable version value and a documented migration process.

### 5.5 Access approval

LinkedIn Community Management API access is vetted.

The current documentation describes:

- Development Tier.
- Standard Tier.

The Development Tier has restricted API call volume. The published documentation lists 500 calls per app and 100 calls per member per 24 hours.

Standard Tier requires an additional review and approval process.

The documentation also states that Community Management API commercial use is limited to registered legal organizations and that access review can require organization verification, business contact information, a verified company page, privacy policy and an application screencast.

The `r_member_social` permission is currently documented as closed to new access requests.

This is a major dependency for a commercial PostFlow release.

### 5.6 Publishing workflow

Recommended flow:

1. Authenticate the user.
2. Retrieve eligible member or organization identity.
3. Verify the required publishing permission.
4. Validate post content.
5. Upload media using the appropriate LinkedIn media workflow.
6. Create the post using the Posts API.
7. Capture the returned post identifier.
8. Record the publication result.
9. Reconcile uncertain responses before retrying.

### 5.7 Media support

PostFlow should implement separate workflows for:

- Text.
- Image.
- Video.
- Document.
- Multi-image.

Do not assume all formats share the same upload process.

### 5.8 PostFlow implementation scope

| Feature | Priority |
|---|---|
| Member text post | P0, subject to approved permission |
| Organization text post | P0, subject to access and page role |
| Image post | P0 |
| Video post | P1 |
| Document post | P1 |
| Multi-image post | P1 |
| Poll | P2 |
| Organization analytics | P1, subject to read permissions |
| Member analytics | Unverified / permission-dependent |

### 5.9 Key risks

- Community Management API approval.
- Legal organization verification.
- Organization administrator eligibility.
- Closed member-read permission.
- API version migration.
- Development Tier request restrictions.
- Standard Tier review delays.

**Decision:** Build the adapter architecture early, but do not promise unrestricted LinkedIn member publishing until the application has obtained and tested the required permissions.

---

## 6. Facebook Pages API Research

<badge color="success">P0 - Meta integration</badge>

### 6.1 Official documentation

- [Meta Pages API](https://developers.facebook.com/documentation/pages-api/)
- [Meta Pages API Posts](https://developers.facebook.com/documentation/pages-api/posts)
- [Meta Graph API](https://developers.facebook.com/docs/graph-api/)
- [Meta Permissions Reference](https://developers.facebook.com/docs/permissions/)

### 6.2 API overview

The Facebook Pages API provides functionality for managing eligible Facebook Pages.

Potential PostFlow use cases:

- Retrieve authorized Pages.
- Retrieve Page metadata.
- Publish Page posts.
- Publish supported media.
- Retrieve published content.
- Retrieve supported Page engagement data.
- Manage supported post operations.

This integration should focus on Facebook Pages.

Do not promise unrestricted personal Facebook profile publishing.

### 6.3 Authentication

The integration generally requires:

- Meta developer application.
- OAuth authorization.
- User authorization.
- Eligible Page access.
- Appropriate permissions.
- Page access token for Page operations.

Relevant permission candidates include:

| Permission | Purpose |
|---|---|
| `pages_show_list` | Discover Pages available to the authorized user |
| `pages_read_engagement` | Read supported Page engagement data |
| `pages_manage_posts` | Manage and publish Page posts |
| `pages_read_user_content` | Read applicable user-generated Page content, where needed |

Request only permissions required by the feature being implemented.

Permission availability and review requirements depend on the app mode, access level and intended user population.

### 6.4 Publishing workflow

General flow:

1. Authorize the user through Meta OAuth.
2. Retrieve eligible Pages.
3. Allow the user to select a Page.
4. Retrieve the appropriate Page access token.
5. Validate content and media.
6. Execute the supported publishing endpoint.
7. Capture the returned post identifier.
8. Store the publication attempt.
9. Retrieve publication status when supported.

### 6.5 API endpoint families

Examples of relevant endpoint families include:

```http
GET  /{user-id}/accounts
POST /{page-id}/feed
POST /{page-id}/photos
POST /{page-id}/videos
GET  /{page-id}/posts
```

These are endpoint-family references. Exact fields, permissions, API versions and media workflows must be checked against the current official documentation.

### 6.6 Scheduling

PostFlow should initially own its scheduling logic.

The local scheduler should decide when a publishing job executes and then invoke the appropriate Page publishing endpoint.

This avoids relying on different platform-native scheduling features as if they were identical.

Where platform-native scheduling is supported and useful, it can be implemented as a separate capability.

### 6.7 PostFlow implementation scope

| Feature | Priority |
|---|---|
| Connect Facebook account | P0 |
| Discover eligible Pages | P0 |
| Publish text to Page | P0 |
| Publish image to Page | P0 |
| Publish supported video | P1 |
| Retrieve post identifier | P0 |
| Retrieve supported Page metrics | P1 |
| Schedule through PostFlow | P0 |
| Personal profile publishing | Excluded unless officially supported |

### 6.8 Key risks

- Meta application review.
- Page authorization.
- Token expiration and revocation.
- API version migration.
- Media upload requirements.
- Permission restrictions.
- Page-level publishing limitations.

**Decision:** Prioritize Page publishing as part of the Meta integration, with a separate capability registry for each Page and media type.

---

## 7. Instagram API Research

<badge color="success">P0 - Meta integration</badge>

### 7.1 Official documentation

- [Instagram Platform](https://developers.facebook.com/docs/instagram-platform/)
- [Instagram Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/)

### 7.2 Account eligibility

Instagram API publishing is not universally available to all Instagram accounts.

PostFlow should target eligible:

- Business accounts.
- Creator accounts.

Do not assume that ordinary personal Instagram accounts can use the same publishing API.

There are two relevant authorization approaches:

1. Instagram API with Instagram Login.
2. Instagram API with Facebook Login.

They have different permission and account-linking requirements.

Select one supported flow initially and avoid mixing token assumptions between them.

### 7.3 Instagram Login permissions

Relevant current permission names include:

| Permission | Purpose |
|---|---|
| `instagram_business_basic` | Access basic professional account information |
| `instagram_business_content_publish` | Publish supported Instagram content |
| `instagram_business_manage_comments` | Manage supported comments |
| `instagram_business_manage_messages` | Manage supported messaging operations |

For the Instagram Login flow, use the current permission names documented by Meta.

Older scope names such as `business_basic` and `business_content_publish` should not be used in new implementations.

### 7.4 Facebook Login permissions

The Facebook Login flow uses a different permission model.

Relevant permission candidates include:

- `instagram_basic`.
- `instagram_content_publish`.
- `pages_show_list`.
- `pages_read_engagement`.
- Additional permissions when other capabilities are required.

A professional Instagram account may need to be associated with a Facebook Page for this flow.

Do not mix permissions from the two login approaches without understanding their respective documentation.

### 7.5 Content publishing workflow

Instagram publishing generally uses a media-container workflow.

```text
Prepare media
     |
     v
Make media accessible to Meta
     |
     v
Create media container
     |
     v
Check container processing status
     |
     v
Publish media container
     |
     v
Capture returned media identifier
     |
     v
Verify publication result
```

Relevant endpoint families include:

```http
POST /{ig-user-id}/media
POST /{ig-user-id}/media_publish
GET  /{container-id}
```

Exact request fields depend on media type and API version.

### 7.6 Media delivery requirements

This is a major architectural issue for PostFlow.

A local filesystem path is not a public media URL.

If the publishing API requires Meta to retrieve media from a URL, PostFlow must provide a valid delivery mechanism.

Potential approaches:

**Option A - Temporary object storage**

- Upload media to controlled storage.
- Generate a time-limited or otherwise appropriately protected media URL.
- Submit the URL to the platform.
- Remove temporary data according to retention policy.

**Option B - User-configured storage**

Allow users to connect an object storage service.

**Option C - Supported upload workflow**

Use an official resumable or direct upload workflow where supported by the selected API and media type.

**Option D - Manual publishing**

If automated publishing cannot be performed, prepare the media and content for user-assisted publication.

Never assume that a local `file://` path or a private LAN URL is accessible to Meta.

### 7.7 Supported content formats

The integration should evaluate:

- Single image.
- Single video.
- Reels.
- Carousel.
- Stories.

Support depends on the selected API flow, account type and current platform rules.

Stories have additional restrictions and should not be assumed available to every professional account.

### 7.8 Publishing limits

The platform exposes publishing-limit information.

PostFlow should retrieve or otherwise respect the current platform-provided limits instead of hardcoding a universal daily posting number.

### 7.9 PostFlow implementation scope

| Feature | Priority |
|---|---|
| Professional account authorization | P0 |
| Retrieve account identity | P0 |
| Image publishing | P0 |
| Caption validation | P0 |
| Media container processing | P0 |
| Reels | P1 |
| Carousel | P1 |
| Stories | P2, account-dependent |
| Instagram insights | P1, permission-dependent |
| Personal account publishing | Excluded |

### 7.10 Key risks

- Professional account eligibility.
- Meta app review.
- Public media delivery.
- Media processing delays.
- Publishing limits.
- Account-specific restrictions.
- API version changes.
- Difference between Instagram Login and Facebook Login.

**Decision:** Instagram is a high-priority integration, but media delivery and app authorization must be validated before implementing the complete publishing workflow.

---

## 8. Threads API Research

<badge color="warning">P1 - Verify authorization before commitment</badge>

### 8.1 Official documentation

- [Threads API](https://developers.facebook.com/docs/threads/)
- [Threads API Publishing Documentation](https://developers.facebook.com/docs/threads/posts/)
- [Meta Developer Platform](https://developers.facebook.com/)

### 8.2 API overview

Threads provides an official API for authorized account operations.

Potential PostFlow functionality includes:

- Account authorization.
- Account identity retrieval.
- Text publishing.
- Supported image and video publishing.
- Supported reply and conversation operations.
- Available insights and metrics.

Exact capabilities must be confirmed against the current API reference.

### 8.3 Authentication

The Threads API uses a Meta-supported OAuth workflow.

Relevant scope families include:

- `threads_basic`.
- `threads_content_publish`.
- Additional read, reply or interaction scopes when required by the implemented functionality.

Do not request additional interaction scopes merely because they exist.

### 8.4 Publishing workflow

The integration should follow the official Threads publishing flow.

A typical workflow uses a content-creation operation followed by a publishing operation.

The adapter must handle:

- Media processing.
- Container or draft state where applicable.
- Publishing status.
- Returned content identifiers.
- API errors.
- Platform rate limits.

Exact endpoints and payload formats must be verified before implementation.

### 8.5 PostFlow implementation scope

| Feature | Priority |
|---|---|
| Threads authorization | P1 |
| Account identity | P1 |
| Text publishing | P1 |
| Image publishing | P1 |
| Video publishing | P2 |
| Replies and conversation features | Future |
| Insights | P2, permission-dependent |

### 8.6 Key risks

- OAuth scope changes.
- App review requirements.
- Account eligibility.
- Media processing.
- Rate limits.
- Feature differences between Threads and Instagram.

**Decision:** Build a separate Threads adapter. Do not reuse the Instagram adapter's publishing implementation simply because both platforms use Meta infrastructure.

**Verification requirement:** Before coding, verify current endpoint paths, scope names, media workflows, token lifecycle and publishing limits directly in the official Threads documentation. These details are not treated as release-approved in this research baseline.

---

## 9. Pinterest API Research

<badge color="warning">P1 - Access-tier dependency</badge>

### 9.1 Official documentation

- [Pinterest API](https://developers.pinterest.com/)
- [Pinterest API v5](https://developers.pinterest.com/docs/api/v5/)
- [Access Tiers](https://developers.pinterest.com/docs/key-concepts/access-tiers/)
- [Create Boards and Pins](https://developers.pinterest.com/docs/work-with-organic-content-and-users/create-boards-and-pins/)
- [Authentication and Authorization](https://developers.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/)
- [Rate Limits](https://developers.pinterest.com/docs/reference/rate-limits/)

### 9.2 API overview

Pinterest API v5 provides functionality for:

- Account information.
- Boards.
- Pins.
- Pin creation.
- Pin retrieval.
- Board management.
- Supported analytics.
- Additional business features.

### 9.3 Authentication

Pinterest supports OAuth 2.0.

Relevant scopes include:

| Scope | Purpose |
|---|---|
| `boards:read` | Read eligible boards |
| `boards:write` | Create or manage boards |
| `pins:read` | Read Pins |
| `pins:write` | Create or manage Pins |

For a basic publishing integration, request the minimum scopes needed to discover boards and create Pins.

### 9.4 Access tiers

Pinterest documents Trial and Standard access.

Trial access is intended for API exploration and testing.

The documentation states that Pins and boards created under Trial access are visible only to the creator.

Standard access is required for broader production functionality.

This creates an important release dependency.

PostFlow must not treat successful sandbox or Trial publishing as proof of production readiness.

### 9.5 Publishing workflow

Typical flow:

1. Connect Pinterest account.
2. Retrieve eligible boards.
3. Allow the user to select a board.
4. Validate Pin title and description.
5. Validate media.
6. Create a Pin using the official API.
7. Capture the returned Pin identifier.
8. Record the result.

### 9.6 Supported media

Pinterest documents support for:

- Image Pins.
- Video Pins.

Additional product-tagging functionality is available for eligible organic Pins.

Do not include product tagging in the MVP unless its eligibility and data requirements have been validated.

### 9.7 Rate limits

The current Pinterest documentation lists:

- Trial access: 1,000 requests per day for all API requests.
- Standard access: 100 requests per second per user per app as a universal limit.
- Endpoint-category-specific limits also apply.

For example, the documented `org_write` category has separate Trial and Standard limits.

PostFlow must monitor response headers and handle HTTP 429 responses.

Do not implement one global rate limit for all Pinterest endpoints.

### 9.8 Token lifecycle

The official authentication documentation includes:

- Access tokens.
- Refresh tokens.
- Token expiration.
- Scope information.

The documented authorization-code example returns a 30-day access token and a longer refresh-token lifetime. These values must be treated as current documented examples and revalidated during implementation.

### 9.9 PostFlow implementation scope

| Feature | Priority |
|---|---|
| OAuth connection | P1 |
| Retrieve boards | P1 |
| Image Pin publishing | P1 |
| Video Pin publishing | P2 |
| Board management | P2 |
| Pin metrics | P2 |
| Product tagging | Future |

### 9.10 Key risks

- Trial-to-Standard upgrade.
- Application approval.
- Scope configuration.
- Media processing.
- Rate limits.
- Refresh-token lifecycle.
- Board eligibility.

**Decision:** Develop the adapter after the first Meta and LinkedIn publishing workflows are stable. Obtain Standard access before declaring Pinterest production-ready.

---

## 10. X API Research

<badge color="warning">P2 - Cost-sensitive integration</badge>

### 10.1 Official documentation

- [X Developer Platform](https://developer.x.com/)
- [X API Documentation](https://developer.x.com/en/docs)
- [X API v2 Reference](https://developer.x.com/en/docs/api-reference-index)
- [X Developer Console](https://console.x.com/)

### 10.2 API overview

X API supports authenticated account operations, post creation, media workflows and other developer capabilities.

PostFlow's initial objective should be limited to authorized post publishing and basic publication status tracking.

### 10.3 Authentication

Use the current supported OAuth 2.0 user-context flow for applicable endpoints.

The implementation must confirm the required user scopes.

For post creation, the relevant permission family includes:

- `tweet.write`.
- `tweet.read`.
- `users.read`.
- `offline.access` when a refresh-token workflow is required and supported by the selected authorization configuration.

Exact scope requirements must be verified against the endpoint and current authentication documentation.

### 10.4 Post creation

The X API v2 post-creation endpoint is:

```http
POST https://api.x.com/2/tweets
```

The application should:

1. Authorize the user.
2. Validate the post text.
3. Prepare supported media.
4. Upload media using the appropriate workflow.
5. Create the post.
6. Capture the returned post identifier.
7. Record the attempt.
8. Reconcile uncertain outcomes.

### 10.5 Media support

Media publishing requires a separate upload workflow.

Do not rely on deprecated media endpoints or obsolete API examples.

Validate current support for:

- Images.
- GIFs.
- Video.
- Multiple attachments.
- Media processing.
- Media upload limits.

### 10.6 API pricing

The X Developer Platform currently advertises consumption-based billing.

The public pricing page lists examples such as:

| Resource | Advertised unit price |
|---|---:|
| Posts: Read | USD 0.005 per resource |
| User: Read | USD 0.010 per resource |
| Post: Create | USD 0.015 per request |
| Content: Create | USD 0.010 per request |

These are observed public prices at the research date, not guaranteed future rates.

Actual billing may differ due to usage, taxes, fees, rate changes and other applicable charges.

### 10.7 Cost-control requirements

PostFlow should:

- Track API consumption.
- Estimate publishing costs.
- Display usage information.
- Avoid unnecessary read requests.
- Avoid polling when webhooks or other supported mechanisms are preferable.
- Allow the user to disable X integration.
- Prevent unexpected API spending.
- Provide a cost warning before high-volume operations.

Do not promise unlimited X publishing as part of a low-cost subscription unless the economics have been validated.

### 10.8 PostFlow implementation scope

| Feature | Priority |
|---|---|
| OAuth connection | P2 |
| Text publishing | P2 |
| Image publishing | P2 |
| Video publishing | P2 |
| Post status tracking | P2 |
| Analytics | P2 |
| API usage tracking | P0 for X integration |
| Cost estimation | P1 |
| Automated engagement | Excluded from MVP |

### 10.9 Key risks

- Consumption-based API charges.
- Pricing changes.
- Scope restrictions.
- Media upload complexity.
- Rate limits.
- User authorization.
- API endpoint changes.

**Decision:** Keep X optional. Implement it only after confirming the API cost model and acceptable publishing economics.

---

## 11. Reddit API Research

<badge color="danger">Deferred - Commercial permission required</badge>

### 11.1 Official documentation

- [Reddit Developer Platform](https://developers.reddit.com/)
- [Reddit Data API Wiki](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)
- [Reddit Developer Platform Accessing Reddit Data](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data)
- [Reddit Data API Terms](https://redditinc.com/policies/data-api-terms)

### 11.2 API overview

Reddit provides developer APIs for authorized operations.

Potential functionality includes:

- OAuth authentication.
- Account information.
- Subreddit information.
- Submission creation.
- Comment operations.
- Other supported community interactions.

However, technical endpoint availability does not establish commercial permission.

### 11.3 Commercial-use restriction

Reddit's official developer guidance states that commercial use of its developer tools and services requires prior permission.

Its definition of commercial use includes monetized applications, subscription services and products offered by or on behalf of a business.

The documentation also states that commercial use may require a contract.

This applies directly to a monetized PostFlow product.

### 11.4 Data API rules

The Reddit Data API documentation includes requirements relating to:

- OAuth authentication.
- Rate limits.
- Deleted content.
- User deletion.
- Data retention.
- Developer terms.
- Responsible Builder Policy.

The current Data API Wiki recommends routinely deleting stored user data and content that has been deleted from Reddit, and notes a 48-hour recommendation.

The documented free-access Data API limit is 100 queries per minute per OAuth client ID, subject to the applicable policy and rate-limit conditions.

### 11.5 AI and data usage

Reddit explicitly restricts using its content to train large language models without explicit consent.

PostFlow must not use Reddit data for model training or model-training datasets without the required permission.

### 11.6 PostFlow recommendation

Do not implement Reddit commercial publishing as an MVP dependency.

Before enabling a Reddit API integration:

1. Submit the intended use case to Reddit.
2. Obtain explicit commercial-use permission.
3. Confirm contractual requirements.
4. Confirm API access.
5. Review retention and deletion obligations.
6. Review rate limits.
7. Implement compliance controls.
8. Obtain legal review where appropriate.

### 11.7 Alternative functionality

Until commercial permission is obtained, PostFlow may support manual content preparation for Reddit where appropriate.

This must not involve:

- Scraping.
- Unofficial API access.
- Automated browser-based posting.
- Credential collection.
- Circumvention of platform restrictions.

**Decision:** Reddit remains a deferred integration and a release-blocking legal dependency for any commercial API-based functionality.

---

## 12. Cross-Platform Capability Matrix

This matrix is the proposed implementation target, not a guarantee of universal platform availability.

| Capability | LinkedIn | Facebook Pages | Instagram | Threads | Pinterest | X | Reddit |
|---|---|---|---|---|---|---|---|
| Text publishing | Yes | Yes | Caption with media workflow | Yes | Pin description | Yes | Submission-dependent |
| Image publishing | Yes | Yes | Yes | Supported | Yes | Yes | Submission-dependent |
| Video publishing | Yes | Yes | Yes | Supported | Yes | Yes | Submission-dependent |
| Document publishing | Yes | Not established as equivalent | No equivalent standard document post | Not established | Not applicable | Not equivalent | Not applicable |
| Carousel publishing | Not supported as organic carousel in current Posts API matrix | Format-dependent | Yes, subject to API flow | Verify | Not a universal carousel workflow | Not equivalent | Not equivalent |
| Polls | Yes, supported format | Format-dependent | No standard equivalent | Verify | Not applicable | Endpoint-dependent | Submission-dependent |
| Scheduling | PostFlow scheduler | PostFlow scheduler | PostFlow scheduler | PostFlow scheduler | PostFlow scheduler | PostFlow scheduler | Deferred |
| Analytics | Permission-dependent | Permission-dependent | Permission-dependent | Permission-dependent | Permission-dependent | Permission-dependent | Restricted |
| Commercial approval risk | High | Medium–High | Medium–High | Medium–High | Medium | Medium | Critical |

### Important interpretation

A `Yes` in this matrix means the platform documents a related capability. It does not guarantee that PostFlow's application will receive the necessary access.

The platform adapter must validate the capability for each connected account.

---

## 13. Media Handling Architecture

### 13.1 Media lifecycle

```text
Local Media Library
       |
       v
Media Validation
       |
       v
Platform-Specific Transformation
       |
       v
Destination Capability Check
       |
       v
Required Upload or Hosting Workflow
       |
       v
Platform Publishing Request
       |
       v
Publication Verification
       |
       v
Temporary Media Cleanup
```

### 13.2 Media metadata

Recommended fields:

```text
media_assets
------------
id
workspace_id
filename
original_filename
mime_type
file_size
width
height
duration
checksum
storage_path
created_at
updated_at
```

Platform-specific media preparation should be stored separately from the original asset.

### 13.3 Media validation

Validate:

- MIME type.
- File signature.
- File size.
- Image dimensions.
- Video dimensions.
- Video duration.
- Supported codecs.
- Aspect ratio.
- File extension.
- Platform-specific requirements.

Do not trust filename extensions as proof of file type.

### 13.4 Temporary hosting

For platforms requiring publicly accessible media:

- Upload only the necessary asset.
- Use an approved storage provider.
- Use short-lived access where supported.
- Avoid exposing permanent public media URLs unnecessarily.
- Record data-transmission events.
- Apply retention and deletion policies.
- Remove temporary assets after processing and the required retention period.

Do not delete temporary media immediately if the platform may still be processing it.

### 13.5 User disclosure

Before transmitting media outside the device, disclose:

- Destination platform.
- Storage provider.
- File being transferred.
- Reason for transfer.
- Expected retention.
- Whether the URL is public or access-controlled.

---

## 14. Unified Publishing Engine

### 14.1 Publishing model

A content item may target several platforms.

Each destination must have an independent publishing job.

Example:

```text
Content Item: Product Launch

   +-- LinkedIn Job
   +-- Instagram Job
   +-- Facebook Page Job
   +-- Threads Job
   +-- Pinterest Job
   +-- X Job
```

A successful destination must not be rolled back because another platform failed.

### 14.2 Publishing state machine

Recommended states:

```text
draft
  |
  v
awaiting_approval
  |
  v
approved
  |
  +----> scheduled
  |         |
  |         v
  |       queued
  |         |
  |         v
  |      publishing
  |         |
  |         +----> published
  |         |
  |         +----> failed
  |         |
  |         +----> unknown_outcome
  |
  +----> cancelled
```

Retry path:

```text
failed
  |
  v
retry_pending
  |
  v
queued
```

Unknown outcomes require reconciliation before another publishing attempt.

### 14.3 Idempotency

Every publishing job should have:

- Unique job ID.
- Content variant ID.
- Destination account ID.
- Revision number.
- Idempotency key.
- Attempt count.
- Last response.
- Remote post ID, if known.
- Current state.

Do not assume every social platform supports a native idempotency key.

PostFlow must implement its own duplicate-prevention strategy.

For an uncertain request:

1. Record the uncertain outcome.
2. Inspect the response and any returned identifier.
3. Query the platform where supported.
4. Reconcile whether the post exists.
5. Retry only when it is safe.

### 14.4 Retry classification

| Failure | Retry strategy |
|---|---|
| Network timeout before request transmission | Retry if safely identifiable |
| Network timeout after request transmission | Reconcile first |
| HTTP 400 validation error | Do not retry without changing input |
| HTTP 401 | Refresh or reauthorize |
| HTTP 403 | Verify permissions and account eligibility |
| HTTP 429 | Respect retry guidance and rate limits |
| HTTP 5xx | Controlled retry with backoff |
| Unknown outcome | Reconcile before retry |

### 14.5 Scheduler requirements

The scheduler must:

- Persist jobs in SQLite.
- Recover queued jobs after restart.
- Avoid duplicate execution.
- Use UTC internally.
- Store user timezone separately.
- Respect platform rate limits.
- Track missed schedules.
- Handle network outages.
- Support cancellation.
- Preserve attempt history.

For the initial desktop release, users must understand that scheduled publishing depends on the desktop application or its background service being active and the computer being able to access the internet.

---

## 15. Recommended Database Schema

The existing PostFlow database design should be extended to support platform-specific integration metadata.

### 15.1 Social accounts

```text
social_accounts
---------------
id
workspace_id
platform
platform_account_id
account_name
account_type
account_metadata
authorization_status
connection_status
created_at
updated_at
last_verified_at
```

### 15.2 OAuth credentials

```text
oauth_credentials
-----------------
id
social_account_id
credential_reference
token_type
granted_scopes
access_token_expires_at
refresh_token_expires_at
last_refreshed_at
created_at
updated_at
```

`credential_reference` should point to secure OS-backed credential storage, not contain a plaintext token.

### 15.3 Platform capabilities

```text
platform_capabilities
---------------------
id
social_account_id
capability_key
supported
availability_reason
last_verified_at
```

### 15.4 Publishing jobs

```text
publish_jobs
------------
id
content_variant_id
social_account_id
platform
scheduled_at
status
idempotency_key
attempt_count
remote_post_id
last_error_code
last_error_message
created_at
updated_at
```

### 15.5 Publishing attempts

```text
publish_attempts
----------------
id
publish_job_id
attempt_number
started_at
completed_at
request_metadata
response_metadata
http_status
remote_post_id
outcome
error_category
```

Never store raw access tokens or sensitive authorization headers in request or response metadata.

### 15.6 Platform API usage

```text
platform_api_usage
------------------
id
social_account_id
platform
endpoint_category
operation
request_count
estimated_cost
currency
recorded_at
```

This is especially relevant to X consumption-based billing.

### 15.7 Platform configuration

```text
platform_integrations
---------------------
id
platform
api_version
application_status
enabled
configuration
last_documentation_review
last_compatibility_test
created_at
updated_at
```

Do not store application secrets in ordinary configuration JSON.

---

## 16. Recommended API Module Structure

```text
backend/
└── app/
    ├── integrations/
    │   ├── registry.py
    │   ├── capabilities.py
    │   ├── base.py
    │   │
    │   ├── linkedin/
    │   │   ├── adapter.py
    │   │   ├── auth.py
    │   │   ├── posts.py
    │   │   ├── media.py
    │   │   ├── analytics.py
    │   │   └── schemas.py
    │   │
    │   ├── meta/
    │   │   ├── auth.py
    │   │   ├── facebook_pages/
    │   │   │   ├── adapter.py
    │   │   │   ├── posts.py
    │   │   │   ├── media.py
    │   │   │   └── schemas.py
    │   │   │
    │   │   └── instagram/
    │   │       ├── adapter.py
    │   │       ├── posts.py
    │   │       ├── media.py
    │   │       ├── insights.py
    │   │       └── schemas.py
    │   │
    │   ├── threads/
    │   │   ├── adapter.py
    │   │   ├── auth.py
    │   │   ├── posts.py
    │   │   └── schemas.py
    │   │
    │   ├── pinterest/
    │   │   ├── adapter.py
    │   │   ├── auth.py
    │   │   ├── boards.py
    │   │   ├── pins.py
    │   │   └── schemas.py
    │   │
    │   ├── x/
    │   │   ├── adapter.py
    │   │   ├── auth.py
    │   │   ├── posts.py
    │   │   ├── media.py
    │   │   ├── usage.py
    │   │   └── schemas.py
    │   │
    │   └── reddit/
    │       ├── adapter.py
    │       ├── auth.py
    │       ├── submissions.py
    │       └── schemas.py
    │
    ├── publishing/
    │   ├── orchestrator.py
    │   ├── scheduler.py
    │   ├── job_manager.py
    │   ├── retry_policy.py
    │   ├── reconciliation.py
    │   └── idempotency.py
    │
    └── security/
        ├── credential_store.py
        ├── oauth_state.py
        ├── token_manager.py
        └── audit.py
```

### Architecture rules

- Keep each platform adapter independent.
- Share only genuinely common functionality.
- Do not put platform-specific payloads into generic models.
- Version API clients explicitly.
- Use typed request and response schemas.
- Maintain platform-specific error mappings.
- Keep credentials outside normal application configuration.
- Keep the publishing orchestrator independent of provider SDKs.

---

## 17. Error Handling and Observability

### 17.1 Standard internal error categories

```text
AUTHORIZATION_ERROR
TOKEN_EXPIRED
TOKEN_REVOKED
INSUFFICIENT_PERMISSION
ACCOUNT_NOT_ELIGIBLE
UNSUPPORTED_CONTENT
MEDIA_VALIDATION_ERROR
MEDIA_UPLOAD_ERROR
RATE_LIMITED
PLATFORM_UNAVAILABLE
PUBLISHING_REJECTED
UNKNOWN_PUBLISHING_OUTCOME
API_VERSION_ERROR
COMMERCIAL_ACCESS_RESTRICTED
```

### 17.2 Standard internal error response

```json
{
  "success": false,
  "platform": "instagram",
  "error_category": "MEDIA_VALIDATION_ERROR",
  "platform_error_code": "PLATFORM_SPECIFIC_CODE",
  "message": "The media could not be accepted.",
  "retryable": false,
  "requires_user_action": true,
  "correlation_id": "request-id"
}
```

This is an internal PostFlow schema, not a response format returned by any social network.

### 17.3 Logging requirements

Log:

- Platform.
- Account identifier.
- Job identifier.
- Request correlation ID.
- Operation.
- API version.
- Response status.
- Platform error code.
- Retry decision.
- Attempt number.
- Duration.

Never log:

- Access tokens.
- Refresh tokens.
- Client secrets.
- Authorization headers.
- Full sensitive user payloads unless strictly necessary and explicitly protected.

---

## 18. Security and Compliance Requirements

### 18.1 Credential protection

- Use Windows DPAPI or Credential Manager.
- Never expose OAuth tokens to the React frontend.
- Never write secrets to ordinary logs.
- Encrypt sensitive backup data.
- Delete credentials when an account is disconnected.
- Handle credential revocation.
- Avoid embedding confidential OAuth secrets in the distributed desktop application.

### 18.2 OAuth protection

- State validation.
- PKCE where supported.
- Redirect URI allowlisting.
- Authorization-code replay protection.
- Token rotation.
- Minimal scopes.
- Secure callback handling.

### 18.3 User authorization

Each connected account must represent an account the user owns or is explicitly authorized to manage.

PostFlow must not:

- Collect social account passwords.
- Impersonate users.
- Circumvent platform authorization.
- Scrape private account information.
- Automate restricted engagement activity.
- Bypass rate limits.

### 18.4 AI content safety

AI-generated content must remain untrusted until validated.

The application should:

- Keep generated content in draft state.
- Require approval by default.
- Validate platform-specific constraints.
- Avoid automatic publication of unreviewed content by default.
- Maintain content revision history.
- Bind approval to an exact content revision.

### 18.5 Data retention

Define retention policies for:

- OAuth credentials.
- Platform metadata.
- Published post identifiers.
- Analytics snapshots.
- Media uploads.
- Platform-derived content.
- Logs.
- User-deleted data.

Platform-specific retention and deletion obligations must override generic PostFlow retention preferences where required.

### 18.6 Legal review

Before public commercial launch, review:

- Platform developer terms.
- Platform branding and trademark requirements.
- Data processing obligations.
- Privacy policy.
- User consent.
- Data deletion.
- API commercial-use restrictions.
- Cross-border data transmission.
- Applicable privacy and consumer laws.

This document is technical research, not legal advice.

---

## 19. Implementation Priority and Roadmap

### Phase 0 - API access validation

**Objective:** Confirm that PostFlow can obtain the necessary API access before investing heavily in integration development.

Deliverables:

- Developer applications.
- API access requests.
- OAuth configuration.
- Required scopes.
- Test accounts.
- Permission validation.
- API cost assessment.
- Media delivery feasibility.
- Commercial terms review.

Exit criteria:

- Required developer applications are approved or their limitations are documented.
- OAuth works for eligible test accounts.
- Basic API calls are successful.
- Publishing feasibility is demonstrated.
- Unavailable features are removed from the MVP commitment.

### Phase 1 - LinkedIn integration

Deliverables:

- OAuth flow.
- Account identity.
- Organization eligibility.
- Text publishing.
- Image publishing.
- Post identifier tracking.
- Error handling.
- Permission validation.

Release gate:

- Successful test publication to an authorized test account.
- Confirmed access tier.
- No token exposure.
- Reliable attempt history.

### Phase 2 - Meta integration

Deliverables:

- Meta OAuth.
- Facebook Page discovery.
- Facebook Page publishing.
- Instagram professional account connection.
- Instagram media publishing.
- Media container handling.
- Temporary media delivery.
- Token lifecycle.

Release gate:

- Successful Page publishing.
- Successful eligible Instagram publishing.
- Verified account eligibility.
- Tested media cleanup.
- Correct permission handling.

### Phase 3 - Threads

Deliverables:

- Threads authorization.
- Text publishing.
- Supported media workflows.
- Status tracking.
- Error handling.

Release gate:

- Verified current API scopes and endpoints.
- Successful test publication.
- Correct capability registry.

### Phase 4 - Pinterest

Deliverables:

- OAuth.
- Board discovery.
- Image Pin publishing.
- Video Pin support.
- Rate-limit handling.
- Token refresh.

Release gate:

- Standard access approval for production functionality.
- Successful external visibility test.
- Tested rate-limit handling.

### Phase 5 - X

Deliverables:

- OAuth.
- Text publishing.
- Media publishing.
- Usage tracking.
- Cost estimation.
- Rate-limit handling.

Release gate:

- Confirmed API access.
- Verified current pricing.
- Successful publishing.
- Acceptable cost per expected usage profile.

### Phase 6 - Reddit assessment

Deliverables:

- Commercial-use application.
- Terms review.
- Permission assessment.
- API access assessment.
- Data retention design.

Release gate:

- Explicit commercial-use permission.
- Contractual requirements satisfied.
- Technical and compliance validation.

Until this gate passes, the Reddit adapter must remain disabled in commercial releases.

---

## 20. Testing Strategy

### 20.1 Unit tests

Test:

- OAuth state generation.
- PKCE generation.
- Token expiry calculations.
- Token refresh.
- Capability evaluation.
- Content validation.
- Media validation.
- Error mapping.
- Retry classification.
- Idempotency key generation.

### 20.2 Integration tests

Test:

- OAuth connection.
- Account discovery.
- Permission validation.
- Text publishing.
- Image publishing.
- Video publishing where implemented.
- Post identifier retrieval.
- Rate-limit handling.
- Token expiration.
- Token revocation.
- API errors.

### 20.3 Publishing reliability tests

| Test | Expected outcome |
|---|---|
| Valid publication | Post is created and recorded |
| Invalid content | Validation error; no publication attempt |
| Missing permission | Clear authorization error |
| Expired token | Refresh or reauthorization |
| HTTP 429 | Respect retry guidance |
| Network timeout | Record uncertain outcome |
| Duplicate execution | Prevent duplicate publication where safely possible |
| One platform fails | Other destination results remain intact |
| Application restart | Queued jobs recover |
| Media upload failure | No false publication success |
| Account disconnected | New jobs blocked |

### 20.4 Contract tests

Each adapter must have:

- Request schema tests.
- Response schema tests.
- API version tests.
- Permission mapping tests.
- Error response tests.
- Capability tests.
- Mocked platform responses.

Mock tests must not be presented as proof of live platform access.

### 20.5 Live API tests

Use approved test accounts and real platform applications.

Live tests should verify:

- Authorization.
- Publishing.
- Media processing.
- Returned identifiers.
- Account eligibility.
- Real API errors.
- Token lifecycle.

Do not publish test content to unrelated users or production audiences without explicit authorization.

---

## 21. Release-Blocking Acceptance Criteria

A platform integration cannot be marked production-ready until all applicable checks pass.

| ID | Acceptance criterion |
|---|---|
| API-001 | Official API documentation reviewed |
| API-002 | Current API version confirmed |
| API-003 | Required developer application access approved |
| API-004 | OAuth flow works |
| API-005 | State and callback validation work |
| API-006 | Tokens are stored securely |
| API-007 | Required scopes are validated |
| API-008 | Account eligibility is verified |
| API-009 | Supported content types are validated |
| API-010 | Media upload workflow is verified |
| API-011 | Publishing response is handled correctly |
| API-012 | Remote post identifier is persisted |
| API-013 | Rate limits are handled |
| API-014 | Token expiration and revocation are handled |
| API-015 | Unknown publishing outcomes are reconciled |
| API-016 | Duplicate execution is prevented |
| API-017 | API usage and costs are tracked where applicable |
| API-018 | Platform terms and commercial restrictions are reviewed |
| API-019 | Logs do not expose credentials |
| API-020 | Live integration tests pass |
| API-021 | User-facing limitations are documented |
| API-022 | Account disconnection and credential deletion work |

### 21.1 Release statuses

Use the following integration statuses:

- `NOT_STARTED`
- `RESEARCHED`
- `ACCESS_REQUESTED`
- `ACCESS_APPROVED`
- `IN_DEVELOPMENT`
- `INTEGRATION_TESTED`
- `PRODUCTION_READY`
- `RESTRICTED`
- `DEFERRED`
- `DISABLED`

Do not mark an integration `PRODUCTION_READY` based only on successful mock tests.

---

## 22. Platform Decision Register

| Platform | Decision | Reason |
|---|---|---|
| LinkedIn | Build first | Core professional publishing workflow; access approval must be secured |
| Facebook Pages | Build early | Useful Meta integration for business publishing |
| Instagram | Build early | Important creator and business workflow; media delivery must be solved |
| Threads | Build after Meta foundation | Separate API and publishing workflow |
| Pinterest | Build after initial integrations | Requires access-tier progression |
| X | Optional expansion | Consumption-based pricing requires cost controls |
| Reddit | Defer | Commercial-use permission and contractual dependency |

### 22.1 What should be built before platform-specific integrations?

The following foundational components should be completed first:

1. Integration registry.
2. OAuth state manager.
3. Credential storage.
4. Token lifecycle manager.
5. Platform capability registry.
6. Media preparation service.
7. Publishing orchestrator.
8. Persistent job queue.
9. Idempotency system.
10. Attempt history.
11. Error classification.
12. Platform API usage tracking.

This avoids building seven disconnected publishing implementations.

---

## 23. Operational Monitoring and Documentation Maintenance

Platform APIs change frequently.

PostFlow needs a formal maintenance process.

### 23.1 Monitoring targets

Track:

- API version announcements.
- Deprecated endpoints.
- Permission changes.
- OAuth changes.
- Rate-limit changes.
- Media format changes.
- Publishing restrictions.
- Application review requirements.
- Commercial terms.
- API pricing.
- Security advisories.

### 23.2 Review cadence

| Item | Review frequency |
|---|---|
| API version and deprecations | Monthly |
| Permissions and OAuth scopes | Monthly |
| Pricing and rate limits | Monthly |
| Developer terms | Quarterly |
| Media requirements | Before each platform release |
| Security advisories | As announced |
| Production compatibility | Every release |

### 23.3 Documentation ownership

Each adapter should have an internal integration record containing:

```text
Platform:
API version:
Documentation URL:
Developer application ID:
Application status:
Approval tier:
OAuth scopes:
Account eligibility:
Supported content types:
Media workflow:
Rate limits:
Pricing:
Known restrictions:
Last verified:
Next review:
```

Do not store confidential application secrets in this document.

---

## 24. Final Recommendations

### Recommendation 1 - Do not build all integrations simultaneously

Start with the platform foundation and one approved integration.

A working publishing pipeline is more valuable than seven incomplete adapters.

### Recommendation 2 - Validate access before implementation

LinkedIn and Meta approval requirements can become significant project dependencies.

Obtain real developer access as early as possible.

### Recommendation 3 - Treat Instagram media hosting as an architectural requirement

The local-first media library and external platform publishing workflow must be connected through an explicit, secure media-delivery design.

### Recommendation 4 - Keep the scheduler independent of platform scheduling

PostFlow should own the scheduling workflow initially.

Each platform adapter should execute a publication operation when the local scheduler triggers it.

### Recommendation 5 - Make capabilities account-specific

A platform connection does not guarantee support for all formats or account types.

The UI must display actual supported operations.

### Recommendation 6 - Build robust publishing recovery

Idempotency, reconciliation and per-destination execution are mandatory.

Do not retry an unknown publishing outcome blindly.

### Recommendation 7 - Treat X as a cost-sensitive integration

Consumption-based pricing must be visible to users and included in product economics.

### Recommendation 8 - Keep Reddit deferred

Do not expose commercial Reddit integration until explicit permission and contractual requirements are satisfied.

### Recommendation 9 - Do not embed OAuth secrets in the desktop application

Use supported public-client flows or a controlled backend OAuth broker where confidential client authentication is required.

### Recommendation 10 - Keep manual publishing as a supported fallback

An unsupported API operation should not prevent the user from preparing content for that platform.

Manual publishing assistance is a legitimate product capability, not a failed automatic integration.

---

## 25. Final Technical Assessment

| Dimension | Assessment |
|---|---|
| Overall API feasibility | Moderate |
| LinkedIn feasibility | Approval-dependent |
| Facebook Pages feasibility | Permission and review-dependent |
| Instagram feasibility | Account and media-delivery-dependent |
| Threads feasibility | API and authorization verification required |
| Pinterest feasibility | Access-tier-dependent |
| X feasibility | Cost-dependent |
| Reddit feasibility | Commercial permission required |
| OAuth architecture | Feasible with public-client and broker considerations |
| Media infrastructure | Requires explicit design |
| Publishing orchestration | Feasible |
| Production reliability | Requires reconciliation and idempotency |
| Maintenance burden | High |
| Recommended approach | Incremental adapter-based implementation |

### Final decision

**Proceed with the PostFlow platform integration architecture, but gate each production integration on actual API approval and live verification.**

The recommended sequence is:

1. Build the integration framework.
2. Validate LinkedIn access.
3. Implement Facebook Pages and Instagram.
4. Add Threads.
5. Add Pinterest.
6. Add X with cost controls.
7. Reconsider Reddit only after commercial authorization.

The primary engineering objective is not maximum platform count.

It is **reliable, authorized and recoverable publishing across the platforms PostFlow can genuinely support.**

---

## 26. Official Reference Directory

### LinkedIn

- [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [Community Management Overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview)
- [Community Management Migration Guide](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide)

### Meta - Facebook

- [Meta Developers](https://developers.facebook.com/)
- [Pages API](https://developers.facebook.com/documentation/pages-api/)
- [Pages API Posts](https://developers.facebook.com/documentation/pages-api/posts)
- [Graph API](https://developers.facebook.com/docs/graph-api/)
- [Permissions Reference](https://developers.facebook.com/docs/permissions/)

### Meta - Instagram

- [Instagram Platform](https://developers.facebook.com/docs/instagram-platform/)
- [Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/)

### Threads

- [Threads API](https://developers.facebook.com/docs/threads/)
- [Threads Posts](https://developers.facebook.com/docs/threads/posts/)

### Pinterest

- [Pinterest Developers](https://developers.pinterest.com/)
- [API v5](https://developers.pinterest.com/docs/api/v5/)
- [Access Tiers](https://developers.pinterest.com/docs/key-concepts/access-tiers/)
- [Create Boards and Pins](https://developers.pinterest.com/docs/work-with-organic-content-and-users/create-boards-and-pins/)
- [Authentication](https://developers.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/)
- [Rate Limits](https://developers.pinterest.com/docs/reference/rate-limits/)

### X

- [X Developer Platform](https://developer.x.com/)
- [X API Documentation](https://developer.x.com/en/docs)
- [X API v2 Reference](https://developer.x.com/en/docs/api-reference-index)
- [X Developer Console](https://console.x.com/)

### Reddit

- [Reddit Developer Platform](https://developers.reddit.com/)
- [Reddit Data API Wiki](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)
- [Developer Platform and Commercial Use](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data)
- [Reddit Data API Terms](https://redditinc.com/policies/data-api-terms)

---

**Document owner:** PostFlow Product and Engineering  
**Review frequency:** Monthly for API compatibility and quarterly for policy and commercial terms  
**Next review:** 8 December 2026  
**Related documents:** `PRODUCT_VISION.md`, `PRD.md`, `USER_STORIES.md`, `ACCEPTANCE_CRITERIA.md`, `TEST_PLAN.md`, `TRACEABILITY_MATRIX.md`, `MARKET_RESEARCH.md`, `ARCHITECTURE.md`, `API_SPECIFICATION.md`, `SECURITY.md`
