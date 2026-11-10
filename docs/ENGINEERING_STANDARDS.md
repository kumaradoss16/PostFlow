# PostFlow — Engineering Standards

**Status:** Proposed mandatory repository standard  
**Applies to:** all M1 source, tests, build scripts and documentation

## 1. Repository layout

Adopt this monorepo structure. Minor naming changes require architect approval; layer boundaries do not.

```text
PostFlow/
├── apps/
│   └── desktop/
│       ├── src/                    # React UI
│       ├── src-tauri/              # Rust/Tauri commands and lifecycle
│       ├── public/
│       └── package.json
├── apps/
│   ├── backend/
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── migrations/
│   │   │   └── versions/
│   │   ├── src/postflow/
│   │   │   ├── main.py             # app factory entrypoint
│   │   │   ├── api/
│   │   │   ├── application/
│   │   │   ├── domain/
│   │   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   └── security/
│   │   └── tests/
│   │       ├── unit/
│   │       ├── integration/
│   │       └── contract/
│   ├── scripts/
│   ├── docs/
│   ├── .github/workflows/
│   ├── .editorconfig
│   ├── .gitignore
│   ├── .pre-commit-config.yaml
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── README.md
└── README.md
```

Do not create additional deployable services. Rust commands remain thin transport/lifecycle adapters. Route handlers remain thin and delegate to application use cases. Domain rules must not depend on FastAPI, SQLAlchemy, Tauri or vendor SDKs.

## 2. Toolchain and dependency policy

Pin compatible stable versions during M1. Commit lockfiles. Do not use floating dependency ranges for production builds. Record the supported matrix in `docs/ENGINEERING_STANDARDS.md` or a generated toolchain manifest:
- Windows 11 x64 release target;
- Rust stable toolchain via `rust-toolchain.toml`;
- Node LTS selected and pinned by CI;
- pnpm via Corepack/packageManager field;
- Python supported minor version pinned in CI and project metadata;
- MSVC Build Tools / Windows SDK requirements;
- Tauri CLI and WebView2 runtime requirements.

No version is considered approved until a clean Windows CI build proves compatibility.

## 3. Formatting and static analysis

| Area | Required tool | Gate |
|---|---|---|
| Python format | Ruff formatter | `ruff format --check` |
| Python lint | Ruff | `ruff check` |
| Python types | Pyright strict for application modules | CI failure on errors |
| Python tests | Pytest | All required tests pass |
| TS/JS format | Prettier | `prettier --check` |
| TS/JS lint | ESLint with TypeScript rules | `eslint` clean |
| TS types | `tsc --noEmit` | No type errors |
| Frontend tests | Vitest + React Testing Library | Required suite passes |
| Rust format | rustfmt | `cargo fmt --all -- --check` |
| Rust lint | Clippy | `cargo clippy --all-targets --all-features -- -D warnings` |
| Rust tests | Cargo test | All tests pass |
| Desktop build | Tauri CLI | Windows build succeeds |
| Dependency audit | Python/npm/Rust audit tooling | No unresolved critical/high finding |
| Secret scan | GitHub secret scanning or pinned scanner | No secret finding |

Use configuration files in version control; do not rely on editor-local settings.

## 4. Coding rules

### Python
- Type annotations required for public functions and service boundaries.
- Pydantic DTOs at external boundaries; domain objects remain framework-independent.
- Use `pathlib`, explicit timezones and `Decimal` where precision matters.
- Catch expected exceptions; do not use broad `except Exception` as normal control flow.
- Never use `eval`, unsafe deserialization or shell interpolation.
- Use SQLAlchemy parameterized expressions.
- Avoid global mutable state; inject dependencies.
- Keep route handlers thin and side effects explicit.

### TypeScript/React
- `strict: true`; avoid `any`, non-null assertions and type casts without documented justification.
- Components render state; business rules and secrets stay outside UI.
- Use typed IPC DTOs and centralized command wrappers.
- No direct local API calls from React.
- No tokens/secrets in localStorage, sessionStorage, IndexedDB or frontend env.
- Handle loading, unavailable, error and empty states explicitly.
- Avoid unbounded effects, hidden background polling and implicit mutation.

### Rust/Tauri
- Keep commands narrow, typed and allowlisted.
- No arbitrary shell execution or general-purpose HTTP proxy.
- Avoid `unwrap()`/`expect()` on runtime-controlled input or I/O paths.
- Propagate errors with contextual, sanitized categories.
- Minimize Tauri capabilities and plugin permissions.
- Use safe process argument APIs; never construct shell command strings.
- Process handles must be supervised and reaped.

### Database
- All schema changes through Alembic.
- Migrations reviewed and tested against empty and populated DBs.
- Sessions are scoped to one request/use case.
- No network I/O inside DB transactions.
- Constraints enforce key invariants.

## 5. Naming and structure

- Python: `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`.
- TypeScript: components/types `PascalCase`; variables/functions `camelCase`.
- Rust: `snake_case` functions/modules, `PascalCase` types.
- SQL: `snake_case`.
- Tests describe behavior, e.g. `test_rejects_non_loopback_bind`.
- Avoid vague names (`data`, `manager`, `utils`, `common`) unless narrowly scoped and justified.

## 6. Error and logging standards

Errors have stable internal codes and safe user messages. Include correlation IDs. Never return stack traces, SQL, filesystem internals or secrets to UI. Logs are structured and redacted at source. Do not log full user content by default. Avoid logging tokens, headers, credentials, authorization codes, passwords or request bodies.

## 7. Testing standards

- Unit tests for domain decisions and validators.
- Integration tests for DB, migrations, API authentication and process lifecycle.
- Negative security tests for every trust boundary.
- Deterministic fixtures; no network dependency in normal CI.
- External integrations mocked only for contract tests; mock success is not live integration evidence.
- No tests against personal or production accounts.
- Test names must state expected behavior.
- Tests must clean up temporary databases/files/processes.
- Flaky tests are defects; do not quarantine without owner, issue and expiry.

## 8. Git workflow

- Branch from latest `main`; fetch and rebase/update before opening PR.
- Branch names: `feat/<short-description>`, `fix/<short-description>`, `docs/<short-description>`, `chore/<short-description>`.
- Keep PRs focused; avoid unrelated formatting churn.
- Never force-push shared branches without explicit coordination.
- No direct commits to `main`.
- Require review and mandatory CI checks before merge.
- No generated build artifacts, local databases, secrets or environment files in Git.

### Commit convention

Use Conventional Commits:
```text
<type>(<scope>): <imperative summary>

[optional body]

[optional footer]
```
Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `security`. Example: `docs(m1): define backend lifecycle contract`. Breaking changes use `!` and a `BREAKING CHANGE:` footer.

## 9. Pull request requirements

Every PR includes:
- purpose and scope;
- task/acceptance IDs;
- design decisions and alternatives;
- security/privacy impact;
- schema/migration impact;
- test commands and results;
- screenshots or logs where useful;
- known limitations and follow-up issues.

A reviewer must reject hidden scope expansion, undocumented security exceptions, missing migrations, missing negative tests or unverifiable claims.

## 10. Documentation and decisions

Architecture decisions with lasting impact are recorded as ADRs in `docs/adr/NNNN-title.md`. Update source-of-truth docs when implementation changes behavior. Documentation must distinguish approved, proposed, implemented and verified. Never label an untested design as implemented.

## 11. Definition of Done

Code is complete only when it is reviewed, formatted, linted, typed, tested, secure by default, documented, traceable and CI-green. A local developer success that cannot be reproduced from a clean checkout is not Done.