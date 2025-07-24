from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.core.database import get_session
from app.repositories.application_repository import ApplicationRepository
from app.services.application_service import ApplicationService
from app.schemas.application import ApplicationCreate, ApplicationRead, ApplicationUpdate
from app.models.application import StatusEnum
from app.core.security import verify_token

router = APIRouter()

def get_service(session: AsyncSession = Depends(get_session)):
    return ApplicationService(ApplicationRepository(session))

@router.post("/candidates/{candidate_id}/applications", response_model=ApplicationRead)
async def apply(candidate_id: UUID, data: ApplicationCreate, service: ApplicationService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.create_application(candidate_id, data)

@router.get("/candidates/{candidate_id}/applications", response_model=List[ApplicationRead])
async def list_applications(candidate_id: UUID, status: Optional[StatusEnum] = None, service: ApplicationService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.list_applications(candidate_id, status)

@router.patch("/applications/{application_id}", response_model=ApplicationRead)
async def update_status(application_id: UUID, data: ApplicationUpdate, service: ApplicationService = Depends(get_service), _: str = Depends(verify_token)):
    return await service.update_status(application_id, data.status)