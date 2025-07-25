from app.repositories.application_repository import ApplicationRepository
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from uuid import UUID
from typing import List, Optional
from app.models.application import StatusEnum

class ApplicationService:
    def __init__(self, repository: ApplicationRepository):
        self.repository = repository

    async def create_application(self, candidate_id: UUID, data: ApplicationCreate) -> Application:
        application = Application(candidate_id=candidate_id, job_title=data.job_title)
        return await self.repository.create(application)

    async def list_applications(self, candidate_id: UUID, status: Optional[StatusEnum]) -> List[Application]:
        return await self.repository.list_by_candidate(candidate_id, status=status)

    async def update_status(self, application_id: UUID, status: StatusEnum) -> Optional[Application]:
        return await self.repository.update_status(application_id, status)