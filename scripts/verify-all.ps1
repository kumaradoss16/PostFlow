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
    
    # Check if MSVC link.exe is available; if not, use GNU toolchain
    $HasMsvc = (Get-Command "link.exe" -ErrorAction SilentlyContinue) -ne $null
    $CargoCmd = if ($HasMsvc) { "cargo" } else { "cargo +stable-x86_64-pc-windows-gnu" }
    
    Write-Host "Running Cargo check ($CargoCmd)..."
    Invoke-Expression "$CargoCmd check"

    Write-Host "Running Cargo test ($CargoCmd)..."
    Invoke-Expression "$CargoCmd test"
} finally {
    Pop-Location
}

Write-Host "`n>>> ALL M1.1 VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<" -ForegroundColor Green
