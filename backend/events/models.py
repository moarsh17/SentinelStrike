from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.database import Base
from pydantic import BaseModel

def get_utc_now():
    return datetime.now(timezone.utc)

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True) # e.g., "PORT_SCAN", "SSH_BRUTEFORCE"
    src_ip = Column(String)
    dst_ip = Column(String)
    dst_port = Column(Integer, nullable=True)
    severity = Column(String) # "LOW", "MEDIUM", "HIGH"
    status = Column(String, default="NEW") # "NEW", "ACKNOWLEDGED"
    detected_at = Column(DateTime, default=get_utc_now)
    details = Column(String, nullable=True)

from pydantic import BaseModel, field_validator

class EventBase(BaseModel):
    type: str
    src_ip: str
    dst_ip: str
    dst_port: int | None = None
    severity: str
    status: str = "NEW"
    details: str | None = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    detected_at: datetime

    @field_validator('detected_at', mode='before')
    @classmethod
    def force_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True
