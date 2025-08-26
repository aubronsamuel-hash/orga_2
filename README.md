# Monorepo Coulisses Crew (Backend/Frontend)

## Backend Quickstart (Windows)

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ./backend[dev]
copy .env.example .env
# Dev DB sqlite par defaut. Pour Postgres, editer DATABASE_URL.
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
```

API: http://localhost:8000 (healthz) ; http://localhost:8000/api/v1 (endpoints)

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
