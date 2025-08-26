
from dateutil.parser import isoparse
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=list[schemas.MissionOut])
def list_missions(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(models.Mission).all()


@router.post("", response_model=schemas.MissionOut, status_code=201)
def create_mission(payload: schemas.MissionCreate, db: Session = Depends(get_db)):  # noqa: B008
    m = models.Mission(title=payload.title, start=payload.start, end=payload.end, location=payload.location)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/{mid}", response_model=schemas.MissionOut)
def get_mission(mid: int, db: Session = Depends(get_db)):  # noqa: B008
    m = db.get(models.Mission, mid)
    if not m:
        raise HTTPException(404, "Mission not found")
    return m


@router.put("/{mid}", response_model=schemas.MissionOut)
def update_mission(mid: int, payload: schemas.MissionUpdate, db: Session = Depends(get_db)):  # noqa: B008
    m = db.get(models.Mission, mid)
    if not m:
        raise HTTPException(404, "Mission not found")
    if payload.title is not None:
        m.title = payload.title
    if payload.start is not None:
        m.start = payload.start
    if payload.end is not None:
        m.end = payload.end
    if payload.location is not None:
        m.location = payload.location
    db.commit()
    db.refresh(m)
    return m


@router.delete("/{mid}", status_code=204)
def delete_mission(mid: int, db: Session = Depends(get_db)):  # noqa: B008
    m = db.get(models.Mission, mid)
    if not m:
        raise HTTPException(404, "Mission not found")
    db.delete(m)
    db.commit()
    return None


@router.get("/exports/ics")
def export_ics(range: str | None = None, db: Session = Depends(get_db)):  # noqa: B008
    # range format: YYYY-MM-DD,YYYY-MM-DD
    q = db.query(models.Mission)
    if range:
        a, b = range.split(",")
        start = isoparse(a).replace(tzinfo=None)
        end = isoparse(b).replace(tzinfo=None)
        q = q.filter(models.Mission.start >= start, models.Mission.end <= end)
    items = q.all()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CCW//Missions//EN",
    ]
    for m in items:
        lines += [
            "BEGIN:VEVENT",
            f"UID:mission-{m.id}@ccw",
            f"DTSTART:{m.start.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{m.end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{m.title}",
            f"LOCATION:{m.location or ''}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    body = "\r\n".join(lines)
    return Response(content=body, media_type="text/calendar")
