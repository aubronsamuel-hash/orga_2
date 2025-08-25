from datetime import datetime, timedelta

from tests.backend.conftest import get_client


def test_crud_availability() -> None:
    client = get_client()
    t = client.post("/technicians/", json={"name": "T1"}).json()
    payload = {
        "technician_id": t["id"],
        "start": datetime.utcnow().isoformat(),
        "end": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }
    res = client.post("/availability/", json=payload)
    assert res.status_code == 200
    item_id = res.json()["id"]

    res = client.get("/availability/")
    assert len(res.json()) == 1

    res = client.delete(f"/availability/{item_id}")
    assert res.json()["ok"] is True
