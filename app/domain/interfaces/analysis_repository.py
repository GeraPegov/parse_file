from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

class IAnalysisRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def tourists_for_all_dates(self) -> dict:
        pass

    @abstractmethod
    async def tourists_for_every_month(self):
        pass