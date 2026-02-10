from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class IAnalysisRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def get_tourists_for_all_dates(self) -> dict:
        pass

    @abstractmethod
    async def get_tourists_for_every_month(self) -> dict:
        pass

    @abstractmethod
    async def get_tourists_for_random_period(self) -> dict:
        pass

    @abstractmethod
    async def get_tourists_by_country(self) -> dict:
        pass

    @abstractmethod
    async def get_tourists_by_region(self) -> dict:
        pass

    @abstractmethod
    async def get_demographic_distribution(self) -> dict:
        pass

    @abstractmethod
    async def get_typical_tourist_profile(self) -> dict:
        pass

    @abstractmethod
    async def get_most_valuable_segments(self) -> dict:
        pass
