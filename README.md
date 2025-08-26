# Monorepo Coulisses Crew (Backend/Frontend)

## Quickstart Windows (Backend)

* cd backend
* python -m pip install -U pip setuptools wheel
* python -m pip install -e .
* uvicorn app.main:app --host 0.0.0.0 --port 8000
* Smoke local: `pwsh -NoLogo -NoProfile -File PS1/smoke.ps1`

## CI

* Job Python: lints, types, tests puis `tools/smoke_ci.sh` demarre uvicorn et verifie:

  * GET /healthz => 200
  * GET /api/v1/technicians => 200/401/403/404 acceptes
* Environnement CI Linux: PowerShell indisponible; un script bash est fourni.

### Migrations

```
# Dans le conteneur backend:
docker compose -f docker-compose.dev.yml exec backend bash -lc "alembic revision --autogenerate -m 'change'"
docker compose -f docker-compose.dev.yml exec backend bash -lc "alembic upgrade head"
```

### Seed

```
pwsh PS1/seed.ps1
```

### Tests (backend)

```
pwsh PS1/test_all.ps1
```

Endpoints clefs:

* GET /healthz
* GET /metrics (placeholder)
* POST /api/v1/auth/login
* CRUD /api/v1/technicians
* CRUD /api/v1/missions
* CRUD /api/v1/availability
* GET /api/v1/availability/conflicts?mission_id=ID
* GET /api/v1/missions/exports/ics?range=YYYY-MM-DD,YYYY-MM-DD

## Notes de compatibilite

* Python 3.13: utiliser `psycopg[binary]` en version 3.2.x (>=3.2,<3.3). Les versions 3.1.x n'ont pas de roue precompilee compatible et provoquent un echec `No matching distribution`.
