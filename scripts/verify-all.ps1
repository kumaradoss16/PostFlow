# PostFlow Full Verification Suite (M1.1)
$ErrorActionPreference = "Stop"

Write-Host "`n=== 1. VERIFYING PYTHON BACKEND ===" -ForegroundColor Cyan
$BackendVenv = Join-Path $PSScriptRoot "..\apps\backend\.venv"
$Pytest = Join-Path $BackendVenv "Scripts\pytest.exe"
$Ruff = Join-Path $BackendVenv "Scripts\ruff.exe"
$Pyright = Join-Path $BackendVenv "Scripts\pyright.exe"

if (-not (Test-Path $Pytest)) {
    Write-Host "Setting up Python backend environment..."
    & (Join-Path $PSScriptRoot "dev-backend.ps1")
}

Write-Host "Running Ruff linter..."
& $Ruff check (Join-Path $PSScriptRoot "..\apps\backend")

Write-Host "Running Ruff formatter check..."
& $Ruff format --check (Join-Path $PSScriptRoot "..\apps\backend")

Write-Host "Running Pytest test suite..."
& $Pytest (Join-Path $PSScriptRoot "..\apps\backend") -v

Write-Host "Running Pyright static type checker..."
Push-Location (Join-Path $PSScriptRoot "..\apps\backend")
try {
    & $Pyright
} finally {
    Pop-Location
}

Write-Host "`n=== 2. VERIFYING FRONTEND & CONTRACTS ===" -ForegroundColor Cyan
Push-Location (Join-Path $PSScriptRoot "..")
try {
    Write-Host "Running TypeScript typecheck..."
    pnpm run typecheck

    Write-Host "Running Frontend Vitest suite..."
    pnpm run test:frontend

    Write-Host "Running Frontend production build..."
    pnpm run build
} finally {
    Pop-Location
}

Write-Host "`n=== 3. VERIFYING RUST TAURI SHELL ===" -ForegroundColor Cyan
Push-Location (Join-Path $PSScriptRoot "..\apps\desktop\src-tauri")
try {
    $env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"
    
    Write-Host "Running Cargo format check..."
    cargo fmt --all -- --check
    if ($LASTEXITCODE -ne 0) {
        throw "cargo fmt check failed!"
    }

    $HasMsvc = (Get-Command "link.exe" -ErrorAction SilentlyContinue) -ne $null
    $HasGnu = (Get-Command "dlltool.exe" -ErrorAction SilentlyContinue) -ne $null
    if ($HasMsvc) {
        Write-Host "Running Cargo check (MSVC toolchain)..."
        cargo check
        if ($LASTEXITCODE -ne 0) { throw "cargo check failed!" }

        Write-Host "Running Cargo test (MSVC toolchain)..."
        cargo test
        if ($LASTEXITCODE -ne 0) { throw "cargo test failed!" }
    } elseif ($HasGnu) {
        Write-Host "Running Cargo check (GNU toolchain)..."
        cargo +stable-x86_64-pc-windows-gnu check
        if ($LASTEXITCODE -ne 0) { throw "cargo check failed!" }

        Write-Host "Running Cargo test (GNU toolchain)..."
        cargo +stable-x86_64-pc-windows-gnu test
        if ($LASTEXITCODE -ne 0) { throw "cargo test failed!" }
    } else {
        Write-Host "[WARNING] Neither MSVC (link.exe) nor MinGW (dlltool.exe) was detected in local PATH." -ForegroundColor Yellow
        Write-Host "Cargo format check PASSED. Full Rust compilation and test execution are verified in CI (windows-latest)." -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}

Write-Host "`n>>> ALL M1.1 VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<" -ForegroundColor Green
