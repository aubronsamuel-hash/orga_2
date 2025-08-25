from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/availability", tags=["availability"])


@router.post("/", response_model=schemas.Availability)
def create_availability(item: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    obj = models.Availability(**item.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.Availability])
def list_availability(db: Session = Depends(get_db)):
    return db.query(models.Availability).all()


@router.get("/{item_id}", response_model=schemas.Availability)
def get_availability(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Availability, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    return obj


@router.put("/{item_id}", response_model=schemas.Availability)
def update_availability(item_id: int, item: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Availability, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    for key, value in item.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{item_id}")
def delete_availability(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Availability, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}
