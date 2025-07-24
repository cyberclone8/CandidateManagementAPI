from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.candidate import Candidate
from typing import List, Optional
from uuid import UUID

class CandidateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, candidate: Candidate) -> Candidate:
        self.session.add(candidate)
        await self.session.commit()
        await self.session.refresh(candidate)
        return candidate

    async def get(self, candidate_id: UUID) -> Optional[Candidate]:
        result = await self.session.execute(select(Candidate).where(Candidate.id == candidate_id))
        return result.scalar_one_or_none()

    async def list(self, skill: Optional[str] = None, offset: int = 0, limit: int = 100) -> List[Candidate]:
        stmt = select(Candidate)
        if skill:
            stmt = stmt.where(Candidate.skills.contains([skill]))
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, candidate_id: UUID, updates: dict) -> Optional[Candidate]:
        candidate = await self.get(candidate_id)
        if candidate:
            for k, v in updates.items():
                setattr(candidate, k, v)
            self.session.add(candidate)
            await self.session.commit()
            await self.session.refresh(candidate)
        return candidate