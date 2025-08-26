from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..conflicts import find_unavailability_conflicts
from ..db import get_db

router = APIRouter(prefix="/availability", tags=["availability"])


@router.get("", response_model=list[schemas.AvailabilityOut])
def list_availability(db: Session = Depends(get_db)):
    return db.query(models.Availability).all()


@router.post("", response_model=schemas.AvailabilityOut, status_code=201)
def create_availability(payload: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    if not db.get(models.Technician, payload.technician_id):
        raise HTTPException(400, "Unknown technician_id")
    a = models.Availability(
        technician_id=payload.technician_id,
        start=payload.start,
        end=payload.end,
        status=models.AvStatus(payload.status.value),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@router.get("/conflicts")
def conflicts(mission_id: int, db: Session = Depends(get_db)):
    tech_ids = find_unavailability_conflicts(db, mission_id)
    return {"mission_id": mission_id, "technicians_conflicts": tech_ids}


@router.get("/{aid}", response_model=schemas.AvailabilityOut)
def get_availability(aid: int, db: Session = Depends(get_db)):
    a = db.get(models.Availability, aid)
    if not a:
        raise HTTPException(404, "Availability not found")
    return a


@router.put("/{aid}", response_model=schemas.AvailabilityOut)
def update_availability(aid: int, payload: schemas.AvailabilityUpdate, db: Session = Depends(get_db)):
    a = db.get(models.Availability, aid)
    if not a:
        raise HTTPException(404, "Availability not found")
    if payload.start is not None:
        a.start = payload.start
    if payload.end is not None:
        a.end = payload.end
    if payload.status is not None:
        a.status = models.AvStatus(payload.status.value)
    db.commit()
    db.refresh(a)
    return a


@router.delete("/{aid}", status_code=204)
def delete_availability(aid: int, db: Session = Depends(get_db)):
    a = db.get(models.Availability, aid)
    if not a:
        raise HTTPException(404, "Availability not found")
    db.delete(a)
    db.commit()
    return None
