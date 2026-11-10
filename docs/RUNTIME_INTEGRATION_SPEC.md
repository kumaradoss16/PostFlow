# PostFlow — Runtime Integration Specification

**Status:** Proposed; implementation contract for M1  
**Applies to:** Tauri 2 / Rust, React + TypeScript, Python + FastAPI

## 1. Purpose and constraints

This specification defines the process boundary between the native desktop shell and the local Python backend. PostFlow is one desktop application and one supervised backend process—not a distributed system.

The trust model is:
- Rust is the native lifecycle and credential authority.
- React is an untrusted presentation client.
- FastAPI owns application use cases and data access.
- The backend is reachable only through loopback and authenticated native mediation.
- The user must never see a false-ready UI when the backend is unavailable.

## 2. Process topology

Production topology:

```text
PostFlow.exe (Tauri / Rust)
  ├─ React WebView
  │    └─ typed Tauri IPC commands only
  └─ supervised backend sidecar
       └─ FastAPI / Uvicorn on 127.0.0.1:<ephemeral-port>
            └─ SQLite + application data directory
```

Development may launch the backend using the pinned Python environment. Production must launch the packaged sidecar; a developer's Python installation is not a runtime dependency.

## 3. Startup protocol

1. Tauri resolves an absolute, application-owned data directory and creates it with restrictive user-only permissions where Windows permits.
2. Rust loads the installation credential from Windows Credential Manager/DPAPI integration. If absent, it generates at least 256 bits from the OS cryptographic RNG and stores it before proceeding.
3. Rust creates a one-time, bidirectional bootstrap channel using an explicitly inherited Windows pipe handle (or a separately reviewed equivalent). Restrict handle inheritance to the intended child process; do not expose the channel to unrelated child processes.
4. Rust launches the sidecar with explicit arguments, a controlled working directory, minimal environment and no shell interpolation. Pass only non-secret configuration, such as the application data path, through validated arguments or a controlled environment.
5. Backend binds its listener directly to numeric `127.0.0.1` with port `0` (OS-assigned ephemeral port). It must fail closed on any host other than `127.0.0.1`.
6. Backend initializes logging and database connectivity, starts serving, and completes required migrations before declaring readiness.
7. Backend sends a readiness message over the bootstrap channel containing protocol version, actual bound address/port and a fresh process nonce. Do not treat process creation or an open TCP port as readiness.
8. Rust validates that the reported address is exactly `127.0.0.1`, the port is valid and nonzero, the protocol version is supported, and the process nonce matches the current launch. Rust then provisions the installation secret through the protected channel, closes the bootstrap channel and enables the narrow IPC proxy.
9. React receives a typed `backendReady` state through Tauri events/commands. Until then, the UI shows a startup state with bounded timeout and actionable failure.

Startup must be bounded. Define and test a startup deadline (initial target 30 seconds on supported baseline hardware); do not loop indefinitely.

## 4. Port binding and listener ownership

- Bind only to numeric IPv4 loopback `127.0.0.1`; do not use `0.0.0.0`, `::`, hostname `localhost`, LAN interfaces or wildcard hosts.
- The backend asks the OS for an ephemeral port by binding `127.0.0.1:0`; Rust accepts only the validated address reported by the child. This avoids a cross-process socket-reservation handoff and its time-of-check/time-of-use race.
- Backend startup fails closed if configured host is not exactly `127.0.0.1`.
- Backend must report the actual bound socket address; Rust validates it before enabling requests.
- Rust must not independently probe an available port and then ask the backend to bind it.
- Do not expose the port in external deep links, logs or telemetry. Local diagnostic display may show a redacted status, not credentials.
- A port conflict or bind failure is a startup failure; do not silently select a different host or disable authentication.

## 5. Request path

React calls typed Tauri commands, e.g. `workspace_list`, `workspace_create`, `brand_create`. Rust:
1. validates command arguments and applies command-level size/rate limits;
2. constructs a fixed allowlisted backend route/method;
3. attaches the installation authentication credential;
4. sends the request to the verified loopback origin;
5. validates response status/size/schema;
6. returns a typed, sanitized DTO to React.

Do not implement a generic URL, method, header or body forwarding command. Do not let React supply arbitrary backend URLs, auth headers or credential references.

Backend endpoints may be independently tested, but production UI access must use the native proxy. The backend must still authenticate every request; loopback alone is not authentication.

## 6. Shutdown and process supervision

On normal window/app shutdown:
1. Rust marks the application as stopping and rejects new mutating IPC calls.
2. Rust sends an authenticated graceful-shutdown request over the established local channel.
3. Backend stops accepting new work, completes or rolls back bounded in-flight database transactions, closes SQLAlchemy resources and exits.
4. Rust waits a bounded grace period (initial target 5 seconds), then terminates the child if necessary.
5. Rust waits/reaps the process and records a sanitized shutdown outcome.

On unexpected backend exit:
- Rust marks backend unavailable immediately and disables dependent UI actions.
- Rust captures exit code and sanitized diagnostic metadata.
- One bounded restart may be attempted only if startup failure classification indicates transient failure and no in-flight mutation has ambiguous outcome.
- Do not create an infinite restart loop.
- If restart fails, show a recoverable error with logs location and safe recovery guidance.
- Never report an operation successful solely because the frontend sent it before process death.

Application crash/restart recovery is validated by database persistence tests. M1 does not promise background execution while the desktop app is closed or the device sleeps.

## 7. Packaging and deployment

### 7.1 Backend packaging

Candidate: PyInstaller one-folder or one-file sidecar, selected after a packaging spike. Prefer the approach that is diagnosable, reproducible and compatible with native dependencies. The backend artifact must be versioned with the desktop release and included as a Tauri sidecar/resource.

Requirements:
- pin Python and dependency versions;
- generate reproducible build inputs and lockfiles;
- include licenses/notices;
- no secrets in binary, resources, build args or manifests;
- resolve writable data paths from explicit runtime configuration;
- resolve read-only bundled resources from the executable/resource directory;
- test on a clean Windows 11 VM/user profile without Python installed;
- verify Defender/SmartScreen and signing implications before public distribution;
- retain build logs, artifact hashes and SBOM/dependency inventory.

### 7.2 Installer

Tauri packaging produces a signed Windows installer for release candidates. Signing certificate availability is a release-management dependency; unsigned internal artifacts may be used for controlled QA but must not be represented as production-ready.

Installer tests cover fresh install, launch, upgrade, uninstall behavior, user-data preservation policy and clean reinstall. Uninstall must not silently delete user content unless the user explicitly chooses data removal.

## 8. Configuration and filesystem

- Store database, logs, backups and local media under the OS-provided per-user application data directory.
- No writable files in Program Files, installation directory or current working directory.
- Paths must handle spaces, Unicode and long path conditions.
- Apply restrictive ACLs to application-owned directories where supported.
- Do not follow arbitrary symlinks/reparse points during destructive cleanup.
- Separate config from secrets; config contains secret references only.
- Backend must not bind or initialize from environment values that weaken security.

## 9. Version and protocol compatibility

- Desktop and sidecar are released as one compatibility unit.
- Readiness handshake includes protocol version.
- IPC DTOs and backend API schemas are versioned and typed.
- Incompatible protocol versions fail startup rather than guessing.
- Database schema version is managed independently by Alembic.
- App upgrade must run migrations before declaring ready; migration failure leaves the database recoverable and app in a safe unavailable state.

## 10. Runtime observability

Structured logs include timestamp, severity, process role, correlation ID, operation, duration and sanitized error category. Never log tokens, installation secrets, full authorization headers, raw request bodies or sensitive user content. Diagnostic export must be opt-in and reviewed for redaction.

## 11. Required runtime tests

- backend missing/corrupt; startup timeout; wrong protocol version;
- backend attempts non-loopback bind;
- readiness reports wildcard, IPv6, LAN or unexpected address and Rust refuses to enable IPC;
- bootstrap pipe handle inheritance is restricted to the intended backend process;
- port collision and bind failure;
- readiness before database initialization is rejected;
- child process crash while idle and during request;
- graceful shutdown and forced termination;
- duplicate app launch behavior;
- clean packaged install without Python;
- Unicode/spaced data paths;
- upgrade migration failure and recovery;
- no secret in process arguments, environment dump, frontend bundle, logs or diagnostics.

## 12. Open implementation spike

Before committing to a packaging mechanism, produce a short spike report comparing PyInstaller modes and any viable alternative against: native dependency support, startup latency, artifact size, antivirus false positives, clean-machine behavior, debugability, license inventory and upgrade behavior. Product Owner/Lead Architect approval is required for a different packager or runtime topology.