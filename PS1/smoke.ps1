#requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Write-Host "[SMOKE] API healthz" -ForegroundColor Cyan
curl http://localhost:8000/healthz
Write-Host "[SMOKE] List missions" -ForegroundColor Cyan
curl http://localhost:8000/api/v1/missions
