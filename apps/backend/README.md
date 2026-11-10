# PostFlow Backend

Python + FastAPI local engine powering PostFlow.

## Architecture
- Strictly bound to loopback `127.0.0.1` ephemeral port.
- Modular monolith design separating API, application use cases, domain models, infrastructure, worker, and integration adapters.
- Supervised by the Tauri desktop shell (M1.2).
- Zero remote or unauthenticated network exposure.

## Development Setup

```powershell
# Create venv and install dependencies
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check
ruff format --check

# Start local development server
python -m postflow.main --port 8000
```
