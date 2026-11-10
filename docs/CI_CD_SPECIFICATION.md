# PostFlow — CI/CD Specification

**Status:** Proposed M1 pipeline baseline  
**CI provider:** GitHub Actions  
**Primary runner:** Windows Server 2022/Windows 11-compatible hosted runner (pin the supported image)

## 1. Goals

CI must prove that a clean checkout can be installed, checked, tested and packaged on Windows. Linux-only success is insufficient because Tauri, WebView2, Windows credential integration, sidecar packaging and installer behavior are platform-specific.

M1 CI validates code and produces internal artifacts. It does not deploy a SaaS service or publish public releases automatically.

## 2. Trigger policy

- `pull_request` to `main`: required quality and build gates.
- `push` to `main`: repeat required gates on merged state.
- `workflow_dispatch`: authorized manual full verification and artifact build.
- Scheduled dependency/security scan may run separately.
- Do not run release signing or public release publication on untrusted fork PRs.

Use least-privilege workflow permissions. Pin third-party actions to reviewed immutable commit SHAs. Avoid secrets in fork PR workflows.

## 3. Pipeline stages

| Stage | Checks | Blocking |
|---|---|---|
| 1. Repository hygiene | whitespace, forbidden files, lockfile presence, secret scan | Yes |
| 2. Python | install locked deps, Ruff format/lint, Pyright, Pytest | Yes |
| 3. Frontend | frozen install, Prettier, ESLint, TypeScript, Vitest | Yes |
| 4. Rust | toolchain install, rustfmt, Clippy, Cargo tests | Yes |
| 5. Database | Alembic upgrade fresh DB, populated upgrade, FK/integrity tests | Yes |
| 6. Security | dependency audit, license inventory, secret scan | Yes for critical/high |
| 7. Desktop build | Tauri Windows build with backend sidecar | Yes |
| 8. Packaged smoke | install/launch/health/stop smoke in clean Windows environment | Yes for M1 release |
| 9. Artifact evidence | hashes, logs, SBOM/dependency inventory, test reports | Yes |

## 4. Windows environment

- Use a pinned GitHub-hosted Windows runner image and record it in workflow comments/docs.
- Install Rust stable via `rust-toolchain.toml`.
- Install Node version pinned by repository metadata; use pnpm frozen lockfile.
- Install the pinned Python minor version and project lockfile.
- Install required MSVC Build Tools/Windows SDK dependencies where not present.
- Verify WebView2 runtime availability or install the documented supported runtime.
- Use PowerShell with explicit error handling (`$ErrorActionPreference = 'Stop'`).
- Set deterministic locale/timezone where tests require it.
- Do not assume paths are short, ASCII-only or free of spaces.

## 5. Job design and caching

Separate Python, frontend and Rust checks where possible for clear diagnostics. Cache only dependency stores keyed by lockfile hash, OS and toolchain version. Never cache application secrets, generated databases, mutable build outputs across incompatible toolchains or user data.

Use concurrency groups to cancel superseded PR runs, but do not cancel release verification after it begins.

## 6. Commands and expected gates

Exact commands are finalized with manifests in M1.1; expected gate classes:

```powershell
# Python
ruff format --check backend/src backend/tests
ruff check backend/src backend/tests
pyright backend/src
pytest backend/tests -q

# Frontend
pnpm install --frozen-lockfile
pnpm prettier --check .
pnpm eslint .
pnpm tsc --noEmit
pnpm vitest run

# Rust
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all

# Database
alembic upgrade head
pytest backend/tests/integration/test_migrations.py -q

# Desktop
pnpm tauri build
```

Do not copy commands blindly if project layout differs; update this specification and workflow together.

## 7. Test strategy in CI

- Unit and deterministic integration tests run on every PR.
- SQLite tests use isolated temporary directories and databases.
- API tests verify authentication, origin/host checks and request limits.
- Process tests start and stop the real backend executable where feasible.
- Packaged smoke tests verify the built sidecar and Tauri app, not only Vite dev server.
- No real social publishing or paid AI API calls in routine CI.
- External provider tests, if later approved, run manually with dedicated test credentials in protected environments.

## 8. Build and artifact verification

Build artifacts must:
- contain the expected Tauri app and backend sidecar;
- contain no `.env`, test secrets, developer database or debug-only configuration;
- have a manifest of versions and SHA-256 hashes;
- include third-party license notices;
- launch on a clean Windows 11 VM/user profile without Python installed;
- create data only under the expected user application data directory;
- bind backend to loopback and pass authenticated health check;
- shut down the child process when app exits.

Signing is required before public distribution. CI must not store signing keys in repository variables accessible to untrusted workflows. Use protected environment secrets and an auditable release job.

## 9. Dependency and supply-chain controls

- Commit lockfiles for Python, Node and Rust.
- Review dependency changes and license compatibility.
- Run ecosystem vulnerability scanners; fail on known critical/high vulnerabilities unless a documented exception is approved with expiry and mitigation.
- Generate SBOM or dependency inventory for release candidates.
- Pin GitHub Actions by SHA.
- Do not run untrusted install scripts with elevated privileges.
- Secret scanning is mandatory; any exposed credential triggers rotation, not merely deletion from the latest commit.

## 10. Branch protection

`main` must require:
- PR review;
- all required CI checks;
- no unresolved change requests;
- up-to-date branch before merge where practical;
- no force push or direct push except controlled administrator recovery.

## 11. Failure policy and evidence retention

A failed mandatory job blocks merge. No `continue-on-error` for core lint, type, tests, security or build. Any temporary exception requires an issue, owner, expiry date, risk statement and approval. Retain test reports, build logs, artifact hashes and migration output as workflow artifacts for a defined retention period.

## 12. M1 CI exit criteria

At least one PR and one main-branch run must complete all mandatory jobs on Windows. A clean packaged smoke test must pass. Green unit tests alone do not satisfy M1.