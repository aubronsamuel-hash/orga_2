from fastapi.testclient import TestClient
from datetime import datetime
from backend.app.main import app
from backend.app.models import Base
from backend.app.db import engine

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_availability_crud():
    t = client.post("/api/v1/technicians", json={"name": "Claire"}).json()
    start = datetime(2025, 8, 28, 8, 0, 0).isoformat()
    end = datetime(2025, 8, 28, 18, 0, 0).isoformat()
    r = client.post("/api/v1/availability", json={"technician_id": t["id"], "start": start, "end": end, "status": "available"})
    assert r.status_code == 201
    aid = r.json()["id"]
    r2 = client.put(f"/api/v1/availability/{aid}", json={"status": "unavailable"})
    assert r2.status_code == 200 and r2.json()["status"] == "unavailable"
    r3 = client.delete(f"/api/v1/availability/{aid}")
    assert r3.status_code == 204
