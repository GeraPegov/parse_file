
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.application.services.parse_service import TourismService
from app.infrastructure.connection import get_db
from app.infrastructure.database.repositories.tourism_repository import TourismRepository

async def get_tourism_repo(session: AsyncSession = Depends(get_db)):
    return TourismRepository(session)


async def get_tourism_service(tourism_repo: TourismRepository = Depends(get_tourism_repo)):
    return TourismService(tourism_repo)