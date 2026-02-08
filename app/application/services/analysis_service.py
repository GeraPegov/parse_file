

from app.domain.interfaces.analysis_repository import IAnalysisRepository


class AnalysisService:
    def __init__(self, repo: IAnalysisRepository):
        self.repo = repo

    async def count_tourist_with_all_time(self):
        return await self.repo.tourists_for_all_dates()
    
    async def count_tourist_with_every_month(self):
        return await self.repo.tourists_for_every_month()
    
    async def count_tourists_for_random_period(self):
        return await self.repo.tourists_for_random_period()
    
    async def count_from_country(self):
        return await self.repo.from_country()
    
    async def count_from_region(self):
        return await self.repo.from_region()
    
    async def demographic_presentation(self):
        return await self.repo.demographic_presentation()
    
    async def average_tourists(self):
        return await self.repo.average_tourists()