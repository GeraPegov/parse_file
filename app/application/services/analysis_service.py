
import json
from app.domain.interfaces.analysis_repository import IAnalysisRepository


class AnalysisService:
    def __init__(self, repo: IAnalysisRepository):
        self.repo = repo

    async def analysis_result(self):
        coroutines = [
            self.repo.tourists_for_all_dates(),
            self.repo.tourists_for_every_month(),
            self.repo.tourists_for_random_period(),
            self.repo.from_country(),
            self.repo.from_region(),
            self.repo.demographic_presentation(),
            self.repo.average_tourists(),
            self.repo.profit_event()
        ]

        data = [await record for record in coroutines]
        print(data)
        with open('analysis_tourism.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, default=str, indent=2)



    