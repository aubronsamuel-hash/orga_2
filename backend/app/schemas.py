from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class AvStatus(str, Enum):
    available = "available"
    unavailable = "unavailable"


class TechnicianBase(BaseModel):
    name: str
    role: str | None = None


class TechnicianCreate(TechnicianBase):
    pass


class TechnicianUpdate(BaseModel):
    name: str | None = None
    role: str | None = None


class TechnicianOut(TechnicianBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MissionBase(BaseModel):
    title: str
    start: datetime
    end: datetime
    location: str | None = None

    @field_validator("end")
    @classmethod
    def check_range(cls, v: datetime, info):
        start = info.data.get("start")
        if start and v <= start:
            raise ValueError("end must be after start")
        return v


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    title: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    location: str | None = None


class MissionOut(MissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AvailabilityBase(BaseModel):
    technician_id: int
    start: datetime
    end: datetime
    status: AvStatus

    @field_validator("end")
    @classmethod
    def check_range(cls, v: datetime, info):
        start = info.data.get("start")
        if start and v <= start:
            raise ValueError("end must be after start")
        return v


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityUpdate(BaseModel):
    start: datetime | None = None
    end: datetime | None = None
    status: AvStatus | None = None


class AvailabilityOut(AvailabilityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
