# Run PostFlow Backend in Development Mode
param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$Reload = $true
)

$ErrorActionPreference = "Stop"

if ($HostAddress -ne "127.0.0.1") {
    Write-Error "Security violation: Host must be '127.0.0.1'. Binding to other interfaces is blocked."
    exit 1
}

$VenvPython = Join-Path $PSScriptRoot "..\apps\backend\.venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating Python virtual environment..."
    python -m venv (Join-Path $PSScriptRoot "..\apps\backend\.venv")
    & $VenvPython -m pip install --upgrade pip
    & (Join-Path $PSScriptRoot "..\apps\backend\.venv\Scripts\pip.exe") install -e (Join-Path $PSScriptRoot "..\apps\backend[dev]")
}

Write-Host "Starting PostFlow backend on http://$HostAddress`:$Port (Development Mode)..."
$BackendArgs = @("--host", $HostAddress, "--port", "$Port")
if ($Reload) {
    $BackendArgs += "--reload"
}
& $VenvPython -m postflow.main @BackendArgs
