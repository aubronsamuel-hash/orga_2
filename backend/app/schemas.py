from datetime import datetime
from pydantic import BaseModel


class TechnicianBase(BaseModel):
    name: str


class TechnicianCreate(TechnicianBase):
    pass


class Technician(TechnicianBase):
    id: int

    class Config:
        from_attributes = True


class MissionBase(BaseModel):
    title: str
    technician_id: int | None = None
    start: datetime | None = None
    end: datetime | None = None


class MissionCreate(MissionBase):
    pass


class Mission(MissionBase):
    id: int

    class Config:
        from_attributes = True


class AvailabilityBase(BaseModel):
    technician_id: int
    start: datetime
    end: datetime


class AvailabilityCreate(AvailabilityBase):
    pass


class Availability(AvailabilityBase):
    id: int

    class Config:
        from_attributes = True
