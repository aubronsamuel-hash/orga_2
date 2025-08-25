from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..conflicts import has_conflict
from ..db import get_db

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=schemas.Mission)
def create_mission(mis: schemas.MissionCreate, db: Session = Depends(get_db)):
    obj = models.Mission(**mis.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.Mission])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()


@router.get("/conflicts", response_model=bool)
def check_conflicts(mission_id: int, db: Session = Depends(get_db)):
    mission = db.get(models.Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="not found")
    slots = (
        db.query(models.Availability)
        .filter(models.Availability.technician_id == mission.technician_id)
        .all()
    )
    return has_conflict(mission, slots)


@router.get("/{mis_id}", response_model=schemas.Mission)
def get_mission(mis_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Mission, mis_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    return obj


@router.put("/{mis_id}", response_model=schemas.Mission)
def update_mission(mis_id: int, mis: schemas.MissionCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Mission, mis_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    for key, value in mis.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{mis_id}")
def delete_mission(mis_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Mission, mis_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}
