from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models
from db.database import get_db

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[models.EventResponse])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(models.EventModel).order_by(models.EventModel.detected_at.desc()).offset(skip).limit(limit).all()
    return events
