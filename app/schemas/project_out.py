from __future__ import annotations

from datetime import datetime

from app.schemas.event_out import  EventOut
from pydantic import BaseModel



class ProjectOut(BaseModel):
    id: int
    client_name: str
    code: str
    created_at: datetime
    event: EventOut

    model_config = {"from_attributes": True}