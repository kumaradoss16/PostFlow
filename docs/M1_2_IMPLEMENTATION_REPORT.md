# PostFlow M1.2: Secure Backend Bootstrap Implementation Report

**Milestone:** M1.2 — Secure Backend Bootstrap  
**Branch:** `feat/m1.2-secure-backend-bootstrap`  
**Status:** Completed & Formally Verified  
**Date:** 2026-11-13  
**Target:** Windows Desktop / Tauri 2 + Rust + Python 3.13 FastAPI

---

## 1. Executive Summary

Milestone M1.2 establishes the secure, deterministic, supervised lifecycle for PostFlow's local Python backend engine managed by the native Tauri 2 / Rust desktop shell. 

Direct frontend-to-FastAPI access is eliminated. The backend strictly binds to dynamic IPv4 loopback (`127.0.0.1:0`), authenticates through an OS-level Windows Named Pipe challenge/response protocol, enforces an in-memory activation barrier before accepting any application traffic, and mediates all requests via a narrow, type-safe Rust IPC proxy.

---

## 2. Architecture & Security Invariants

### 2.1 Supervisor Lifecycle State Machine
The Rust supervisor (`postflow_desktop_lib::supervisor`) implements an explicit, observable state machine:
- **`Stopped`**: Initial idle state; no backend process exists.
- **`Starting`**: Process spawned with `--bootstrap-pipe \\.\pipe\postflow-bootstrap-<uuid>`.
- **`Authenticating`**: Awaiting client connection and executing the cryptographic nonce handshake.
- **`Ready`**: Port reported, token active, HTTP requests allowed through proxy.
- **`Degraded`**: Health probe failures or transient network anomalies.
- **`Stopping`**: Graceful shutdown initiated (`POST /api/v1/shutdown`), waiting up to 5s before `child.kill()`.
- **`Failed`**: Handshake timeout (30s), PID spoofing attempt, or process crash.

### 2.2 TOCTOU-Free Dynamic Loopback Allocation
- The Python process binds an ephemeral socket directly to `127.0.0.1:0`.
- The operating system atomically assigns a free port (`bound_port = sock.getsockname()[1]`).
- The socket is passed directly to Uvicorn via `server.run(sockets=[sock])`.
- There is no port-probing race window and no hardcoded port collision risk.

### 2.3 Windows Named Pipe Bootstrap Protocol
- **Transport**: `\\.\pipe\postflow-bootstrap-<uuid>` created with single instance semantics.
- **Process Identity Validation**: Upon connection, Rust queries `GetNamedPipeClientProcessId(pipe_handle)` and asserts it matches the supervised `child.id()`. If any other process attempts connection, it is instantly rejected.
- **Cryptographic Nonce Exchange**:
  1. Supervisor -> Client: `BootstrapInit { protocol_version: 1, challenge_nonce: <32 bytes hex> }`
  2. Client -> Supervisor: `BootstrapReady { echoed_challenge: <challenge_nonce>, port: <u16>, backend_nonce: <32 bytes hex> }` (verified with `subtle::ConstantTimeEq`)
  3. Supervisor -> Client: `BootstrapAuthorize { auth_token: <32 bytes hex>, backend_nonce_ack: <backend_nonce> }`
  4. Client -> Supervisor: `BootstrapAck { status: "active" }`
  5. Pipe is closed; secrets exist solely in memory.

### 2.4 Python Authentication Barrier Middleware (`AuthenticationBarrierMiddleware`)
- **Pre-Activation Gate**: Any request arriving prior to handshake completion is rejected with `503 Service Unavailable` (`{"error": "backend_not_ready"}`).
- **Constant-Time Verification**: All requests must supply `X-PostFlow-Local-Auth`. Tokens are validated with `secrets.compare_digest` to prevent timing attacks.
- **Root `/health` Containment**: Development health check is mounted solely in development/test modes. In production, unauthenticated root `/health` returns 404, while `/api/v1/health` requires valid authentication.

### 2.5 Narrow Rust IPC Proxy
- React does not possess backend credentials or manage HTTP connections.
- Requests pass through `backend_proxy_request` Tauri command:
  - Allowed path prefix: `/api/v1/*` (strictly checked).
  - Path traversal (`..`, `//`, `\`) rejected immediately.
  - Allowed methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.
  - Body payload limit: 1 MB.
  - Response payload limit: 5 MB.
  - Rust injects `X-PostFlow-Local-Auth: <token>` and `Host: 127.0.0.1`.

---

## 3. Verification & Test Evidence

### 3.1 Python Backend Verification
- **Pytest**: 20 passed (100% passing)
  - `test_auth_barrier.py`: 5 passed (lifecycle, 503 before activation, 401 on missing/invalid token, 200 on valid token, OPTIONS preflight)
  - `test_bootstrap_client.py`: 3 passed (complete handshake, protocol version mismatch rejection, nonce tampering rejection)
  - `test_health.py`: 8 passed (production containment, auth barrier enforcement, shutdown endpoint, host header rejection, data leak prevention)
  - `test_security_bind.py`: 4 passed (wildcard rejection, LAN rejection, hostname rejection, strict loopback acceptance)
- **Ruff Linter**: `All checks passed!`
- **Ruff Formatter**: `25 files already formatted`
- **Pyright**: `0 errors, 0 warnings, 0 informations`

### 3.2 Frontend & Contracts Verification
- **Contracts Typecheck**: `tsc --noEmit` passed (0 errors)
- **Desktop Typecheck**: `tsc --noEmit` passed (0 errors)
- **Vitest Suite**: 4 passed
- **Production Vite Build**: Passed (bundle: 162 kB JS, 0.8 kB CSS)

### 3.3 Rust Shell Verification
- **Cargo Format Check**: `cargo fmt --all -- --check` passed cleanly
- **Rust Compiler Gates**: Automated via GitHub Actions Windows CI (`windows-latest`)

---

## 4. M1.2.1 Runtime Hardening & Acceptance Closure

Following internal security and runtime audit review, Milestone M1.2.1 was executed on branch `fix/m1.2-bootstrap-runtime-acceptance` to harden:
1. Windows named-pipe prefix detection (`\\\\.\\pipe\\`).
2. 64-bit ctypes `HANDLE` prototypes and lifecycle management.
3. Named-pipe startup synchronization and bounded connection retry.
4. Active supervisor background monitoring of child process state.
5. Graceful Windows backend shutdown via FastAPI background tasks and Uvicorn lifespan coordination.

For complete audit and acceptance verification details, see [M1_2_1_RUNTIME_HARDENING_REPORT.md](file:///d:/AI/PostFlow/docs/M1_2_1_RUNTIME_HARDENING_REPORT.md).

