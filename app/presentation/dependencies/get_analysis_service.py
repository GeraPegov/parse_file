
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.application.services.analysis_service import AnalysisService
from app.domain.interfaces.analysis_repository import IAnalysisRepository
from app.infrastructure.connection import get_db
from app.infrastructure.database.repositories.analysis_repository import AnalysisRepository


def get_analysis_repository(
        session: AsyncSession = Depends(get_db)
) -> IAnalysisRepository:
    return AnalysisRepository(session)


def get_analysis_service(
        analysis_repo: IAnalysisRepository = Depends(get_analysis_repository)
) -> AnalysisService:
    return AnalysisService(analysis_repo)