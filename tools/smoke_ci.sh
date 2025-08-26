#!/usr/bin/env bash
set -euo pipefail

# Exit codes (spec projet)
# 0 OK; 1 USAGE_INVALIDE; 2 PREREQUIS_MANQUANTS; 3 TIMEOUT; 4 ERREUR_RESEAU_API; 10 ERREUR_INTERNE

API_BASE="${API_BASE:-http://127.0.0.1:8000}"
BACKEND_DIR="${BACKEND_DIR:-backend}"
HOST="0.0.0.0"
PORT="${PORT:-8000}"

log() { echo "[SMOKE] $*"; }

if [[ ! -d "${BACKEND_DIR}" ]]; then
  echo "PREREQUIS_MANQUANTS: dossier ${BACKEND_DIR} introuvable." >&2
  exit 2
fi

pushd "${BACKEND_DIR}" >/dev/null

log "Installer deps runtime (si besoin)..."
python -m pip install -U pip >/dev/null

# Uvicorn/FastAPI doivent etre dans le projet; sinon fallback soft:
python -c "import fastapi,uvicorn" 2>/dev/null || python -m pip install fastapi uvicorn >/dev/null

log "Demarrer uvicorn sur ${HOST}:${PORT}..."
python -m uvicorn app.main:app --host "${HOST}" --port "${PORT}" > /tmp/uvicorn.log 2>&1 &
UVICORN_PID=$!
sleep 0.5

cleanup() {
  if ps -p ${UVICORN_PID} >/dev/null 2>&1; then
    kill ${UVICORN_PID} || true
    sleep 0.5
  fi
}
trap cleanup EXIT

log "Attente readiness /healthz (30s max)..."
READY=0
for i in $(seq 1 30); do
  if curl -fsS "${API_BASE}/healthz" >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 1
done

if [[ "${READY}" -ne 1 ]]; then
  echo "TIMEOUT: /healthz indisponible apres 30s." >&2
  echo "==== TAIL uvicorn.log ===="
  tail -n 120 /tmp/uvicorn.log || true
  exit 3
fi
log "OK healthz atteint."

log "Verifier /healthz code 200..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/healthz" || true)
if [[ "${CODE}" != "200" ]]; then
  echo "ERREUR_RESEAU_API: /healthz HTTP ${CODE}" >&2
  exit 4
fi

log "Verifier /api/v1/technicians (200/401/404 acceptes en smoke)..."
CODE2=$(curl -s -o /dev/null -w "%{http_code}" "${API_BASE}/api/v1/technicians" || true)
case "${CODE2}" in
  200|401|403|404) log "OK technicians HTTP ${CODE2}" ;;
  *) echo "ERREUR_RESEAU_API: /api/v1/technicians HTTP ${CODE2}" >&2; exit 4 ;;
esac

log "OK"
exit 0
