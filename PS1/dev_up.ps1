#requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "[DEV] Compose up (db, redis, backend)" -ForegroundColor Cyan
docker compose -f docker-compose.dev.yml up -d db redis backend

Write-Host "[DEV] Waiting for DB:5432..." -ForegroundColor Cyan

# Simple wait loop

$max=30; $ok=$false
for ($i=0; $i -lt $max; $i++) {
    try {
        $tcp = Test-NetConnection -ComputerName "localhost" -Port 5432
        if ($tcp.TcpTestSucceeded) { $ok=$true; break }
    } catch {}
    Start-Sleep -Seconds 1
}
if (-not $ok) { Write-Error "DB non disponible" ; exit 2 }

Write-Host "[DEV] Alembic upgrade head" -ForegroundColor Cyan
docker compose -f docker-compose.dev.yml exec -T backend bash -lc "alembic upgrade head"

Write-Host "[DEV] Healthz" -ForegroundColor Cyan
curl http://localhost:8000/healthz
