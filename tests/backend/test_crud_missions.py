from datetime import datetime, timedelta

from tests.backend.conftest import get_client


def test_crud_mission() -> None:
    client = get_client()
    t = client.post("/technicians/", json={"name": "T1"}).json()
    payload = {
        "title": "M1",
        "technician_id": t["id"],
        "start": datetime.utcnow().isoformat(),
        "end": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }
    res = client.post("/missions/", json=payload)
    assert res.status_code == 200
    mis_id = res.json()["id"]

    res = client.get(f"/missions/{mis_id}")
    assert res.status_code == 200

    res = client.delete(f"/missions/{mis_id}")
    assert res.json()["ok"] is True
