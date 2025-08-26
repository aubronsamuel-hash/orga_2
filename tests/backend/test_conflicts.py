from fastapi.testclient import TestClient
from datetime import datetime
from backend.app.main import app
from backend.app.models import Base
from backend.app.db import engine

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_conflicts_unavailable_overlap():
    t = client.post("/api/v1/technicians", json={"name": "Dan"}).json()
    mid = client.post("/api/v1/missions", json={
        "title": "Test",
        "start": datetime(2025, 8, 29, 18, 0, 0).isoformat(),
        "end": datetime(2025, 8, 29, 22, 0, 0).isoformat(),
        "location": "X"
    }).json()["id"]
    client.post("/api/v1/availability", json={
        "technician_id": t["id"],
        "start": datetime(2025, 8, 29, 17, 0, 0).isoformat(),
        "end": datetime(2025, 8, 29, 19, 0, 0).isoformat(),
        "status": "unavailable"
    })
    r = client.get("/api/v1/availability/conflicts", params={"mission_id": mid})
    assert r.status_code == 200
    assert t["id"] in r.json()["technicians_conflicts"]
