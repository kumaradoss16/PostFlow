# PostFlow

> Single-user, local-first desktop application for creating source content, managing platform variants, AI-assisted generation, managing local media, approving publication revisions, and durable scheduling/publishing.

## 1. Architecture Overview

PostFlow is engineered as a **modular monolith** with strict process and trust boundaries:

```text
PostFlow (Windows Desktop Application)
├── apps/desktop/
│   ├── src/                    # React 18 + TypeScript + Vite (Presentation layer)
│   │                           # Strictly untrusted client; communicates via typed Tauri IPC
│   └── src-tauri/              # Tauri 2 + Rust (Desktop Shell & Lifecycle Authority)
│                               # Process supervision, native OS credential storage, narrow proxy
└── apps/backend/
    └── postflow/               # Python 3.11+ + FastAPI (Modular Monolith Local Backend)
        ├── api/                # Authenticated route handlers & schemas
        ├── application/        # Application use cases & orchestration
        ├── domain/             # Core business rules & validation logic
        ├── infrastructure/     # SQLite / Alembic / Local Filesystem configuration
        ├── integrations/       # In-process adapter interfaces (AI & Social platforms)
        ├── worker/             # Supervised local background job worker
        └── main.py             # Application factory and CLI entry point
```

### Non-Negotiable Invariants
- **Strict Loopback**: The backend listener binds strictly to `127.0.0.1` ephemeral port. Binding to `0.0.0.0`, wildcard, or LAN addresses fails closed.
- **Zero Raw Secret Exposure**: All credentials and tokens are managed via Windows Credential Manager / DPAPI. React JavaScript memory, storage, DOM, and logs never receive raw secret tokens.
- **No Direct HTTP from Frontend**: React interacts strictly via typed Tauri IPC commands. No arbitrary HTTP proxy exists.
- **Strict Content Security Policy**: Denies remote scripts, `unsafe-eval`, and unauthorized navigation/popups.

---

## 2. Prerequisites

- **Windows 11 x64** (production baseline; Windows 10 supported for development).
- **Node.js**: LTS (`>= 20.x`).
- **pnpm**: `pnpm >= 9.x` (`pnpm@12.18.0` pinned).
- **Python**: `3.11` to `3.13`.
- **Rust Toolchain**: `stable-x86_64-pc-windows-msvc` (or `stable-x86_64-pc-windows-gnu`) via `rustup`.

---

## 3. Getting Started

### 3.1 Clone the Repository
```powershell
git clone https://github.com/kumaradoss16/PostFlow.git
cd PostFlow
```

### 3.2 Install Dependencies

#### Frontend & Contracts
```powershell
pnpm install
```

#### Python Backend
```powershell
python -m venv apps/backend/.venv
.\apps\backend\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e "apps/backend[dev]"
```

---

## 4. Running in Development

### Run Backend Engine (Standalone Dev Mode)
```powershell
# Using the helper script:
.\scripts\dev-backend.ps1 -Port 8000

# Or via package command:
pnpm run dev:backend
```

### Run Frontend & Desktop Shell
```powershell
# Start Vite development server
pnpm run dev:desktop

# Or start the full Tauri desktop shell:
pnpm --filter @postflow/desktop tauri dev
```

---

## 5. Verification and Quality Gates

Execute the full suite across all three architectural layers:

```powershell
# Run all automated verification checks:
.\scripts\verify-all.ps1
```

Or run individual verification commands:

| Layer | Check | Command |
|---|---|---|
| **Python Backend** | Linter (Ruff) | `.\apps\backend\.venv\Scripts\ruff.exe check apps/backend` |
| **Python Backend** | Formatter check | `.\apps\backend\.venv\Scripts\ruff.exe format --check apps/backend` |
| **Python Backend** | Test suite (Pytest) | `.\apps\backend\.venv\Scripts\pytest.exe apps/backend` |
| **Python Backend** | Type check (Pyright) | `cd apps/backend; .venv/Scripts/pyright.exe` |
| **Frontend & UI** | Type check | `pnpm run typecheck` |
| **Frontend & UI** | Linting | `pnpm run lint:frontend` |
| **Frontend & UI** | Component tests | `pnpm run test:frontend` |
| **Frontend & UI** | Production build | `pnpm run build` |
| **Rust Desktop Shell** | Cargo check | `cd apps/desktop/src-tauri; cargo check` |
| **Rust Desktop Shell** | Cargo tests | `cd apps/desktop/src-tauri; cargo test` |

---

## 6. Project Milestone Status

- [x] **M1.1 — Repository & Application Foundation**: Tauri 2, React/TypeScript/Vite, and Python/FastAPI scaffolds, strict loopback config, contracts, CI, scripts.
- [ ] **M1.2 — Backend Lifecycle & Supervision**: Supervised child process, protected Windows bootstrap pipe, launch challenge and handshake.
- [ ] **M1.3 — Local API Security & Rust Proxy**: Installation secret provisioning, narrow typed IPC proxy, Host/Origin validation.
- [ ] **M1.4 — SQLite Persistence & Migrations**: SQLAlchemy models, Alembic baseline, workspace/brand entities.
- [ ] **M1.5 — Backup, Restore & Data Lifecycle**: Consistent SQLite backup and verified restore.
- [ ] **M1.6 — Windows Packaging & Release Gates**: Sidecar packaging, clean Windows 11 installation tests.
