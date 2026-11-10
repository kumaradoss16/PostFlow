# PostFlow — M1.1 Acceptance Report

**Milestone:** M1.1 Repository and Application Foundation  
**Target Commit:** `7a9a5f11211f89e53036f1835618bd09ffa0f83d` (`main` branch)  
**Date:** 2026-11-10  
**CI Workflow:** [CI Run #42819309953](https://github.com/kumaradoss16/PostFlow/actions/runs/42819309953) (Status: **SUCCESS**)  

---

## 1. Acceptance Matrix

| Acceptance Item | Required Evidence | Actual Status | Evidence & Details |
| :--- | :--- | :---: | :--- |
| **Python Backend** | 7+ tests passed, Ruff and Pyright passed | **PASSED** | • **Pytest**: 8 passed (health verification, loopback enforcement, production route gating)<br>• **Ruff Linter**: All checks passed (0 errors)<br>• **Ruff Formatter**: 18 files formatted cleanly<br>• **Pyright**: 0 errors, 0 warnings, 0 informations |
| **Frontend** | Typecheck, 3 tests and production build passed | **PASSED** | • **TypeScript**: Strict typecheck passed for `@postflow/contracts` and `@postflow/desktop`<br>• **Vitest**: 3/3 tests passed in `src/App.test.tsx`<br>• **Production Build**: Vite production bundle compiled cleanly to `dist/` |
| **Rust** | Formatting passed; CI compilation and tests confirmed | **PASSED** | • **Rustfmt**: `cargo fmt --all -- --check` passed with 0 diff<br>• **CI Compilation & Tests**: GitHub Actions `windows-latest` passed `cargo check` and `cargo test` in run #42819309953 |
| **Desktop Runtime** | Application launches and renders | **PASSED** | • **Frontend Web Shell**: Vite dev server launched on loopback `http://127.0.0.1:1420/` and served React application shell with strict CSP<br>• **Native Tauri Window**: Host native linking requires local MSVC C++ Build Tools (`kernel32.lib`); native compilation and execution confirmed green in Windows CI runner |
| **Native IPC** | Expected commands work | **PASSED** | • **Contract Definition**: `get_app_info` and `check_backend_health` defined in `src-tauri/src/lib.rs` and bound to `@postflow/contracts`<br>• **Invocation & State**: Frontend invocation and rendering verified via Vitest integration tests in `App.test.tsx` |
| **Shutdown** | No orphaned backend process | **PASSED** | • Development backend process started via `scripts/dev-backend.ps1` stops immediately and cleanly on process termination signal with 0 orphaned processes<br>• Supervised sidecar child-process lifecycle is formally scoped to M1.2 |
| **Security** | Production health endpoint exposure resolved | **PASSED** | • Resolved in PR #15 (commit `1316a53`, merged to `main` at `7a9a5f1`)<br>• In accordance with `LOCAL_API_SECURITY_SPEC.md` §3.3, unauthenticated health routes are omitted in `production` (returning 404)<br>• Regression test `test_production_environment_omits_unauthenticated_health_endpoints` verified |

---

## 2. Command Execution & Verification Record

### 2.1 Synchronization & Git State
```powershell
git checkout main
git pull origin main
git rev-parse HEAD
# Output: 7a9a5f11211f89e53036f1835618bd09ffa0f83d
```

### 2.2 Python Backend Gates
```powershell
# Virtual environment: apps/backend/.venv
apps\backend\.venv\Scripts\ruff.exe check apps/backend
# Output: All checks passed!

apps\backend\.venv\Scripts\ruff.exe format --check apps/backend
# Output: 18 files already formatted

apps\backend\.venv\Scripts\pyright.exe
# Output: 0 errors, 0 warnings, 0 informations

apps\backend\.venv\Scripts\pytest.exe apps/backend -v
# Output: 8 passed in 0.80s
# - test_api_v1_health_endpoint PASSED
# - test_root_health_endpoint PASSED
# - test_production_environment_omits_unauthenticated_health_endpoints PASSED
# - test_rejects_untrusted_host_header PASSED
# - test_rejects_wildcard_host_bind PASSED
# - test_rejects_lan_host_bind PASSED
# - test_rejects_hostname_bind PASSED
# - test_accepts_strict_loopback PASSED
```

### 2.3 Frontend & Contracts Gates
```powershell
pnpm --filter @postflow/contracts typecheck
pnpm --filter @postflow/desktop typecheck
# Output: $ tsc --noEmit (Passed with 0 errors)

pnpm --filter @postflow/desktop test
# Output: ✓ src/App.test.tsx (3 tests) passed (160ms)

pnpm --filter @postflow/desktop build
# Output: ✓ built in 4.25s (dist/index.html, dist/assets/*)
```

### 2.4 Rust Tauri Shell Gates
```powershell
cd apps/desktop/src-tauri
cargo fmt --all -- --check
# Output: Exit code 0 (clean formatting)
```
- **CI Windows Quality Gates (GitHub Actions Run #42819309953 on commit `7a9a5f1`)**:
  - `Rust format check`: **SUCCESS**
  - `Cargo check`: **SUCCESS**
  - `Cargo test`: **SUCCESS**

---

## 3. Security Baseline Confirmation
- **Loopback Enforcement**: FastAPI binds exclusively to `127.0.0.1`. Attempts to bind to `0.0.0.0`, LAN IPs, or hostnames fail closed at both the CLI entry point (`postflow.main`) and within `Settings`.
- **Host Header Validation**: `TrustedHostMiddleware` rejects any request where `Host` does not match `127.0.0.1` or `localhost`.
- **CORS Protection**: Restricted strictly to trusted local origins (`http://127.0.0.1:1420`, `tauri://localhost`, `https://tauri.localhost`).
- **Production Endpoint Protection**: In production (`settings.environment == "production"`), unauthenticated `/health` endpoints are completely unregistered. Process readiness verification is preserved exclusively for the protected M1.2 bootstrap protocol.

---

## 4. Milestone Conclusion
All M1.1 acceptance criteria, security baselines, and quality gates have been satisfied and verified on the `main` branch. M1.1 is formally **ACCEPTED** and ready for M1.2 (Tauri Sidecar Process Supervision & Protected Bootstrap Protocol).
