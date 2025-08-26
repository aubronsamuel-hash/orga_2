Param(
  [string]$ApiBase = "http://127.0.0.1:8000",
  [int]$TimeoutSec = 30
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Fail([int]$code, [string]$msg){
  Write-Error $msg
  exit $code
}

if (-not (Test-Path "backend")) { Fail 2 "PREREQUIS_MANQUANTS: dossier backend manquant." }

Push-Location backend
try {
  Write-Host "[SMOKE] Installer deps runtime si besoin..."
  python -m pip install -q -U pip
  try { python -c "import fastapi,uvicorn" | Out-Null } catch { python -m pip install -q fastapi uvicorn }

  Write-Host "[SMOKE] Demarrer uvicorn..."
  $p = Start-Process -FilePath "python" -ArgumentList @("-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000") -PassThru -WindowStyle Hidden
  Start-Sleep -Milliseconds 500

  $ready = $false
  1..$TimeoutSec | ForEach-Object {
    try {
      Invoke-WebRequest -UseBasicParsing -Uri ($ApiBase + "/healthz") -TimeoutSec 3 | Out-Null
      $ready = $true
      break
    } catch { Start-Sleep -Seconds 1 }
  }
  if (-not $ready) {
    Fail 3 "TIMEOUT: /healthz indisponible apres $TimeoutSec s."
  }

  Write-Host "[SMOKE] /healthz doit renvoyer 200"
  $r = Invoke-WebRequest -UseBasicParsing -Uri ($ApiBase + "/healthz") -TimeoutSec 5
  if ($r.StatusCode -ne 200) { Fail 4 "ERREUR_RESEAU_API: /healthz HTTP $($r.StatusCode)" }

  Write-Host "[SMOKE] /api/v1/technicians (200/401/403/404 acceptes)"
  try {
    $r2 = Invoke-WebRequest -UseBasicParsing -Uri ($ApiBase + "/api/v1/technicians") -TimeoutSec 5
    $code = $r2.StatusCode
  } catch {
    $code = $_.Exception.Response.StatusCode.Value__
  }
  if (@(200,401,403,404) -notcontains $code) { Fail 4 "ERREUR_RESEAU_API: /api/v1/technicians HTTP $code" }

  Write-Host "OK"
  exit 0
} finally {
  if ($p) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
  Pop-Location
}
