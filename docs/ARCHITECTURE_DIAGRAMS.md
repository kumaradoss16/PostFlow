# PostFlow - Architecture Diagrams

**File:** `docs/ARCHITECTURE_DIAGRAMS.md`  
**Version:** 1.0  
**Status:** Proposed Architecture  
**Architecture Style:** Modular Monolith  
**Desktop Platform:** Windows  
**Future Platform:** SaaS

---

## 1. System Context Diagram

Shows PostFlow's relationship with the user, desktop environment, AI providers, social platforms, and external infrastructure.

```mermaid
flowchart TB
    USER["User / Content Creator"]

    subgraph POSTFLOW["PostFlow Application"]
        DESKTOP["Desktop Application"]
        AI["AI Content Intelligence"]
        CONTENT["Content Management"]
        MEDIA["Media Management"]
        PUBLISH["Publishing and Scheduling"]
        ANALYTICS["Analytics"]
    end

    subgraph AI_PROVIDERS["External AI Providers"]
        OPENAI["OpenAI"]
        GEMINI["Google Gemini"]
        CLAUDE["Anthropic Claude"]
        PERPLEXITY["Perplexity"]
    end

    subgraph SOCIAL["Social Media Platforms"]
        INSTAGRAM["Instagram"]
        FACEBOOK["Facebook Pages"]
        LINKEDIN["LinkedIn"]
        THREADS["Threads"]
        X["X"]
        PINTEREST["Pinterest"]
        REDDIT["Reddit"]
    end

    STORAGE["Local Database and Media Storage"]
    SECURE["Operating System Secure Storage"]

    USER --> DESKTOP
    DESKTOP --> AI
    DESKTOP --> CONTENT
    DESKTOP --> MEDIA
    DESKTOP --> PUBLISH
    DESKTOP --> ANALYTICS

    AI --> OPENAI
    AI --> GEMINI
    AI --> CLAUDE
    AI --> PERPLEXITY

    PUBLISH --> INSTAGRAM
    PUBLISH --> FACEBOOK
    PUBLISH --> LINKEDIN
    PUBLISH --> THREADS
    PUBLISH --> X
    PUBLISH --> PINTEREST
    PUBLISH --> REDDIT

    DESKTOP --> STORAGE
    DESKTOP --> SECURE
```

**Boundary:** PostFlow owns application logic, content records, scheduling, and local state. External providers own their APIs, account permissions, publication infrastructure, and platform-reported analytics.

---

## 2. High-Level Application Architecture

Shows the primary application layers and their dependency direction.

```mermaid
flowchart TB
    USER["User"]

    subgraph PRESENTATION["Presentation Layer"]
        TAURI["Tauri 2"]
        REACT["React + TypeScript"]
        UI["Feature Modules and UI Components"]
    end

    subgraph APPLICATION["Application Layer"]
        API["FastAPI REST API"]
        SERVICES["Application Services"]
        COMMANDS["Use Cases and Commands"]
    end

    subgraph DOMAIN["Domain Layer"]
        ENTITIES["Domain Entities"]
        RULES["Business Rules"]
        STATES["State Machines"]
        INTERFACES["Domain Contracts"]
    end

    subgraph INFRASTRUCTURE["Infrastructure Layer"]
        REPOSITORIES["Repository Implementations"]
        DATABASE["SQLite"]
        FILES["Filesystem Storage"]
        SECRETS["OS Secure Storage"]
        WORKER["Background Worker"]
    end

    subgraph INTEGRATIONS["Integration Layer"]
        AI_ADAPTERS["AI Provider Adapters"]
        SOCIAL_ADAPTERS["Social Platform Adapters"]
        MEDIA_ADAPTERS["Media Processing Adapters"]
    end

    USER --> TAURI
    TAURI --> REACT
    REACT --> UI
    UI --> API
    API --> SERVICES
    SERVICES --> COMMANDS
    COMMANDS --> RULES
    RULES --> ENTITIES
    RULES --> STATES
    SERVICES --> INTERFACES

    REPOSITORIES -.-> INTERFACES
    REPOSITORIES --> DATABASE
    FILES --> INFRASTRUCTURE
    SECRETS --> INFRASTRUCTURE
    WORKER --> SERVICES

    SERVICES --> AI_ADAPTERS
    SERVICES --> SOCIAL_ADAPTERS
    SERVICES --> MEDIA_ADAPTERS
```

**Design rule:** Domain logic must not depend on React, FastAPI, SQLAlchemy, provider SDKs, or social platform SDKs. Infrastructure implements the interfaces required by application services.

---

## 3. Desktop Container Architecture

Shows the runtime processes and their communication boundaries.

```mermaid
flowchart TB
    subgraph MACHINE["User's Windows Machine"]
        subgraph DESKTOP["PostFlow Desktop Runtime"]
            TAURI["Tauri Shell"]
            FRONTEND["React Frontend"]
        end

        subgraph BACKEND["Python Backend Runtime"]
            API["FastAPI Process"]
            APP["Application Services"]
            DOMAIN["Domain Services"]
        end

        subgraph EXECUTION["Background Execution"]
            WORKER["Publishing Worker"]
            SCHEDULER["Scheduler"]
            RECOVERY["Recovery and Reconciliation"]
        end

        subgraph LOCALDATA["Local Data"]
            SQLITE[("SQLite Database")]
            MEDIA[("Media Files")]
            LOGS[("Application Logs")]
        end

        subgraph CREDENTIALS["Secure Storage"]
            VAULT["Windows Credential Manager / DPAPI-backed Store"]
        end
    end

    FRONTEND -->|"HTTP / JSON"| API
    TAURI -->|"Lifecycle and Native IPC"| FRONTEND

    API --> APP
    APP --> DOMAIN

    WORKER --> APP
    SCHEDULER --> WORKER
    RECOVERY --> WORKER

    APP --> SQLITE
    WORKER --> SQLITE
    APP --> MEDIA
    APP --> VAULT
    API --> LOGS
```

### Runtime responsibilities

| Runtime | Responsibility |
|---|---|
| Tauri | Desktop lifecycle and native capabilities |
| React | User interface and interaction |
| FastAPI | Local API and request orchestration |
| Application services | Business use cases |
| Worker | Persistent background execution |
| Scheduler | Due-job discovery |
| Recovery | Interrupted-job recovery |
| SQLite | Structured application data |
| Filesystem | Media and generated assets |
| Secure storage | API keys and OAuth credentials |

**Deployment constraint:** Start with one controlled worker and bounded concurrency. Do not introduce distributed workers into the desktop MVP.

---

## 4. Backend Module Architecture

Shows the modular monolith's bounded business modules.

```mermaid
flowchart TB
    API["FastAPI API Router"]

    subgraph CORE["Core Application Modules"]
        WORKSPACE["Workspace Service"]
        BRAND["Brand Service"]
        CONTENT["Content Service"]
        VARIANT["Platform Variant Service"]
        APPROVAL["Approval Service"]
    end

    subgraph AI["AI Modules"]
        PROVIDER["AI Provider Management"]
        ORCHESTRATOR["AI Orchestrator"]
        CAPABILITY["Capability Registry"]
    end

    subgraph PUBLISHING["Publishing Modules"]
        ACCOUNT["Social Account Service"]
        PLATFORM["Platform Capability Service"]
        PUBLISH["Publishing Service"]
        SCHEDULE["Scheduling Service"]
        ANALYTICS["Analytics Service"]
    end

    subgraph SUPPORT["Supporting Modules"]
        MEDIA["Media Service"]
        AUDIT["Audit Service"]
        SECURITY["Security Service"]
    end

    subgraph INFRA["Infrastructure"]
        REPOSITORY["Repositories"]
        DB[("SQLite")]
        FILES[("Filesystem")]
        SECRET["Secure Credential Store"]
    end

    API --> WORKSPACE
    API --> BRAND
    API --> CONTENT
    API --> VARIANT
    API --> APPROVAL
    API --> ORCHESTRATOR
    API --> ACCOUNT
    API --> PUBLISH
    API --> SCHEDULE
    API --> ANALYTICS
    API --> MEDIA

    CONTENT --> BRAND
    VARIANT --> CONTENT
    VARIANT --> MEDIA
    APPROVAL --> VARIANT
    PUBLISH --> APPROVAL
    PUBLISH --> ACCOUNT
    PUBLISH --> PLATFORM
    SCHEDULE --> PUBLISH

    ORCHESTRATOR --> PROVIDER
    ORCHESTRATOR --> CAPABILITY
    ACCOUNT --> SECURITY
    SECURITY --> SECRET

    WORKSPACE --> REPOSITORY
    BRAND --> REPOSITORY
    CONTENT --> REPOSITORY
    VARIANT --> REPOSITORY
    APPROVAL --> REPOSITORY
    PUBLISH --> REPOSITORY
    SCHEDULE --> REPOSITORY
    ANALYTICS --> REPOSITORY
    AUDIT --> REPOSITORY

    REPOSITORY --> DB
    MEDIA --> FILES
```

### Module ownership

| Module | Primary ownership |
|---|---|
| Workspace | Workspace identity and boundaries |
| Brand | Brand voice and guidelines |
| Content | Source content and revisions |
| Variant | Independent platform content |
| AI Provider | Provider configuration |
| AI Orchestrator | AI request coordination |
| Media | Asset processing and storage |
| Social Account | OAuth and account metadata |
| Approval | Revision-bound approval |
| Publishing | Destination-specific publication |
| Scheduling | Persistent scheduled execution |
| Analytics | Platform metrics |
| Audit | Activity and security events |
| Security | Credential and request protection |

---

## 5. AI Integration Architecture

Shows the provider-independent AI orchestration boundary.

```mermaid
flowchart TB
    UI["AI Studio UI"]
    API["AI Generation API"]
    SERVICE["Content Generation Service"]
    CONTEXT["Brand and Content Context Builder"]
    ORCHESTRATOR["AI Orchestrator"]

    REGISTRY["Provider Registry"]
    CAPABILITY["Capability Registry"]
    USAGE["Usage and Cost Tracking"]
    RESULTS["Generation Result Persistence"]

    subgraph PROVIDERS["Provider Adapters"]
        OPENAI["OpenAI Adapter"]
        GEMINI["Gemini Adapter"]
        ANTHROPIC["Claude Adapter"]
        PERPLEXITY["Perplexity Adapter"]
    end

    subgraph EXTERNAL["External APIs"]
        OAPI["OpenAI API"]
        GAPI["Gemini API"]
        AAPI["Anthropic API"]
        PAPI["Perplexity API"]
    end

    UI --> API
    API --> SERVICE
    SERVICE --> CONTEXT
    CONTEXT --> ORCHESTRATOR

    ORCHESTRATOR --> REGISTRY
    ORCHESTRATOR --> CAPABILITY

    ORCHESTRATOR --> OPENAI
    ORCHESTRATOR --> GEMINI
    ORCHESTRATOR --> ANTHROPIC
    ORCHESTRATOR --> PERPLEXITY

    OPENAI --> OAPI
    GEMINI --> GAPI
    ANTHROPIC --> AAPI
    PERPLEXITY --> PAPI

    ORCHESTRATOR --> USAGE
    ORCHESTRATOR --> RESULTS
```

### AI request lifecycle

1. User selects an operation.
2. Backend validates the request.
3. Brand context is assembled using minimum necessary data.
4. Orchestrator selects a configured provider and model.
5. Capability registry checks feature support.
6. Adapter executes the provider request.
7. Response is normalized and validated.
8. Usage metadata is collected where available.
9. Result is persisted.
10. UI receives the result.

**Security boundary:** No silent provider fallback. Additional provider transmission requires user authorization.

---

## 6. Social Platform Integration Architecture

Shows the independent adapter model for publishing.

```mermaid
flowchart TB
    UI["Composer / Publishing UI"]
    API["Publishing API"]
    SERVICE["Publishing Application Service"]

    VALIDATOR["Content and Permission Validator"]
    REGISTRY["Platform Adapter Registry"]
    JOBS[("Publishing Jobs")]

    subgraph ADAPTERS["Platform Adapters"]
        IG["Instagram"]
        FB["Facebook Pages"]
        LI["LinkedIn"]
        TH["Threads"]
        X["X"]
        PIN["Pinterest"]
        RED["Reddit"]
    end

    subgraph PLATFORMS["External Platform APIs"]
        META["Meta APIs"]
        LINKEDIN["LinkedIn API"]
        THREADS["Threads API"]
        XAPI["X API"]
        PINAPI["Pinterest API"]
        REDAPI["Reddit API"]
    end

    UI --> API
    API --> SERVICE
    SERVICE --> VALIDATOR
    VALIDATOR --> REGISTRY
    SERVICE --> JOBS

    REGISTRY --> IG
    REGISTRY --> FB
    REGISTRY --> LI
    REGISTRY --> TH
    REGISTRY --> X
    REGISTRY --> PIN
    REGISTRY --> RED

    IG --> META
    FB --> META
    LI --> LINKEDIN
    TH --> THREADS
    X --> XAPI
    PIN --> PINAPI
    RED --> REDAPI
```

### Adapter isolation rules

- Each destination gets an independent publishing job.
- Each adapter owns its platform-specific payload.
- Each adapter owns its authorization and API errors.
- Each adapter reports supported capabilities.
- One destination's failure must not erase another destination's result.
- Platform API restrictions must be validated before release.

---

## 7. Content Creation and Adaptation Data Flow

```mermaid
flowchart TD
    USER["User"]
    BRAND["Select Brand"]
    SOURCE["Create Source Content"]
    AI["AI Generation"]
    REVIEW["Review Generated Content"]
    DEST["Select Destinations"]
    ADAPT["Platform Adaptation"]
    VARIANTS["Create Independent Variants"]
    VALIDATE["Validate Platform Constraints"]
    EDIT["Edit Variants"]
    APPROVE["Approve Exact Revisions"]
    SAVE["Persist Approved Content"]

    USER --> BRAND
    BRAND --> SOURCE
    SOURCE --> AI
    AI --> REVIEW
    REVIEW --> DEST
    DEST --> ADAPT
    ADAPT --> VARIANTS
    VARIANTS --> VALIDATE
    VALIDATE --> EDIT
    EDIT --> APPROVE
    APPROVE --> SAVE
```

### Data ownership rules

- Source content is independent of platform variants.
- Each variant has its own revision history.
- Editing one variant does not modify other variants.
- Approval belongs to an exact revision.
- Editing an approved revision invalidates its approval.

---

## 8. Media Processing Architecture

```mermaid
flowchart TD
    UPLOAD["Select Media"]
    VALIDATE["Validate File Signature, Format and Size"]
    ORIGINAL["Store Original Asset"]
    METADATA["Extract Metadata"]
    TYPE{"Media Type"}

    IMAGE["Image Processing"]
    VIDEO["Video Processing"]
    THUMB["Generate Thumbnail"]
    STORE["Store Processed Asset"]
    DB["Persist Asset Metadata"]
    READY["Asset Ready"]

    UPLOAD --> VALIDATE
    VALIDATE --> ORIGINAL
    ORIGINAL --> METADATA
    METADATA --> TYPE

    TYPE -->|"Image"| IMAGE
    TYPE -->|"Video"| VIDEO

    IMAGE --> THUMB
    VIDEO --> THUMB
    THUMB --> STORE
    STORE --> DB
    DB --> READY
```

### Media storage boundary

```text
PostFlowData/
├── database/
│   └── postflow.db
├── media/
│   ├── originals/
│   ├── processed/
│   ├── thumbnails/
│   └── temporary/
├── logs/
├── cache/
└── exports/
```

Media binaries belong to the filesystem. SQLite stores metadata, ownership, file references, and transformation history.

---

## 9. Database Entity Relationship Diagram

This is the logical relationship model. It is not a substitute for validating the final physical database schema and migration files.

```mermaid
erDiagram
    WORKSPACES ||--o{ BRANDS : contains
    WORKSPACES ||--o{ CONTENT_ITEMS : owns
    WORKSPACES ||--o{ SOCIAL_ACCOUNTS : manages

    BRANDS ||--o{ CONTENT_ITEMS : informs

    CONTENT_ITEMS ||--o{ CONTENT_REVISIONS : has
    CONTENT_ITEMS ||--o{ POST_VARIANTS : produces

    POST_VARIANTS ||--o{ VARIANT_REVISIONS : has
    POST_VARIANTS ||--o{ APPROVALS : requires
    POST_VARIANTS ||--o{ PUBLISH_JOBS : creates

    SOCIAL_ACCOUNTS ||--o{ PUBLISH_JOBS : receives

    PUBLISH_JOBS ||--o{ PUBLISH_ATTEMPTS : records
    PUBLISH_JOBS ||--o| PUBLISHED_POSTS : confirms

    MEDIA_ASSETS }o--o{ POST_VARIANTS : attaches

    CAMPAIGNS ||--o{ CONTENT_ITEMS : groups
    WORKSPACES ||--o{ CAMPAIGNS : owns

    WORKSPACES {
        uuid id PK
        string name
        datetime created_at
    }

    BRANDS {
        uuid id PK
        uuid workspace_id FK
        string name
        json brand_guidelines
    }

    CONTENT_ITEMS {
        uuid id PK
        uuid workspace_id FK
        uuid brand_id FK
        string title
        text source_content
        datetime created_at
    }

    CONTENT_REVISIONS {
        uuid id PK
        uuid content_id FK
        integer revision
        text content_snapshot
        datetime created_at
    }

    POST_VARIANTS {
        uuid id PK
        uuid content_id FK
        string platform
        integer current_revision
        string status
    }

    VARIANT_REVISIONS {
        uuid id PK
        uuid variant_id FK
        integer revision
        json content_payload
    }

    SOCIAL_ACCOUNTS {
        uuid id PK
        uuid workspace_id FK
        string platform
        string external_account_id
        string credential_reference
    }

    MEDIA_ASSETS {
        uuid id PK
        string storage_path
        string media_type
        integer file_size
    }

    APPROVALS {
        uuid id PK
        uuid variant_id FK
        integer approved_revision
        string status
        datetime approved_at
    }

    PUBLISH_JOBS {
        uuid id PK
        uuid variant_id FK
        uuid account_id FK
        string status
        datetime scheduled_at
        string idempotency_key
    }

    PUBLISH_ATTEMPTS {
        uuid id PK
        uuid job_id FK
        integer attempt_number
        string status
        string error_code
    }

    PUBLISHED_POSTS {
        uuid id PK
        uuid job_id FK
        string external_post_id
        datetime published_at
    }

    CAMPAIGNS {
        uuid id PK
        uuid workspace_id FK
        string name
    }
```

**Important:** Credential references in this diagram are identifiers pointing to OS-backed secure storage. Raw tokens must not be stored in these database records.

---

## 10. Publishing Job State Machine

```mermaid
stateDiagram-v2
    [*] --> Draft

    Draft --> AwaitingApproval
    AwaitingApproval --> Approved
    AwaitingApproval --> Rejected

    Approved --> Queued
    Approved --> Scheduled

    Scheduled --> Queued
    Scheduled --> Cancelled

    Queued --> Publishing
    Queued --> Cancelled

    Publishing --> Published
    Publishing --> Failed
    Publishing --> UnknownOutcome

    Failed --> RetryPending
    RetryPending --> Queued

    UnknownOutcome --> Reconciliation

    Reconciliation --> Published
    Reconciliation --> RetryPending
    Reconciliation --> Failed
```

### State transition requirements

| Transition | Requirement |
|---|---|
| Draft → AwaitingApproval | Content ready for review |
| AwaitingApproval → Approved | Authorized approval |
| Approved → Scheduled | Valid schedule |
| Approved → Queued | Immediate publishing request |
| Queued → Publishing | Worker successfully claims job |
| Publishing → Published | Confirmed external publication |
| Publishing → Failed | Confirmed permanent or exhausted failure |
| Publishing → UnknownOutcome | External outcome uncertain |
| UnknownOutcome → Reconciliation | Reconciliation process initiated |
| Reconciliation → Published | Publication confirmed |
| Reconciliation → RetryPending | Safe retry established |
| Queued → Cancelled | Cancellation wins before execution |

Approval state and publishing job state should be persisted separately even though they are shown together here for conceptual readability.

---

## 11. Scheduled Publishing Execution

```mermaid
sequenceDiagram
    actor User
    participant UI as React
    participant API as FastAPI
    participant SVC as Scheduling Service
    participant DB as SQLite
    participant WORKER as Background Worker
    participant PUB as Publishing Service
    participant PLATFORM as Platform Adapter
    participant EXT as Social Platform

    User->>UI: Schedule post
    UI->>API: Create schedule
    API->>SVC: Validate schedule
    SVC->>DB: Persist scheduled job
    DB-->>SVC: Job committed
    SVC-->>UI: Schedule confirmed

    WORKER->>DB: Find due jobs
    DB-->>WORKER: Due job IDs
    WORKER->>DB: Atomically claim job
    DB-->>WORKER: Claim confirmed

    WORKER->>PUB: Execute job
    PUB->>PUB: Revalidate approval and account
    PUB->>PLATFORM: Publish request
    PLATFORM->>EXT: External API call
    EXT-->>PLATFORM: Publication response
    PLATFORM-->>PUB: Normalized result

    PUB->>DB: Persist attempt and outcome
    DB-->>PUB: Commit
```

### Worker recovery

```mermaid
flowchart TD
    START["Worker Starts"]
    SCAN["Find Expired Claims and Interrupted Jobs"]
    CLASSIFY["Classify Last Execution State"]
    SAFE{"Is Retry Safe?"}
    RECON["Reconcile External Outcome"]
    RETRY["Return Eligible Job to Queue"]
    UNKNOWN["Mark Unknown Outcome"]
    COMPLETE["Mark Confirmed Publication"]
    FAIL["Mark Permanent Failure"]
    NORMAL["Process Normal Due Jobs"]

    START --> SCAN
    SCAN --> CLASSIFY
    CLASSIFY --> SAFE

    SAFE -->|"Yes"| RETRY
    SAFE -->|"No"| RECON

    RECON -->|"Published"| COMPLETE
    RECON -->|"Not Published and Retry Safe"| RETRY
    RECON -->|"Uncertain"| UNKNOWN
    RECON -->|"Permanent Failure"| FAIL

    RETRY --> NORMAL
    COMPLETE --> NORMAL
    UNKNOWN --> NORMAL
    FAIL --> NORMAL
```

A network timeout is not evidence that publication failed. Unknown outcomes must be reconciled before retrying.

---

## 12. OAuth and Credential Security Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as React UI
    participant API as FastAPI
    participant OAUTH as OAuth Service
    participant PLATFORM as Social Platform
    participant VAULT as OS Secure Storage
    participant DB as SQLite

    User->>UI: Connect account
    UI->>API: Start OAuth connection
    API->>OAUTH: Create authorization request
    OAUTH-->>UI: Authorization URL and state
    UI->>PLATFORM: Open authorization
    PLATFORM-->>API: OAuth callback
    API->>OAUTH: Validate state and callback
    OAUTH->>PLATFORM: Exchange authorization code
    PLATFORM-->>OAUTH: Access and refresh credentials
    OAUTH->>VAULT: Store credentials
    OAUTH->>DB: Store account metadata and credential reference
    DB-->>OAUTH: Commit
    OAUTH-->>UI: Connection status
```

### Credential boundaries

```mermaid
flowchart LR
    UI["Frontend"]
    API["Local API"]
    SERVICE["Credential Service"]
    DB[("SQLite")]
    VAULT["OS Secure Storage"]
    EXT["External Provider"]

    UI -->|"Credential reference/status only"| API
    API --> SERVICE
    SERVICE --> DB
    SERVICE --> VAULT
    SERVICE -->|"Authorized external request"| EXT

    VAULT -.->|"Never expose raw token to UI"| UI
```

The dashed relationship represents a prohibited data path, not an actual communication channel.

---

## 13. Deployment Architecture - Desktop

```mermaid
flowchart TB
    subgraph WINDOWS["Windows Desktop Environment"]
        USER["User"]

        subgraph INSTALL["Installed PostFlow Application"]
            TAURI["Tauri Shell"]
            FRONTEND["React Production Build"]
            BACKEND["Packaged FastAPI Runtime"]
            WORKER["Background Worker"]
        end

        subgraph APPDATA["Application Data Directory"]
            DB[("SQLite Database")]
            MEDIA[("Media Assets")]
            BACKUP[("Backups")]
            LOGS[("Logs")]
        end

        VAULT["Windows Credential Manager / DPAPI-backed Storage"]
    end

    subgraph CLOUD["External Services"]
        AI["AI Provider APIs"]
        SOCIAL["Social Platform APIs"]
    end

    USER --> TAURI
    TAURI --> FRONTEND
    FRONTEND -->|"Loopback API"| BACKEND
    BACKEND --> WORKER
    BACKEND --> DB
    WORKER --> DB
    BACKEND --> MEDIA
    BACKEND --> VAULT
    BACKEND --> AI
    WORKER --> SOCIAL
    DB --> BACKUP
    BACKEND --> LOGS
```

### Desktop runtime rules

- API binds to `127.0.0.1`.
- Backend authentication is required.
- User data remains outside the installation directory.
- The worker must persist and recover jobs.
- Secrets use OS-backed storage.
- Media processing is bounded.
- Application shutdown must be controlled.
- Desktop scheduled execution requires the computer and worker to remain available.

---

## 14. Deployment Architecture - Future SaaS

```mermaid
flowchart TB
    USER["Web / Desktop Clients"]
    EDGE["HTTPS Gateway"]
    AUTH["Authentication and Authorization"]

    subgraph APPLICATION["Application Platform"]
        API["FastAPI Application"]
        DOMAIN["Application and Domain Services"]
        AI["AI Orchestrator"]
        SOCIAL["Social Integration Services"]
    end

    subgraph WORKERS["Background Infrastructure"]
        QUEUE["Redis / Durable Queue"]
        SCHEDULER["Central Scheduler"]
        WORKER["Distributed Workers"]
    end

    subgraph DATA["Data Infrastructure"]
        POSTGRES[("PostgreSQL")]
        OBJECT[("Object Storage")]
        SECRET["Managed Secret Store"]
    end

    subgraph OBSERVABILITY["Observability"]
        LOG["Centralized Logs"]
        METRICS["Metrics"]
        ALERT["Alerts"]
    end

    AI_EXT["AI Providers"]
    SOCIAL_EXT["Social Platforms"]

    USER --> EDGE
    EDGE --> AUTH
    AUTH --> API
    API --> DOMAIN
    DOMAIN --> POSTGRES
    DOMAIN --> QUEUE
    QUEUE --> WORKER
    SCHEDULER --> QUEUE
    WORKER --> POSTGRES
    WORKER --> OBJECT

    DOMAIN --> AI
    DOMAIN --> SOCIAL
    AI --> AI_EXT
    SOCIAL --> SOCIAL_EXT

    API --> SECRET
    API --> LOG
    WORKER --> LOG
    API --> METRICS
    WORKER --> METRICS
    METRICS --> ALERT
```

### SaaS evolution

| Desktop | SaaS |
|---|---|
| SQLite | PostgreSQL |
| Local filesystem | Object storage |
| Local scheduler | Central scheduler |
| Single worker | Distributed workers |
| OS secure storage | Managed secrets and encrypted credentials |
| Local workspace | Tenant-isolated workspace |
| Local logs | Centralized observability |

The SaaS deployment must introduce tenant isolation, role-based access control, rate limits, usage metering, centralized backups, and secure credential isolation.

---

## 15. Security Trust Boundary Diagram

```mermaid
flowchart TB
    subgraph TRUST1["Trust Boundary 1 - Desktop Presentation"]
        UI["React Frontend"]
        TAURI["Tauri Runtime"]
    end

    subgraph TRUST2["Trust Boundary 2 - Local Application"]
        API["Authenticated Local API"]
        DOMAIN["Application and Domain Services"]
        WORKER["Background Worker"]
    end

    subgraph TRUST3["Trust Boundary 3 - Local Data"]
        DB[("SQLite")]
        FILES[("Media Files")]
        VAULT["OS Secure Storage"]
    end

    subgraph TRUST4["Trust Boundary 4 - External Providers"]
        AI["AI APIs"]
        SOCIAL["Social APIs"]
    end

    UI --> TAURI
    TAURI -->|"Authenticated local communication"| API
    API --> DOMAIN
    DOMAIN --> WORKER

    DOMAIN --> DB
    DOMAIN --> FILES
    DOMAIN --> VAULT

    DOMAIN -->|"Minimum necessary disclosed data"| AI
    WORKER -->|"Authorized publishing requests"| SOCIAL
```

### Security controls by boundary

| Boundary | Required controls |
|---|---|
| Frontend → Local API | Authentication, origin restrictions, input validation |
| Local API → Domain | Authorization and business rule enforcement |
| Domain → Database | Transactions, scoped queries and constraints |
| Domain → Secure storage | Credential references and OS protection |
| Domain → AI providers | Data disclosure, minimum necessary context |
| Worker → Social platforms | OAuth protection, permission checks, idempotency |
| Media ingestion | File validation, path controls, bounded processing |

---

## 16. Component Dependency Diagram

```mermaid
flowchart TD
    PRESENTATION["Presentation Components"]
    API["API Controllers"]
    APPLICATION["Application Services"]
    DOMAIN["Domain Models and Policies"]

    PORTS["Repository and Integration Interfaces"]

    DB["SQLite Repository"]
    FILE["Filesystem Adapter"]
    SECRET["Secure Storage Adapter"]
    AI["AI Provider Adapters"]
    SOCIAL["Social Platform Adapters"]

    PRESENTATION --> API
    API --> APPLICATION
    APPLICATION --> DOMAIN
    APPLICATION --> PORTS

    DB -.-> PORTS
    FILE -.-> PORTS
    SECRET -.-> PORTS
    AI -.-> PORTS
    SOCIAL -.-> PORTS
```

### Dependency rules

1. Frontend depends on API contracts.
2. API controllers depend on application services.
3. Application services depend on domain logic and interfaces.
4. Domain logic remains independent of infrastructure.
5. Infrastructure implements required interfaces.
6. Workers reuse application services.
7. Provider adapters do not own business workflows.
8. Platform adapters do not own approval policy.
9. Media processing does not own publishing.
10. Cross-module access must use public module interfaces.

---

## 17. Architecture Diagram Index

| Diagram | Purpose |
|---|---|
| 01. System Context | External actors and system boundaries |
| 02. Application Architecture | Application layers |
| 03. Desktop Containers | Runtime processes |
| 04. Backend Modules | Service ownership |
| 05. AI Integration | Provider abstraction |
| 06. Social Integration | Platform adapter boundaries |
| 07. Content Data Flow | Source and variant lifecycle |
| 08. Media Processing | Media ingestion and transformation |
| 09. Database ERD | Logical entity relationships |
| 10. Publishing State Machine | Publication lifecycle |
| 11. Scheduled Execution | Worker and recovery flow |
| 12. OAuth Security | Account authorization and token handling |
| 13. Desktop Deployment | Local deployment |
| 14. SaaS Deployment | Future cloud deployment |
| 15. Security Boundaries | Trust and data boundaries |
| 16. Component Dependencies | Dependency direction |

---

## 18. Architecture Invariants

The following rules apply to every diagram and implementation:

1. PostFlow desktop uses a modular monolith.
2. The frontend does not directly publish to social platforms.
3. Domain logic does not depend on external SDKs.
4. AI provider integrations are adapter-based.
5. Social integrations are independently bounded.
6. Source content and platform variants are separate.
7. Approval is tied to an exact content revision.
8. Every destination has an independent publishing job.
9. Publishing is idempotent.
10. Unknown outcomes are reconciled before retry.
11. Scheduled jobs survive application restarts.
12. Credentials never enter frontend state or logs.
13. SQLite is the desktop structured-data source of truth.
14. Media binaries are stored outside SQLite.
15. External AI transmission is disclosed and controlled.
16. Desktop scheduling limitations are communicated clearly.
17. SaaS requires tenant isolation.
18. Unsupported API capabilities must fail explicitly.

---

## 19. Document Maintenance

Update these diagrams whenever any of the following changes:

- Application layer boundaries.
- Backend service ownership.
- Frontend-to-backend contracts.
- AI provider integration contracts.
- Social platform integration contracts.
- Database relationships.
- Publishing state transitions.
- Worker execution and recovery.
- Security boundaries.
- Desktop or SaaS deployment architecture.

Every material architecture change must be reflected in the implementation and corresponding tests.

**Final architecture recommendation:** Keep PostFlow as a local-first modular monolith for the desktop MVP. Preserve explicit service contracts and infrastructure adapters so the system can evolve into SaaS without prematurely adopting microservices or distributed infrastructure.
