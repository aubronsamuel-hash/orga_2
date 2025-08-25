from .models import Availability, Mission


def has_conflict(mission: Mission, slots: list[Availability]) -> bool:
    if mission.start is None or mission.end is None:
        return False
    for slot in slots:
        if slot.start <= mission.start and slot.end >= mission.end:
            return False
    return True
