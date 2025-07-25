from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.models.application import StatusEnum

class ApplicationCreate(BaseModel):
    job_title: str

class ApplicationRead(BaseModel):
    id: UUID
    candidate_id: UUID
    job_title: str
    status: StatusEnum
    applied_at: datetime

    class Config:
        orm_mode = True

class ApplicationUpdate(BaseModel):
    status: Optional[StatusEnum]