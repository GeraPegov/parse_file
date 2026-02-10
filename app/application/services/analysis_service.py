import json

from app.domain.interfaces.analysis_repository import IAnalysisRepository


class AnalysisService:
    def __init__(self, repo: IAnalysisRepository):
        self.repo = repo

    async def generate_analysis_report(self):
        coroutines = [
            self.repo.get_tourists_for_all_dates(),
            self.repo.get_tourists_for_every_month(),
            self.repo.get_tourists_for_random_period(),
            self.repo.get_tourists_by_country(),
            self.repo.get_tourists_by_region(),
            self.repo.get_demographic_distribution(),
            self.repo.get_typical_tourist_profile(),
            self.repo.get_most_valuable_segments(),
        ]

        execution_coroutines = [await coroutine for coroutine in coroutines]
        filepath = "analysis_tourism.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                execution_coroutines, f, ensure_ascii=False, default=str, indent=2
            )
        return filepath
