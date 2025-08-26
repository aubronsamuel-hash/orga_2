#requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Push-Location (Join-Path $PSScriptRoot "..")
try {
    Write-Host "[TEST] Ruff + mypy + pytest" -ForegroundColor Cyan
    python -m ruff check backend
    python -m mypy backend
    PYTHONPATH=backend pytest -q --cov=backend/app
} finally {
    Pop-Location
}
