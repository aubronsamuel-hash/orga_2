from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/technicians", tags=["technicians"])


@router.post("/", response_model=schemas.Technician)
def create_technician(tech: schemas.TechnicianCreate, db: Session = Depends(get_db)):
    obj = models.Technician(name=tech.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.Technician])
def list_technicians(db: Session = Depends(get_db)):
    return db.query(models.Technician).all()


@router.get("/{tech_id}", response_model=schemas.Technician)
def get_technician(tech_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Technician, tech_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    return obj


@router.put("/{tech_id}", response_model=schemas.Technician)
def update_technician(tech_id: int, tech: schemas.TechnicianCreate, db: Session = Depends(get_db)):
    obj = db.get(models.Technician, tech_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    obj.name = tech.name
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{tech_id}")
def delete_technician(tech_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Technician, tech_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}
