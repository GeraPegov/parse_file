from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class IManagementDatabaseRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def drop_table(self):
        pass
