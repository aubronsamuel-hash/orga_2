# Coulisses Crew MVP

## Prerequis
- Python 3.11+
- Node 20
- PowerShell 7
- Docker (pour dev et staging)

## Setup
```
pwsh -NoLogo -NoProfile -File PS1/init_repo.ps1
```

## Developpement
```
pwsh -NoLogo -NoProfile -File PS1/dev_up.ps1
```
Backend: http://localhost:8000/healthz
Frontend: http://localhost:5173

## Tests
```
pwsh -NoLogo -NoProfile -File PS1/test_all.ps1
```

## Smoke
```
pwsh -NoLogo -NoProfile -File PS1/smoke.ps1
```

## Deploiement staging
```
docker compose -f docker-compose.staging.yml up -d
```
