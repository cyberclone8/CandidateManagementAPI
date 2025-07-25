from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
import enum

class StatusEnum(str, enum.Enum):
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    REJECTED = "REJECTED"
    HIRED = "HIRED"

class Application(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    candidate_id: UUID = Field(foreign_key="candidate.id")
    job_title: str
    status: StatusEnum = Field(default=StatusEnum.APPLIED)
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    candidate: Optional["Candidate"] = Relationship(back_populates="applications")