# Run PostFlow Desktop in Development Mode
$ErrorActionPreference = "Stop"

Write-Host "Starting PostFlow Desktop (Vite + Tauri dev mode)..."
Set-Location (Join-Path $PSScriptRoot "..\apps\desktop")
pnpm dev
