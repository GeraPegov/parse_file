from app.domain.interfaces.management_database_repository import (
    IManagementDatabaseRepository,
)


class ManagementDatabaseService:
    def __init__(self, repo: IManagementDatabaseRepository):
        self.repo = repo

    async def drop_table(self):
        return await self.repo.drop_table()
