from datetime import datetime, timedelta

from tests.backend.conftest import get_client


def test_conflict_detection() -> None:
    client = get_client()
    t = client.post("/technicians/", json={"name": "T1"}).json()
    start = datetime.utcnow()
    slot = {
        "technician_id": t["id"],
        "start": start.isoformat(),
        "end": (start + timedelta(hours=2)).isoformat(),
    }
    client.post("/availability/", json=slot)
    mis = {
        "title": "M1",
        "technician_id": t["id"],
        "start": (start + timedelta(minutes=10)).isoformat(),
        "end": (start + timedelta(minutes=90)).isoformat(),
    }
    mission = client.post("/missions/", json=mis).json()
    res = client.get(f"/missions/conflicts?mission_id={mission['id']}")
    assert res.json() is False
