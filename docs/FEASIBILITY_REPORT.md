# PostFlow - Technical Feasibility Report

**Document:** `FEASIBILITY_REPORT.md`  
**Project:** PostFlow  
**Category:** Technical feasibility and deployment assessment  
**Assessment date:** 8 November 2026  
**Status:** Proposed architecture - feasible with constraints  
**Target deployment:** Windows desktop application  
**Future deployment:** Commercial SaaS  
**Primary development environment:** Antigravity  
**Repository:** `https://github.com/kumaradoss16/PostFlow`

---

## 1. Executive Summary

### 1.1 Purpose

This report evaluates the technical feasibility of the proposed PostFlow architecture against the available development hardware, operating system, storage capacity, deployment requirements and future commercial objectives.

The assessment covers:

- Tauri 2 desktop framework.
- React and TypeScript frontend.
- Python and FastAPI backend.
- SQLite local database.
- Cloud-based AI APIs.
- Media processing using Pillow and FFmpeg.
- Background scheduling and publishing.
- Windows desktop packaging.
- Future SaaS migration.
- Resource consumption and performance.
- Security, reliability and operational constraints.

The objective is to identify architectural decisions that allow PostFlow to be developed and tested on the existing laptop without unnecessary infrastructure expenditure.

### 1.2 Executive verdict

<badge color="success">Feasible with constraints</badge>

PostFlow can be developed on the existing hardware using the proposed technology stack.

However, the implementation must follow a resource-conscious architecture.

The application should not attempt to run:

- Local large language models.
- Multiple backend worker processes.
- Heavy video-processing workloads concurrently.
- Docker-based infrastructure for normal desktop operation.
- Local PostgreSQL and Redis services.
- Multiple unnecessary background services.

The recommended architecture is:

**Tauri 2 + React + TypeScript + FastAPI + SQLite + Cloud AI APIs + Pillow + FFmpeg + Persistent Local Scheduler.**

### 1.3 Primary recommendations

| Area | Decision |
|---|---|
| Desktop framework | Tauri 2 |
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| Database | SQLite with WAL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| AI processing | Cloud APIs |
| AI integration | Provider adapter architecture |
| Image processing | Pillow |
| Video processing | FFmpeg |
| Scheduling | Persistent SQLite job queue |
| Background execution | Lightweight Python process |
| Credential storage | Windows DPAPI / Credential Manager |
| Desktop packaging | Tauri installer with bundled backend |
| Future SaaS database | PostgreSQL |
| Future SaaS queue | Redis + Celery or equivalent |

### 1.4 Critical constraint

The current development machine has 8 GB RAM.

That is sufficient for developing a lightweight desktop application, but it is not sufficient justification for running every development and infrastructure component simultaneously.

PostFlow must be designed for the available hardware rather than relying on future hardware upgrades.

---

## 2. Hardware and Environment Assessment

### 2.1 Available hardware

The assessment uses the following previously established development environment.

| Component | Available specification |
|---|---|
| Laptop | HP 15s-gr0xxx |
| Processor | AMD Ryzen 5 3450U |
| CPU cores | 4 physical cores |
| Logical processors | 8 |
| RAM | 8 GB |
| Graphics | Integrated AMD Radeon Vega |
| Storage | Approximately 100 GB available project storage |
| Operating system | Windows 10 Home Single Language |
| OS build | 19045 |
| Development environment | Antigravity |
| Target application | Windows desktop |

Actual available storage and memory should be remeasured before each major development phase.

### 2.2 Hardware limitations

The primary limitations are:

1. Limited physical memory.
2. Integrated graphics without a suitable dedicated GPU for local LLM inference.
3. CPU-intensive video encoding.
4. Limited storage for dependencies, build artifacts and media.
5. Windows background-process and power-management behavior.
6. Concurrent development tools consuming additional memory.

### 2.3 Overall hardware suitability

| Requirement | Assessment | Explanation |
|---|---|---|
| React development | Suitable | Lightweight frontend development |
| Tauri development | Suitable with build constraints | Rust compilation can be resource-intensive |
| FastAPI development | Suitable | Low overhead for normal application workloads |
| SQLite | Highly suitable | Local database with minimal infrastructure |
| Cloud AI APIs | Highly suitable | Inference happens remotely |
| Image processing | Suitable | Pillow handles normal image transformations |
| Video processing | Limited | Encoding is CPU-intensive |
| Background scheduling | Suitable with limitations | Lightweight persistent scheduler |
| Local AI inference | Not recommended | RAM and integrated GPU constraints |
| Docker infrastructure | Not recommended for normal workflow | Additional memory and storage overhead |
| Future SaaS hosting | Not suitable as production infrastructure | Use managed or dedicated cloud resources |

### 2.4 Memory management strategy

The application must minimize the number of simultaneously running processes.

Recommended operational configuration:

- One React/Tauri application process.
- One FastAPI backend process.
- One lightweight scheduling process or integrated scheduler.
- One active media-processing job.
- Cloud AI requests rather than local inference.

Do not start multiple Uvicorn workers on the desktop deployment.

Do not create separate Python processes for every platform integration.

### 2.5 Proposed memory budget

The following figures are engineering planning estimates, not measured benchmarks or guaranteed runtime usage.

| Component | Planning allowance |
|---|---:|
| Windows and background services | 2.5–3.5 GB |
| Tauri, WebView2 and React | 250–650 MB |
| FastAPI backend | 100–300 MB |
| Scheduler and job processing | 50–150 MB |
| SQLite and application data | 20–100 MB |
| Normal application overhead | 100–300 MB |
| Available operating headroom | Remaining memory |

These estimates vary with browser activity, media size, application state, operating-system services and development tooling.

**Important:** A development environment will consume substantially more memory than a packaged production application because Node.js, the development server, source maps, build tooling and the IDE remain active.

### 2.6 Memory acceptance target

For the packaged application:

- Target idle application memory: under 500 MB.
- Target ordinary active usage: under 1 GB.
- Target normal operation with one media task: under 1.5 GB.
- Avoid sustained memory growth.
- Avoid simultaneous high-memory image and video tasks.
- Avoid memory spikes caused by loading entire media files into memory.

These are proposed performance targets, not verified results.

If the application exceeds these targets, profile the actual process tree and identify the responsible component before changing the architecture.

---

## 3. Operating System Feasibility

### 3.1 Windows compatibility

Tauri uses Microsoft Edge WebView2 on Windows.

The Tauri documentation lists Microsoft C++ Build Tools and WebView2 as Windows development prerequisites. WebView2 is generally already present on Windows 10 version 1803 and later. <https://v2.tauri.app/start/prerequisites/>

The current Windows 10 environment can support development and testing, subject to the installed toolchain and dependencies.

### 3.2 Critical security issue: Windows 10 support lifecycle

Windows 10 Home and Pro reached end of support on 14 October 2025. The machine is therefore running an operating system outside normal Microsoft support unless it is covered by an applicable Extended Security Updates arrangement. <https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro>

This is not a Tauri compatibility failure. It is a security and maintenance risk.

Recommended actions:

1. Check whether the laptop supports Windows 11.
2. Upgrade to a supported operating system if possible.
3. If an upgrade is not feasible, verify ESU eligibility and enrollment.
4. Avoid treating an unsupported operating system as an acceptable production security baseline.
5. Test PostFlow on a currently supported Windows version before commercial release.

### 3.3 Development prerequisites

Install only what is required:

- Node.js LTS.
- Rust stable MSVC toolchain.
- Microsoft C++ Build Tools.
- WebView2 Runtime.
- Python.
- Git.
- Antigravity.
- Required project package managers.

Avoid installing unnecessary SDKs, emulators and infrastructure tools on the development machine.

### 3.4 Operating system decision

<badge color="warning">Conditional</badge>

The current Windows 10 machine is acceptable for development continuity, but it should not define the long-term supported production environment.

Windows 11 should be the preferred desktop validation target if the hardware supports it.

---

## 4. Tauri 2 Feasibility

### 4.1 Role

Tauri will provide:

- Windows desktop application packaging.
- Native application lifecycle.
- Frontend hosting.
- Secure frontend/backend communication.
- System tray functionality.
- Window management.
- Native notifications.
- File-system integration.
- Application updater integration where configured.

### 4.2 Resource suitability

Tauri is a strong fit for the hardware constraints because the frontend is rendered through the operating system's WebView2 runtime rather than bundling a complete Chromium browser.

However, Tauri does not make the React interface free of memory or CPU costs.

Large frontend bundles, excessive state updates, complex dashboards and oversized media previews can still affect performance.

### 4.3 Windows build requirements

Development requires:

- Rust.
- Microsoft C++ Build Tools.
- WebView2.
- Node.js for the frontend framework.

Production builds should use release mode.

Development builds must not be used to measure final application performance.

### 4.4 Backend integration

Two possible integration patterns exist.

**Option A - Bundled FastAPI sidecar**

Tauri launches a packaged Python backend executable.

Advantages:

- Preserves the Python backend architecture.
- Allows Python dependencies to be packaged with the application.
- Separates frontend and backend responsibilities.
- Provides a straightforward path to future SaaS reuse.

Disadvantages:

- Requires backend packaging.
- Requires process supervision.
- Requires startup and shutdown coordination.
- Adds executable size.
- Requires local API authentication.

**Option B - Native Rust backend**

Implement backend responsibilities directly in Rust.

Advantages:

- Fewer runtime dependencies.
- Potentially lower process overhead.

Disadvantages:

- Duplicates or replaces the Python backend.
- Makes reuse of Python integrations more difficult.
- Increases development complexity.
- Requires rewriting existing Python functionality.

### 4.5 Recommendation

<badge color="success">Recommended</badge> Use Tauri 2 with a packaged FastAPI sidecar.

Do not rewrite the backend in Rust solely to reduce memory usage without first measuring a real bottleneck.

### 4.6 Security requirements

- Restrict Tauri capabilities.
- Use explicit command permissions.
- Avoid unrestricted shell access.
- Bind the local API to `127.0.0.1`.
- Generate a per-installation API secret.
- Validate every frontend-to-backend request.
- Do not expose backend administrative endpoints to arbitrary local processes.
- Supervise backend process startup and shutdown.
- Ensure the sidecar cannot be launched with unsafe arguments from frontend input.

### 4.7 Acceptance criteria

- Desktop application launches without a globally installed Python runtime.
- Backend starts and stops correctly.
- Frontend cannot access arbitrary backend functionality.
- Local API rejects unauthenticated requests.
- Application can restart after backend failure.
- Installer works on a clean supported Windows environment.
- No secrets are embedded in frontend bundles.

---

## 5. React and TypeScript Feasibility

### 5.1 Role

React will provide the complete PostFlow user interface.

Main UI areas:

- Dashboard.
- Workspace management.
- Brand management.
- AI content studio.
- AI provider configuration.
- Media library.
- Multi-platform composer.
- Social account connections.
- Approval workflow.
- Publishing calendar.
- Job history.
- Analytics.
- Settings.

### 5.2 Resource suitability

React is suitable for the current machine.

The primary performance risks are not the framework itself. They are:

- Excessive component rendering.
- Large unoptimized images.
- Huge media lists.
- Excessive application state.
- Unnecessary background polling.
- Large JavaScript dependencies.
- Heavy rich-text editing components.
- Unoptimized calendar and analytics rendering.

### 5.3 Recommended frontend stack

| Component | Recommendation |
|---|---|
| Framework | React |
| Language | TypeScript |
| Build tool | Vite |
| Styling | CSS Modules or structured CSS |
| Routing | React Router |
| Server state | TanStack Query |
| Local state | Zustand or React Context where appropriate |
| Forms | React Hook Form |
| Validation | Zod |
| Calendar | Lightweight calendar library |
| Icons | Lucide |
| Charts | Lightweight chart library |
| Testing | Vitest and Playwright |

Avoid adding multiple overlapping state-management and UI frameworks.

### 5.4 Performance requirements

- Lazy-load nonessential modules.
- Paginate media and content lists.
- Use thumbnail previews.
- Avoid rendering full-resolution images in list views.
- Virtualize large tables where needed.
- Avoid frequent polling.
- Use event-driven updates where practical.
- Split analytics and calendar bundles.
- Cache stable reference data.
- Keep dashboard queries bounded.

### 5.5 Production build

Use Vite's production build rather than the development server for packaging and performance evaluation. <https://vite.dev/guide/build>

### 5.6 Acceptance criteria

- Dashboard loads without blocking the UI.
- Large media libraries do not render every asset simultaneously.
- Calendar navigation remains responsive.
- Background job updates do not cause full-screen rerenders.
- No unnecessary API polling.
- Frontend bundle size is tracked in CI.

---

## 6. FastAPI Feasibility

### 6.1 Role

FastAPI will serve as the main application backend.

Responsibilities:

- Business logic.
- API endpoints.
- Database access.
- AI provider orchestration.
- Platform integrations.
- OAuth workflows.
- Media management.
- Publishing jobs.
- Scheduling.
- Analytics.
- Application settings.
- Security and audit logging.

### 6.2 Resource suitability

FastAPI is suitable for the available hardware.

The backend is not expected to perform local AI inference or run large computational workloads.

Most AI and social platform operations involve network requests, which are suitable for asynchronous I/O.

### 6.3 Recommended runtime

Desktop:

- One Uvicorn worker.
- One FastAPI process.
- Async HTTP clients.
- Bounded connection pools.
- Bounded task concurrency.
- Persistent job storage.
- Graceful shutdown.

Do not run multiple independent Uvicorn worker processes against the same SQLite database.

FastAPI's deployment guidance identifies memory, process count, startup, restarts and security as important deployment considerations. <https://fastapi.tiangolo.com/deployment/concepts/>

### 6.4 Asynchronous operations

Use asynchronous execution for:

- AI API requests.
- Social platform API requests.
- OAuth exchanges.
- Account synchronization.
- Publishing operations.
- Network-based media transfers.

Use controlled thread or process execution for CPU-intensive tasks when necessary.

Do not run long-running video encoding directly inside an HTTP request handler.

### 6.5 Process management

The packaged application should supervise FastAPI.

Responsibilities include:

- Backend startup.
- Health checks.
- Process termination.
- Restart after unexpected failure.
- Port selection.
- Local authentication.
- Log rotation.

The application should not assume that a hardcoded local port is always available.

### 6.6 Acceptance criteria

- Backend starts reliably.
- API binds only to loopback.
- Health endpoint is available.
- Application requests are authenticated.
- Backend restarts do not lose queued jobs.
- One failed provider does not stop other providers.
- Long-running jobs do not block HTTP request handling.
- Logs do not expose credentials.

---

## 7. SQLite Feasibility

### 7.1 Role

SQLite is the recommended database for the desktop deployment.

It will store:

- Workspaces.
- Brands.
- Social accounts.
- Content items.
- Platform variants.
- Media metadata.
- AI provider configuration.
- Publishing jobs.
- Publishing attempts.
- Scheduling records.
- Approval history.
- Analytics snapshots.
- Audit logs.
- Application settings.

### 7.2 Resource suitability

SQLite is highly suitable for a single-user local-first application.

It avoids the overhead of maintaining a separate database server.

The database is embedded in the application environment and can be backed up as part of the local workspace.

### 7.3 WAL mode

Enable Write-Ahead Logging where appropriate.

SQLite WAL allows readers and writers to operate concurrently, but it still permits only one writer at a time. It also requires participating processes to use the same host and is unsuitable for sharing the database over a network filesystem. <https://www.sqlite.org/wal.html>

Recommended configuration:

```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
```

The durability trade-off of `synchronous=NORMAL` must be explicitly accepted. Use `FULL` if the stronger durability requirement justifies the additional write cost.

### 7.4 Database access strategy

Use:

- SQLAlchemy.
- Alembic migrations.
- Explicit transactions.
- Short-lived database sessions.
- Foreign-key constraints.
- Appropriate indexes.
- UTC timestamps.
- UUID identifiers.

Do not hold database transactions open while waiting for an external API request.

### 7.5 Concurrency constraints

SQLite is suitable for the desktop version because:

- One local user is the primary workload.
- Writes are relatively small.
- API calls happen outside database transactions.
- Background publishing concurrency can be bounded.

SQLite becomes less appropriate when PostFlow requires:

- Many simultaneous SaaS users.
- Multiple application instances.
- High write concurrency.
- Multi-tenant production workloads.
- Distributed workers accessing shared state.

### 7.6 Backup and recovery

Implement:

- SQLite online backup API or a safe backup procedure.
- Database integrity checks.
- Restore validation.
- WAL-aware backup handling.
- Automatic backup before migrations.
- Backup version metadata.

Do not simply copy the main `.db` file while WAL activity is ongoing and assume that the result is a consistent backup.

### 7.7 Acceptance criteria

- Database migrations run successfully.
- Application restarts preserve state.
- Backup and restore pass.
- Foreign keys are enforced.
- Concurrent reads work.
- Write contention is handled.
- Failed transactions do not leave partial application state.
- Database integrity checks pass.

### 7.8 Decision

<badge color="success">Recommended for desktop</badge>

Use SQLite for the first deployment.

Do not introduce PostgreSQL into the local development stack just to prepare for a future SaaS product.

---

## 8. AI API Feasibility

### 8.1 AI architecture

PostFlow should use cloud AI APIs rather than local inference.

The application should provide an extensible provider architecture for:

- OpenAI.
- Google Gemini.
- Anthropic Claude.
- Perplexity.
- Future providers.

### 8.2 Hardware suitability

Cloud AI APIs are the best fit for the current laptop.

Benefits:

- No local model downloads.
- No GPU memory requirement.
- No local inference CPU consumption.
- No need for 16 GB or more RAM solely for LLM inference.
- Easier support for different models.
- Centralized provider configuration.

The local application is responsible for preparing requests, transmitting authorized data, receiving results and validating responses.

### 8.3 Provider adapter design

Each provider should implement a common internal contract where supported.

```python
class AIProviderAdapter:

    async def generate_text(self, request):
        ...

    async def generate_structured(self, request):
        ...

    async def analyze_image(self, request):
        ...

    async def research(self, request):
        ...

    async def validate_connection(self):
        ...
```

The actual supported capabilities must be declared by each provider adapter.

Do not assume all providers support identical models, structured outputs, image inputs, research tools or token limits.

### 8.4 AI capabilities

Potential features:

- Content generation.
- Platform-specific adaptation.
- Caption generation.
- Hashtag suggestions.
- Content rewriting.
- Tone adjustment.
- Campaign planning.
- Content research.
- Image analysis.
- Content quality evaluation.
- Multi-model comparison.

### 8.5 Multi-provider execution

The architecture should support:

- User-selected provider.
- User-selected model.
- Provider capability validation.
- Independent parallel requests.
- Result comparison.
- Provider-specific error handling.
- User-authorized fallback.

Never silently send content to a different provider when the selected provider fails.

### 8.6 Cost management

AI API costs are separate from the ChatGPT subscription or other consumer subscriptions.

PostFlow must track:

- Provider.
- Model.
- Input tokens.
- Output tokens.
- Estimated request cost.
- Actual billed cost where available.
- Request timestamp.
- Workspace.
- User-configured spending limits.

Provider pricing and rate limits can change. For example, OpenAI publishes model-specific pricing and request/token limits; these must be retrieved from the current provider documentation rather than embedded as permanent constants. <https://developers.openai.com/api/docs/pricing> <https://developers.openai.com/api/docs/guides/rate-limits>

### 8.7 Data transmission and privacy

Before transmitting data to a provider, disclose:

- Provider name.
- Model.
- Content being transmitted.
- Media being transmitted.
- Purpose.
- Relevant retention or processing information.
- Whether the provider is an external third party.

The provider's data retention and processing policy must be reviewed independently. <https://developers.openai.com/api/docs/guides/your-data>

### 8.8 Security requirements

- Store API keys using OS-backed credential storage.
- Never expose keys in React.
- Never include keys in frontend requests.
- Redact credentials from logs.
- Support key rotation.
- Support provider disconnection.
- Use request timeouts.
- Apply bounded retries.
- Validate structured output.
- Enforce provider-specific request limits.

### 8.9 Acceptance criteria

- Multiple provider adapters work independently.
- Provider failures are isolated.
- API keys remain protected.
- Token usage is recorded.
- Cost estimates are available.
- User-authorized fallback works.
- AI output is validated before saving.
- Cloud transmission requires appropriate user authorization.

### 8.10 Decision

<badge color="success">Highly recommended</badge>

Use cloud AI APIs for the desktop MVP and future SaaS architecture.

Do not introduce Ollama, local LLMs, GPU inference or local vector infrastructure into the initial PostFlow runtime.

---

## 9. Media Processing Feasibility

### 9.1 Media architecture

PostFlow needs media processing for:

- Image resizing.
- Image compression.
- Format conversion.
- Thumbnail generation.
- Video conversion.
- Video compression.
- Aspect-ratio validation.
- Platform-specific output preparation.

### 9.2 Image processing

Recommended library: Pillow.

Pillow is suitable for:

- JPEG and PNG processing.
- Resizing.
- Cropping.
- Compression.
- Thumbnail creation.
- Metadata extraction.
- Format conversion.

Image processing is feasible on the current laptop when performed with bounded memory usage.

### 9.3 Video processing

Recommended tool: FFmpeg.

FFmpeg can support:

- Video transcoding.
- Format conversion.
- Compression.
- Resolution changes.
- Audio handling.
- Thumbnail extraction.
- Metadata inspection.

However, video encoding can consume substantial CPU resources.

### 9.4 Hardware constraints

The Ryzen 5 3450U is a mobile processor.

The integrated Radeon Vega graphics should not be treated as a reliable general-purpose GPU acceleration platform for the complete video-processing pipeline.

PostFlow should support CPU-based FFmpeg encoding as its baseline.

Hardware acceleration can be investigated later, but it must remain optional.

### 9.5 Resource-control strategy

Recommended controls:

| Control | Initial policy |
|---|---|
| Concurrent image jobs | 1–2 |
| Concurrent video jobs | 1 |
| Large media processing | Background only |
| Maximum in-memory media | Avoid whole-file loading |
| Video preview | Generate lower-resolution preview |
| Full-resolution preview | On demand |
| Temporary files | Controlled cleanup |
| Processing cancellation | Required |
| Progress reporting | Required |

The concurrency figures are starting configuration values, not measured hardware limits.

### 9.6 Processing workflow

```text
Media Upload
     |
     v
File Type Validation
     |
     v
File Signature Validation
     |
     v
Metadata Extraction
     |
     v
Platform Requirements Check
     |
     v
Processing Job Creation
     |
     v
Pillow / FFmpeg Execution
     |
     v
Output Validation
     |
     v
Media Library Registration
     |
     v
Platform Upload or Publishing
```

### 9.7 Storage implications

Media files can consume significantly more storage than application code.

Keep media outside the SQLite database.

Recommended directory:

```text
PostFlowData/
├── database/
│   └── postflow.db
├── media/
│   ├── originals/
│   ├── processed/
│   ├── thumbnails/
│   └── temporary/
├── backups/
├── logs/
└── cache/
```

### 9.8 FFmpeg distribution

FFmpeg is an external dependency with its own licensing considerations.

Before packaging:

- Review the exact FFmpeg build configuration.
- Verify enabled codecs and libraries.
- Review the applicable LGPL/GPL obligations.
- Preserve required license notices.
- Document third-party components.
- Verify redistribution rights.

Do not assume every FFmpeg binary has the same licensing implications.

### 9.9 Acceptance criteria

- Invalid media is rejected.
- File signatures are checked.
- Processing is cancellable.
- Memory usage is bounded.
- Temporary files are cleaned safely.
- Video jobs do not block the frontend.
- Output files are validated.
- Platform-specific requirements are enforced.
- Media processing failures preserve original files.

### 9.10 Decision

<badge color="success">Feasible with workload limits</badge>

Use Pillow for image processing and FFmpeg for video processing.

Keep video processing asynchronous and limit it to one active job on the development machine.

---

## 10. Background Scheduling Feasibility

### 10.1 Requirement

PostFlow must support:

- Scheduled posts.
- Queue management.
- Automatic publishing.
- Manual approval.
- Retry management.
- Missed schedule recovery.
- Persistent job history.
- Application restart recovery.

### 10.2 Desktop scheduling constraint

A scheduled publishing system cannot guarantee execution if the computer is powered off or unable to access the internet.

If PostFlow is running as a normal desktop application, scheduling also depends on the application or its background process being active.

This must be disclosed in the product UI.

### 10.3 Recommended architecture

Use a persistent SQLite-backed job scheduler.

The scheduler should operate independently of React.

Recommended design:

```text
Tauri Desktop Application
          |
          v
FastAPI Backend
          |
          v
Persistent SQLite Job Store
          |
          v
Scheduler Process
          |
          v
Due Job Detection
          |
          v
Publishing Orchestrator
          |
          v
Platform Adapter
          |
          v
Social Platform API
          |
          v
Publishing Attempt Record
```

### 10.4 Scheduler implementation

For the initial version, use a lightweight Python scheduling implementation.

Possible approaches:

- APScheduler with a persistent job store where compatible with the required deployment model.
- A custom database-backed scheduler using SQLite and explicit due-job polling.

Recommendation: use a database-backed scheduler with PostFlow-owned job state and locking semantics.

A scheduling library may trigger jobs, but it should not become the source of truth for publication status.

### 10.5 Job persistence

Every scheduled job must include:

- Job ID.
- Content variant ID.
- Destination account ID.
- Scheduled UTC timestamp.
- User timezone.
- Current state.
- Approval revision.
- Idempotency key.
- Attempt count.
- Last execution time.
- Next retry time.
- Last error.
- Remote publication ID.

### 10.6 Execution constraints

The scheduler should:

- Run one publishing job at a time initially.
- Recover due jobs after application restart.
- Use atomic job claiming.
- Avoid duplicate execution.
- Respect platform rate limits.
- Respect user cancellation.
- Handle token expiration.
- Preserve unknown outcomes.
- Reconcile before retrying.

### 10.7 Windows background execution

Three possible approaches exist.

| Approach | Assessment |
|---|---|
| Scheduler inside the main application | Simplest, but stops when the application exits |
| Separate lightweight background process | Recommended for desktop scheduling |
| Windows Task Scheduler integration | Useful for starting or recovering the background process |

Recommended implementation:

- Register a lightweight background process to start at user logon.
- Persist jobs in SQLite.
- Allow the process to execute due jobs.
- Coordinate it with the main application.
- Ensure only one scheduler instance claims a job.
- Provide explicit pause and exit controls.

Do not install a Windows service as the initial requirement.

A Windows service introduces installation, privilege, lifecycle and debugging complexity that is unnecessary for the first single-user release.

### 10.8 Power and network conditions

The product must handle:

- Device powered off.
- Device sleeping.
- Internet disconnected.
- Application closed.
- Backend process stopped.
- Platform API unavailable.
- Authentication expired.

The scheduler should report missed jobs and provide a recovery decision instead of silently publishing stale content.

### 10.9 Acceptance criteria

- Scheduled jobs survive application restart.
- Duplicate scheduler processes cannot publish the same job.
- Missed jobs are identified.
- Network failure is handled.
- Authentication failure is handled.
- Unknown publishing outcomes are reconciled.
- Job cancellation works.
- Timezone conversion is correct.
- Manual approval remains the default.

### 10.10 Decision

<badge color="success">Feasible with operational limitations</badge>

Use a persistent local scheduler and a lightweight background process.

Do not promise 24/7 publishing reliability from a desktop computer.

---

## 11. Storage Feasibility

### 11.1 Available storage

The current project environment has approximately 100 GB available storage.

This must cover:

- Source code.
- Node dependencies.
- Python virtual environments.
- Rust build artifacts.
- Tauri build artifacts.
- Backend packaging.
- Media test assets.
- FFmpeg.
- Installer output.
- Logs.
- Database backups.

### 11.2 Proposed storage allocation

The following is a planning budget, not a measurement of current disk usage.

| Category | Budget |
|---|---:|
| Repository and source code | 2 GB |
| Node dependencies | 2 GB |
| Python environments and dependencies | 2 GB |
| Rust and Tauri build artifacts | 8 GB |
| Installer and release artifacts | 3 GB |
| Test media | 10 GB |
| Application data and database | 10 GB |
| Backups and logs | 5 GB |
| Operating headroom | 58 GB |
| **Total** | **100 GB** |

Actual storage consumption must be measured after initial dependency installation and release packaging.

### 11.3 Storage controls

- Keep build artifacts out of version control.
- Use `.gitignore` correctly.
- Delete temporary media.
- Avoid duplicate copies of original assets.
- Generate thumbnails on demand.
- Limit retained processing output.
- Rotate logs.
- Provide backup retention controls.
- Allow media storage location configuration.

### 11.4 Acceptance criteria

- Storage usage is measurable.
- Cache cleanup works.
- Temporary media cleanup works.
- Backups can be configured.
- Database and media restore are tested.
- Low-disk-space warnings are displayed.

---

## 12. Recommended Development Architecture

### 12.1 Desktop architecture

```text
                    POSTFLOW DESKTOP
                           |
             +-------------+-------------+
             |                           |
             v                           v
       TAURI 2 SHELL                 REACT UI
             |                           |
             |                      TypeScript
             |                           |
             +-------------+-------------+
                           |
                           v
                   LOCAL API CLIENT
                           |
                           v
                  FASTAPI BACKEND
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      BUSINESS         AI PROVIDERS     INTEGRATIONS
       LOGIC           ADAPTERS          REGISTRY
          |                |                |
          +----------------+----------------+
                           |
                           v
                     SQLITE DATABASE
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      MEDIA SERVICE    JOB SCHEDULER    AUDIT SERVICE
          |                |                |
          v                v                v
      PILLOW/FFMPEG    PUBLISHING       LOCAL LOGS
                           |
                           v
                    SOCIAL PLATFORM APIs
```

### 12.2 Recommended deployment layout

```text
PostFlow/
├── PostFlow.exe
├── resources/
│   ├── backend/
│   │   └── postflow-backend.exe
│   ├── scheduler/
│   │   └── postflow-scheduler.exe
│   ├── ffmpeg/
│   │   └── ffmpeg.exe
│   └── frontend/
│
└── user-data/
    ├── database/
    ├── media/
    ├── backups/
    ├── logs/
    └── cache/
```

This represents a logical deployment layout. Exact packaging paths should follow Tauri's supported resource and sidecar configuration.

User data must remain outside the application installation directory.

---

## 13. Development Workflow for the Current Hardware

### 13.1 Recommended development mode

Avoid starting every service simultaneously.

Use the following workflow:

**Frontend development**

- Start Vite.
- Start the backend only when required.
- Use mock API responses for UI-only development.
- Avoid running FFmpeg in the background.

**Backend development**

- Run FastAPI with one process.
- Use SQLite.
- Mock external platform APIs where appropriate.
- Avoid starting all integrations simultaneously.

**AI development**

- Use one provider request at a time during early development.
- Set request timeouts.
- Keep output sizes bounded.
- Track API costs.

**Media development**

- Test small files first.
- Run one video task.
- Use low-resolution previews.
- Profile memory and CPU.

**Desktop packaging**

- Stop unnecessary development servers.
- Use release builds.
- Build one installer target at a time.
- Clean old build artifacts after verification.

### 13.2 Avoid

- Docker Compose as a mandatory desktop dependency.
- Local PostgreSQL.
- Local Redis.
- Kubernetes.
- Local LLM inference.
- Multiple Uvicorn workers.
- Multiple simultaneous FFmpeg encoders.
- Unbounded AI concurrency.
- Large media fixtures in the repository.

### 13.3 Development quality gate

Before adding a new dependency, answer:

1. What functionality does it provide?
2. Is it necessary for the MVP?
3. Does an existing dependency already provide the capability?
4. What is its memory footprint?
5. What is its disk footprint?
6. Does it introduce native build requirements?
7. Does it create licensing obligations?
8. Can it be removed without changing the architecture?

---

## 14. Future SaaS Deployment Feasibility

### 14.1 Desktop and SaaS separation

PostFlow should not become a desktop application that later requires a complete rewrite to support SaaS.

The shared application core should be separated from deployment-specific infrastructure.

### 14.2 Shared components

Reuse:

- Domain models.
- Business logic.
- AI provider adapters.
- Social platform adapters.
- Publishing contracts.
- Content validation.
- Media-processing abstractions.
- API schemas.
- Tests.
- Core workflows.

### 14.3 Desktop deployment

```text
Tauri
  |
React
  |
FastAPI
  |
SQLite
  |
Local Media Storage
  |
Local Scheduler
```

### 14.4 SaaS deployment

```text
Web Frontend
     |
API Gateway
     |
FastAPI Application
     |
PostgreSQL
     |
Redis
     |
Distributed Workers
     |
Object Storage
     |
AI Providers
     |
Social Platform APIs
```

### 14.5 Future infrastructure

| Component | Desktop | SaaS |
|---|---|---|
| Frontend | React + Tauri | React web application |
| Backend | FastAPI sidecar | FastAPI services |
| Database | SQLite | PostgreSQL |
| Job queue | Persistent SQLite jobs | Redis-backed distributed queue |
| Workers | Local lightweight process | Distributed workers |
| Media storage | Local filesystem | Object storage |
| Secrets | Windows secure storage | Cloud secret manager |
| Authentication | Local application security | Central identity and access management |
| Monitoring | Local logs | Centralized monitoring |
| Scaling | Single machine | Horizontal scaling |

### 14.6 Migration requirements

- Keep business logic independent of SQLite.
- Use SQLAlchemy models and migrations.
- Avoid SQLite-specific SQL in business services.
- Define storage interfaces.
- Define job queue interfaces.
- Define credential storage interfaces.
- Avoid desktop-only assumptions in shared services.
- Introduce tenant isolation before SaaS data is exposed.
- Keep workspace ownership explicit.

### 14.7 SaaS release gate

The SaaS architecture should be treated as a separate deployment profile.

Do not add PostgreSQL, Redis, Celery and cloud object storage to the local desktop runtime.

Implement these only when the SaaS deployment is actually being developed.

---

## 15. Performance and Reliability Targets

The following are initial engineering targets to be measured on actual hardware.

They are not established benchmarks.

| Area | Initial target |
|---|---|
| Desktop cold startup | Under 5 seconds |
| Dashboard initial render | Under 3 seconds after backend readiness |
| Local API health check | Under 200 ms |
| SQLite normal reads | Under 100 ms for typical indexed queries |
| Normal idle memory | Under 500 MB |
| Normal active memory | Under 1 GB |
| Single media job | Under 1.5 GB total application memory |
| Background scheduler polling | Configurable, low-frequency polling |
| Job recovery | No loss of persisted jobs after restart |
| Duplicate publishing | Prevented through reconciliation and job ownership |
| Backend recovery | Automatic restart or explicit failure notification |
| AI requests | Configurable timeouts and bounded retries |

### 15.1 Measurement methodology

Measure:

- Process memory.
- CPU utilization.
- Disk I/O.
- Database query duration.
- Frontend rendering performance.
- Media-processing duration.
- AI request latency.
- Scheduler delay.
- Publishing success rate.

Use representative datasets rather than empty development databases.

### 15.2 Stress scenarios

Test:

1. Dashboard with 1,000 content records.
2. Media library with 1,000 assets.
3. 100 scheduled jobs.
4. 10 connected social accounts.
5. One active video-processing task.
6. AI generation with a large prompt.
7. Application restart with queued jobs.
8. Network interruption during publication.
9. Low disk space.
10. Database backup during normal application activity.

---

## 16. Technical Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| 8 GB RAM exhaustion | High | One backend process, bounded concurrency, cloud AI |
| Windows 10 end of support | High | Upgrade or verify ESU; validate Windows 11 |
| Video encoding overload | High | One video worker, background processing |
| Local API exposure | High | Loopback binding and per-installation authentication |
| OAuth credential leakage | Critical | OS-backed credential storage |
| SQLite write contention | Medium | Short transactions and bounded writers |
| Scheduler stops with desktop | High | Separate background process and startup recovery |
| Device sleep or shutdown | High | Missed-job detection and user disclosure |
| External API rate limits | Medium | Rate-aware retries and backoff |
| Provider cost overruns | High | Usage tracking and spending controls |
| Media hosting requirements | High | Explicit temporary storage architecture |
| API approval delays | High | Validate access before committing to features |
| SaaS migration complexity | Medium | Deployment abstraction and PostgreSQL-ready data access |
| Installer size growth | Medium | Dependency audit and packaging optimization |
| FFmpeg licensing | High | Review exact build and distribution obligations |

---

## 17. Feasibility Decision Matrix

| Technology | Hardware feasibility | Deployment feasibility | Decision |
|---|---|---|---|
| Tauri 2 | High | High | Adopt |
| React | High | High | Adopt |
| TypeScript | High | High | Adopt |
| FastAPI | High | High | Adopt |
| SQLite | High | High for desktop | Adopt |
| SQLAlchemy | High | High | Adopt |
| Alembic | High | High | Adopt |
| Cloud AI APIs | High | High | Adopt |
| Pillow | High | High | Adopt |
| FFmpeg | Moderate | High with controls | Adopt |
| Local scheduler | High | Conditional on device availability | Adopt |
| Windows background process | High | Moderate | Adopt with lifecycle controls |
| PostgreSQL | Not needed locally | High for SaaS | Defer |
| Redis | Not needed locally | High for SaaS | Defer |
| Celery | Not needed locally | High for SaaS | Defer |
| Local LLM inference | Low | Unnecessary | Reject for MVP |
| Docker infrastructure | Low priority | Unnecessary for desktop | Defer |

---

## 18. Implementation Roadmap Based on Feasibility

### Phase 0 - Environment and foundation

**Objective:** Establish a reproducible, low-resource development environment.

Deliverables:

- Verify Windows compatibility.
- Verify available storage.
- Install Rust and Node.js.
- Configure Python environment.
- Initialize Tauri.
- Initialize React and TypeScript.
- Initialize FastAPI.
- Configure SQLite.
- Establish development scripts.
- Establish baseline resource measurements.

Exit criteria:

- Application shell launches.
- Backend starts.
- Database connects.
- Frontend communicates with backend.
- Resource baseline is recorded.

### Phase 1 - Desktop foundation

Deliverables:

- Tauri application lifecycle.
- React shell.
- FastAPI sidecar.
- Local API authentication.
- SQLite migrations.
- Application settings.
- Logging.
- Error handling.

Exit criteria:

- Packaged application starts.
- Backend lifecycle is managed.
- Data survives restarts.
- Local API is protected.

### Phase 2 - Core application data

Deliverables:

- Workspace.
- Brand management.
- Content records.
- Platform variants.
- Approval workflow.
- Persistent state.

Exit criteria:

- Data integrity tests pass.
- Application restart preserves content.
- Approval is bound to content revision.

### Phase 3 - AI integration

Deliverables:

- Provider registry.
- Secure API key storage.
- OpenAI adapter.
- Gemini adapter.
- Claude adapter.
- Perplexity adapter.
- Usage tracking.
- Data transmission disclosure.

Exit criteria:

- Provider requests work.
- Errors are isolated.
- Keys are not exposed.
- Usage and cost records are stored.

### Phase 4 - Media pipeline

Deliverables:

- Media library.
- Pillow integration.
- FFmpeg integration.
- Thumbnail generation.
- Validation.
- Background processing.
- Temporary storage cleanup.

Exit criteria:

- Image processing works.
- Video processing works within resource limits.
- Processing is cancellable.
- Originals remain intact.

### Phase 5 - Social integrations

Deliverables:

- OAuth infrastructure.
- LinkedIn adapter.
- Facebook Pages adapter.
- Instagram adapter.
- Threads adapter.
- Pinterest adapter.
- X adapter.
- Reddit only after commercial permission.

Exit criteria:

- Required API access is approved.
- Live test accounts work.
- Account capabilities are verified.
- Tokens are secure.

### Phase 6 - Publishing engine

Deliverables:

- Publishing orchestrator.
- Persistent jobs.
- Idempotency.
- Attempt history.
- Reconciliation.
- Retry policy.
- Per-platform error handling.

Exit criteria:

- Successful publishing.
- Failure isolation.
- No blind retries.
- No duplicate job execution.

### Phase 7 - Scheduler and calendar

Deliverables:

- Background scheduler.
- Persistent job recovery.
- Missed-job handling.
- Windows startup integration.
- Calendar.
- Manual approval default.

Exit criteria:

- Jobs recover after restart.
- Missed schedules are detected.
- Timezones work correctly.
- Duplicate scheduler execution is prevented.

### Phase 8 - Release and packaging

Deliverables:

- Windows installer.
- Backend packaging.
- FFmpeg packaging.
- Application updater.
- Backup and restore.
- Clean-machine installation tests.
- Performance and security testing.

Exit criteria:

- Clean installation works.
- Application can be upgraded.
- Data survives upgrades.
- No critical security issues remain.

### Phase 9 - SaaS preparation

Deliverables:

- PostgreSQL deployment profile.
- Redis-backed job queue.
- Cloud object storage.
- Tenant isolation.
- Central authentication.
- Distributed worker architecture.
- Centralized monitoring.

Exit criteria:

- Desktop functionality remains stable.
- SaaS-specific tests pass.
- Tenant isolation is verified.
- Deployment and rollback procedures are documented.

---

## 19. Final Architecture Recommendation

### 19.1 Adopt this stack

| Layer | Selected technology |
|---|---|
| Desktop | Tauri 2 |
| UI | React |
| Language | TypeScript |
| Build | Vite |
| Backend | Python FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| AI | Cloud provider APIs |
| Image processing | Pillow |
| Video processing | FFmpeg |
| Scheduling | Persistent SQLite-backed scheduler |
| Background execution | Lightweight Python process |
| Credential storage | Windows DPAPI / Credential Manager |
| Packaging | Tauri Windows installer |

### 19.2 Architecture constraints

The following are mandatory for the initial implementation:

1. No local LLM inference.
2. No mandatory Docker runtime.
3. No local PostgreSQL.
4. No local Redis.
5. One FastAPI process.
6. Bounded media-processing concurrency.
7. Persistent scheduling state.
8. Secure credential storage.
9. Loopback-only backend.
10. No direct publishing from the frontend.
11. No blind retries for unknown publishing outcomes.
12. No assumption that desktop scheduling works while the machine is powered off.
13. No production release dependency on unsupported Windows 10.
14. No unapproved platform API usage.

### 19.3 Final verdict

**Proceed with the proposed PostFlow architecture.**

The technology stack is appropriate for the current hardware and the desktop-first product strategy.

The architecture does not need to be simplified by removing FastAPI, replacing React or introducing a different database.

The real requirement is disciplined resource management.

The biggest risks are:

- Windows 10 security lifecycle.
- Video-processing resource consumption.
- Persistent scheduler reliability.
- External API access and approval.
- OAuth credential protection.
- Media delivery requirements.
- Future SaaS isolation.

Address these through explicit engineering controls rather than introducing heavyweight infrastructure prematurely.

---

## 20. Sources and Technical References

### Tauri

- [Tauri 2 Prerequisites](https://v2.tauri.app/start/prerequisites/)

### FastAPI

- [Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
- [Deployment](https://fastapi.tiangolo.com/deployment/)

### React and Vite

- [Vite Production Build](https://vite.dev/guide/build)

### SQLite

- [SQLite Write-Ahead Logging](https://www.sqlite.org/wal.html)

### Python

- [Python on Windows](https://docs.python.org/3/using/windows.html)

### OpenAI API

- [API Pricing](https://developers.openai.com/api/docs/pricing)
- [Rate Limits](https://developers.openai.com/api/docs/guides/rate-limits)
- [Data Controls](https://developers.openai.com/api/docs/guides/your-data)

### Windows

- [Windows 10 Home and Pro Lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro)
- [Windows 10 End of Support](https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/windows-10-support-has-ended-on-october-14-2025)

### Media processing

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Legal Information](https://ffmpeg.org/legal.html)

---

## 21. Document Control

| Field | Value |
|---|---|
| Document | `FEASIBILITY_REPORT.md` |
| Project | PostFlow |
| Version | 1.0 |
| Status | Proposed architecture assessment |
| Owner | PostFlow Product and Engineering |
| Created | 8 November 2026 |
| Next review | Before Phase 1 implementation |
| Review frequency | At major architecture changes |

**Related project documents:**

- `PRODUCT_VISION.md`
- `PRD.md`
- `USER_STORIES.md`
- `ACCEPTANCE_CRITERIA.md`
- `TEST_PLAN.md`
- `TRACEABILITY_MATRIX.md`
- `MARKET_RESEARCH.md`
- `PLATFORM_API_RESEARCH.md`
- `ARCHITECTURE.md`
- `TECH_STACK.md`
- `SECURITY.md`
- `API_SPECIFICATION.md`

**Final approval condition:** The architecture is approved for implementation planning, but performance targets, Windows compatibility, packaging behavior and scheduler reliability must be validated through measured tests on the actual development machine before production release.

## M0 Reconciliation — Feasibility Scope and Support Decision

**Authority:** `docs/IMPLEMENTATION_BASELINE.md` and `docs/BUILD_READINESS_REPORT.md`. This addendum supersedes conflicting MVP scope and design assumptions in this document. The target is a single-user, local-first Windows desktop MVP. Windows 11 is the production support baseline; Windows 10 is best-effort development only. P0 includes Tauri 2/Rust, React/TypeScript, supervised FastAPI, SQLite/SQLAlchemy/Alembic, local media, source content and independent revisioned variants, one AI provider, exact human approval, durable per-destination publishing jobs, idempotency/immutable attempts/unknown-outcome reconciliation, one-time local scheduling, privacy, backup and restore. At most one official social-platform integration may be enabled, and only after a documented PASS feasibility gate. Scheduling requires the app/worker active, device awake and internet available. Campaigns, team membership/roles, collaboration, billing, SaaS, cloud scheduling, public API, cloud media relay, additional AI providers/platforms, multi-provider comparison/fallback and advanced social analytics are P1/Future, not MVP requirements.

Windows 11 is the production support and release-validation baseline. Windows 10 may be used for best-effort development continuity only and is not a production support commitment. Keep implementation lightweight and modular for constrained desktop hardware; avoid Redis, Celery, PostgreSQL server, Kubernetes or multiple backend services. One AI provider is sufficient for MVP. One social platform is conditional on real developer access, native/public OAuth security, scopes, review, publishing and local-first media feasibility. If no candidate passes, retain platform-neutral creation and manual export; do not claim automated publishing. Cloud/SaaS architecture and advanced analytics are future scope.
