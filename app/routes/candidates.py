from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import aioredis
import json

from app.core.database import get_session
from app.repositories.candidate_repository import CandidateRepository
from app.services.candidate_service import CandidateService
from app.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate
from app.core.security import verify_token

router = APIRouter(prefix="/candidates")

def get_service(session: AsyncSession = Depends(get_session)):
    return CandidateService(CandidateRepository(session))

@router.post("", response_model=CandidateRead)
async def create_candidate(data: CandidateCreate, service: CandidateService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.create_candidate(data)

@router.get("", response_model=List[CandidateRead])
async def list_candidates(
    skill: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    service: CandidateService = Depends(get_service),
    _: str = Depends(verify_token)
):
    return await service.list_candidates(skill, offset, limit)

@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(candidate_id: UUID, service: CandidateService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.get_candidate(candidate_id)

@router.put("/{candidate_id}", response_model=CandidateRead)
async def update_candidate(candidate_id: UUID, data: CandidateUpdate, service: CandidateService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.update_candidate(candidate_id, data)

@router.post("/{candidate_id}/enqueue-task")
async def enqueue_candidate_task(candidate_id: UUID, _: str = Depends(verify_token)):
    redis = aioredis.from_url("redis://redis")
    payload = {"candidate_id": str(candidate_id)}
    await redis.rpush("candidate:processing_queue", json.dumps(payload))
    return {"message": "Task enqueued"}