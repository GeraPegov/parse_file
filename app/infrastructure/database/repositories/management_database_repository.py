from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.management_database_repository import (
    IManagementDatabaseRepository,
)
from app.infrastructure.database.models.tourismdata import TourismData


class ManagementDatabaseRepository(IManagementDatabaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def drop_table(self):
        await self.session.execute(delete(TourismData))
        await self.session.commit()

        return {"status": "success drop all"}

    async def create_table(self):
        pass
