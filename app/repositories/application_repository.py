from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.application import Application, StatusEnum
from uuid import UUID
from typing import List, Optional

class ApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, application: Application) -> Application:
        self.session.add(application)
        await self.session.commit()
        await self.session.refresh(application)
        return application

    async def list_by_candidate(self, candidate_id: UUID, status: Optional[StatusEnum] = None) -> List[Application]:
        stmt = select(Application).where(Application.candidate_id == candidate_id)
        if status:
            stmt = stmt.where(Application.status == status)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, application_id: UUID, status: StatusEnum) -> Optional[Application]:
        result = await self.session.execute(select(Application).where(Application.id == application_id))
        application = result.scalar_one_or_none()
        if application:
            application.status = status
            self.session.add(application)
            await self.session.commit()
            await self.session.refresh(application)
        return application