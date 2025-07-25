from app.repositories.candidate_repository import CandidateRepository
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from uuid import UUID
from typing import List, Optional

class CandidateService:
    def __init__(self, repository: CandidateRepository):
        self.repository = repository

    async def create_candidate(self, data: CandidateCreate) -> Candidate:
        candidate = Candidate(**data.dict())
        return await self.repository.create(candidate)

    async def get_candidate(self, candidate_id: UUID) -> Optional[Candidate]:
        return await self.repository.get(candidate_id)

    async def list_candidates(self, skill: Optional[str], offset: int, limit: int) -> List[Candidate]:
        return await self.repository.list(skill=skill, offset=offset, limit=limit)

    async def update_candidate(self, candidate_id: UUID, data: CandidateUpdate) -> Optional[Candidate]:
        updates = data.dict(exclude_unset=True)
        return await self.repository.update(candidate_id, updates)