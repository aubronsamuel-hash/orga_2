import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Technician(Base):
    __tablename__ = "technicians"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)

class Mission(Base):
    __tablename__ = "missions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    start: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)

class AvStatus(str, enum.Enum):
    available = "available"
    unavailable = "unavailable"

class Availability(Base):
    __tablename__ = "availabilities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    technician_id: Mapped[int] = mapped_column(ForeignKey("technicians.id", ondelete="CASCADE"))
    start: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    status: Mapped[AvStatus] = mapped_column(Enum(AvStatus), nullable=False, default=AvStatus.available)

Index("ix_avail_tech_time", Availability.technician_id, Availability.start, Availability.end)
