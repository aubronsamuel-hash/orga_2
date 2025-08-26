#requires -Version 7
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$BASE="http://localhost:8000/api/v1"
Write-Host "[SEED] Technicians" -ForegroundColor Cyan
$t1 = Invoke-RestMethod -Method Post -Uri "$BASE/technicians" -Body (@{name="Alice";role="Lumiere"} | ConvertTo-Json) -ContentType "application/json"
$t2 = Invoke-RestMethod -Method Post -Uri "$BASE/technicians" -Body (@{name="Bob";role="Son"} | ConvertTo-Json) -ContentType "application/json"

Write-Host "[SEED] Missions" -ForegroundColor Cyan
$m1 = Invoke-RestMethod -Method Post -Uri "$BASE/missions" -Body (@{title="Montage";start="2025-08-28T08:00:00";end="2025-08-28T16:00:00";location="Bobino"} | ConvertTo-Json) -ContentType "application/json"
$m2 = Invoke-RestMethod -Method Post -Uri "$BASE/missions" -Body (@{title="Show Soir";start="2025-08-29T18:00:00";end="2025-08-29T22:00:00";location="Bobino"} | ConvertTo-Json) -ContentType "application/json"

Write-Host "[SEED] Availabilities" -ForegroundColor Cyan
Invoke-RestMethod -Method Post -Uri "$BASE/availability" -Body (@{technician_id=$t1.id;start="2025-08-29T17:00:00";end="2025-08-29T19:00:00";status="unavailable"} | ConvertTo-Json) -ContentType "application/json" | Out-Null
Invoke-RestMethod -Method Post -Uri "$BASE/availability" -Body (@{technician_id=$t2.id;start="2025-08-28T08:00:00";end="2025-08-28T16:00:00";status="available"} | ConvertTo-Json) -ContentType "application/json" | Out-Null

Write-Host "[SEED] Done" -ForegroundColor Green
