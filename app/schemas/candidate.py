from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str]
    skills: List[str] = []

class CandidateRead(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: Optional[str]
    skills: List[str]
    created_at: datetime

    class Config:
        orm_mode = True

class CandidateUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    skills: Optional[List[str]]