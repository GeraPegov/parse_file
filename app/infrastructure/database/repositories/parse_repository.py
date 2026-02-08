from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.parse_repository import IParseRepository
from app.infrastructure.database.models.tourismdata import TourismData

class ParseRepository(IParseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, records: list[dict]):
        await self.session.execute(
            insert(TourismData)
            .values(records)
        )
        await self.session.commit()