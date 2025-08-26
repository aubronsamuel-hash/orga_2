Param(
    [switch]$Json
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Fail($code, $msg){
    Write-Error $msg
    exit $code
}

Write-Host "== PYTHON =="
if (Test-Path "backend") {
    Push-Location backend
    python -m pip install -U pip setuptools wheel | Out-Host
    python -m pip install -e . | Out-Host
    python -m pip install ruff mypy pytest | Out-Host
    ruff check . | Out-Host
    mypy . | Out-Host
    Pop-Location
} else {
    Fail 2 "PREREQUIS_MANQUANTS: dossier backend manquant."
}

Write-Host "== TESTS PYTHON =="
$env:PYTHONPATH = "backend"
pytest -q | Out-Host

Write-Host "== FRONTEND =="
if (Test-Path "frontend") {
    Push-Location frontend
    if (-not (Test-Path "node_modules")) { npm ci | Out-Host }
    npx eslint . | Out-Host
    npm test --silent | Out-Host
    Pop-Location
} else {
    Fail 2 "PREREQUIS_MANQUANTS: dossier frontend manquant."
}

Write-Host "OK"
exit 0
