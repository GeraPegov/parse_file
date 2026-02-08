
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.application.services.parse_service import ParseService
from app.domain.interfaces.parse_repository import IParseRepository
from app.infrastructure.connection import get_db
from app.infrastructure.database.repositories.parse_repository import ParseRepository

def get_parse_repo(session: AsyncSession = Depends(get_db)) -> IParseRepository:
    return ParseRepository(session)


def get_parse_service(parse_repo: IParseRepository = Depends(get_parse_repo)):
    return ParseService(parse_repo)

