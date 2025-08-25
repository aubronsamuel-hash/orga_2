# Roadmap Coulisses Crew - Pret a deployer (v5)

Ce document resume les jalons pour livrer un MVP pret a deployer.

## Jalon 0 - Socle et arborescence
- Repo init
- Arborescence backend/frontend/docs/CI
- Linters configures
- docker-compose.dev.yml et docker-compose.staging.yml
- Caddyfile.staging
- CI minimal

## Jalon 1 - Backend MVP
- Modeles DB: Technician, Mission, Availability
- Alembic init
- Routers CRUD
- Auth dev
- Seed minimal

## Jalon 2 - Frontend MVP
- Routing, pages de base
- Login mock
- API client
- Tests Vitest

## Jalon 3 - Observabilite
- Logs JSON
- /metrics
- Scripts smoke/logs

## Jalon 4 - CI/CD
- Workflows separes
- Matrices Python/Node
- Docker build

## Jalon 5 - Deploiement staging
- docker-compose.staging
- Caddyfile
- Script deploy_staging.ps1

## Jalon 6 - Securite
- Auth JWT
- Scans
- SECURITY.md, THREAT_MODEL.md
