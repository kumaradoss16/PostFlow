# Run PostFlow Backend Tests and Verification
$ErrorActionPreference = "Stop"

$VenvPytest = Join-Path $PSScriptRoot "..\apps\backend\.venv\Scripts\pytest.exe"

if (-not (Test-Path $VenvPytest)) {
    Write-Host "Virtual environment not detected. Running backend setup..."
    & (Join-Path $PSScriptRoot "dev-backend.ps1")
}

Write-Host "Running backend tests with Pytest..."
& $VenvPytest (Join-Path $PSScriptRoot "..\apps\backend") -v
