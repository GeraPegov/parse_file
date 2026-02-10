from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.services.management_database_service import (
    ManagementDatabaseService,
)
from app.domain.interfaces.management_database_repository import (
    IManagementDatabaseRepository,
)
from app.infrastructure.connection import get_db
from app.infrastructure.database.repositories.management_database_repository import (
    ManagementDatabaseRepository,
)


def get_management_repository(session: AsyncSession = Depends(get_db)):
    return ManagementDatabaseRepository(session)


def get_management_service(
    repo: IManagementDatabaseRepository = Depends(get_management_repository),
):
    return ManagementDatabaseService(repo)
