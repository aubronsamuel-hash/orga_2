from backend.app.schemas import TechnicianCreate
from tests.backend.conftest import get_client


def test_crud_technician() -> None:
    client = get_client()
    res = client.post("/technicians/", json={"name": "T1"})
    assert res.status_code == 200
    tech_id = res.json()["id"]

    res = client.get("/technicians/")
    assert len(res.json()) == 1

    res = client.put(f"/technicians/{tech_id}", json={"name": "T2"})
    assert res.json()["name"] == "T2"

    res = client.delete(f"/technicians/{tech_id}")
    assert res.json()["ok"] is True
