# Contributing to PostFlow

Thank you for contributing to PostFlow. All contributions must adhere to the engineering standards and architectural invariants set forth in `docs/ENGINEERING_STANDARDS.md` and `docs/IMPLEMENTATION_BASELINE.md`.

## 1. Git Workflow

- Always branch from the latest `main`.
- Branch naming convention:
  - `feat/<short-description>` (new features or milestone foundations)
  - `fix/<short-description>` (bug fixes)
  - `docs/<short-description>` (documentation updates)
  - `chore/<short-description>` (tooling, dependencies)
- Never commit directly to `main`.
- All changes must be submitted via a Pull Request with linked issues and tasks.

## 2. Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):
```text
<type>(<scope>): <imperative summary>

[optional body]

[optional footer]
```

Allowed types:
- `feat`: New feature or milestone implementation
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or correcting tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to our CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `security`: Hardening, vulnerability fixes, secret management

## 3. Mandatory Quality Gates

Before opening a Pull Request, run the local verification suite:
```powershell
.\scripts\verify-all.ps1
```

All Pull Requests must:
1. Pass all lint, format, typecheck, and test checks.
2. Include automated tests (positive and negative security tests where applicable).
3. Strictly preserve architectural trust boundaries:
   - No direct HTTP requests from React.
   - No plaintext secrets or tokens in React, database, or logs.
   - Loopback-only binding (`127.0.0.1`).
   - Strict Content Security Policy.

## 4. Definition of Done
A task is Done only when:
- All acceptance criteria are objectively satisfied.
- Automated tests pass.
- Formatting, linting, and type-checking pass without warnings/errors.
- Security-sensitive behaviors have negative tests.
- Documentation and setup instructions are kept up to date.
- CI pipeline is green.
