from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import Base
from backend.app.db import engine

client = TestClient(app)

def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_and_get_technician():
    r = client.post("/api/v1/technicians", json={"name":"Alice","role":"Light"})
    assert r.status_code == 201
    tid = r.json()["id"]
    r2 = client.get(f"/api/v1/technicians/{tid}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Alice"

def test_update_and_delete_technician():
    r = client.post("/api/v1/technicians", json={"name":"Bob"})
    tid = r.json()["id"]
    r2 = client.put(f"/api/v1/technicians/{tid}", json={"role":"Sound"})
    assert r2.status_code == 200 and r2.json()["role"] == "Sound"
    r3 = client.delete(f"/api/v1/technicians/{tid}")
    assert r3.status_code == 204
