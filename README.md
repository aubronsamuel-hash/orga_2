# Monorepo Coulisses Crew (Backend/Frontend)

## Quickstart Windows

* Python 3.13, Node 20, PowerShell
* Backend:
  * cd backend
  * python -m pip install -U pip setuptools wheel
  * python -m pip install -e .
  * uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
* Frontend:
  * cd frontend && npm ci && npm run dev

## CI

* Backend: pip install -e backend, ruff check backend, mypy backend, pytest (PYTHONPATH=backend)
* Frontend: ESLint v9 (flat config: eslint.config.js), Vitest jsdom (vitest.config.ts + tests/setup.ts)

## Scripts PowerShell

* PS1/test_all.ps1: lance l'ensemble des checks locaux (backend + frontend)
