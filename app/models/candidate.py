from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

class Candidate(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str
    email: str = Field(unique=True)
    phone: Optional[str] = None
    skills: List[str] = Field(sa_column=Column(JSON),default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    applications: List["Application"] = Relationship(back_populates="candidate")