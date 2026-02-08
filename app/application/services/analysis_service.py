

from app.domain.interfaces.analysis_repository import IAnalysisRepository


class AnalysisService:
    def __init__(self, repo: IAnalysisRepository):
        self.repo = repo

    async def count_tourist_with_all_time(self):
        return await self.repo.tourists_for_all_dates()
    
    async def count_tourist_with_every_month(self):
        return await self.repo.tourists_for_every_month()