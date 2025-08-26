
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/technicians", tags=["technicians"])


@router.get("", response_model=list[schemas.TechnicianOut])
def list_technicians(db: Session = Depends(get_db)):
    return db.query(models.Technician).all()


@router.post("", response_model=schemas.TechnicianOut, status_code=201)
def create_technician(payload: schemas.TechnicianCreate, db: Session = Depends(get_db)):
    t = models.Technician(name=payload.name, role=payload.role)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("/{tech_id}", response_model=schemas.TechnicianOut)
def get_technician(tech_id: int, db: Session = Depends(get_db)):
    t = db.get(models.Technician, tech_id)
    if not t:
        raise HTTPException(404, "Technician not found")
    return t


@router.put("/{tech_id}", response_model=schemas.TechnicianOut)
def update_technician(tech_id: int, payload: schemas.TechnicianUpdate, db: Session = Depends(get_db)):
    t = db.get(models.Technician, tech_id)
    if not t:
        raise HTTPException(404, "Technician not found")
    if payload.name is not None:
        t.name = payload.name
    if payload.role is not None:
        t.role = payload.role
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{tech_id}", status_code=204)
def delete_technician(tech_id: int, db: Session = Depends(get_db)):
    t = db.get(models.Technician, tech_id)
    if not t:
        raise HTTPException(404, "Technician not found")
    db.delete(t)
    db.commit()
    return None
