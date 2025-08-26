from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from backend.app.main import app
from backend.app.models import Base
from backend.app.db import engine

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_list_mission_and_ics():
    start = datetime(2025, 8, 29, 18, 0, 0).isoformat()
    end = datetime(2025, 8, 29, 22, 0, 0).isoformat()
    r = client.post("/api/v1/missions", json={"title": "Show Soir", "start": start, "end": end, "location": "Bobino"})
    assert r.status_code == 201
    mid = r.json()["id"]
    r2 = client.get("/api/v1/missions")
    assert r2.status_code == 200 and any(m["id"] == mid for m in r2.json())
    r3 = client.get("/api/v1/missions/exports/ics", params={"range": "2025-08-01,2025-08-31"})
    assert r3.status_code == 200
    assert "BEGIN:VCALENDAR" in r3.text
