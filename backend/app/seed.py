from . import models
from .db import SessionLocal


def run() -> None:
    db = SessionLocal()
    t1 = models.Technician(name="Alice")
    t2 = models.Technician(name="Bob")
    db.add_all([t1, t2])
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
