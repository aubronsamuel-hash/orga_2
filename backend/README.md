## Lancer le serveur

* Installation: `python -m pip install -e .`
* Demarrage: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
* Health: `curl http://127.0.0.1:8000/healthz`

## Tests (PS + curl)

### CI (Linux)

bash tools/smoke_ci.sh

### Windows local

pwsh -NoLogo -NoProfile -File PS1/smoke.ps1
