from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from .models import Availability, AvStatus, Mission


def find_unavailability_conflicts(db: Session, mission_id: int) -> list[int]:
    m = db.get(Mission, mission_id)
    if not m:
        return []
    q = (
        db.query(Availability.technician_id)
        .filter(
            Availability.status == AvStatus.unavailable,
            or_(
                and_(Availability.start <= m.start, Availability.end > m.start),
                and_(Availability.start < m.end, Availability.end >= m.end),
                and_(Availability.start >= m.start, Availability.end <= m.end),
            ),
        )
        .distinct()
    )
    return [row[0] for row in q.all()]
