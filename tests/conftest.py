import sys
from pathlib import Path
import pytest_asyncio

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

import asyncio
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import pytest
from app.infrastructure.config import settings
from app.infrastructure.connection import Base
from app.infrastructure.database.models.tourismdata import TourismData

TEST_DATABASE_URL = settings.TEST_DB_URL


@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(url=TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_records(async_session: AsyncSession):
    for i in range(10):
        new_record = TourismData(
            DATE_OF_ARRIVAL=date.today(),
            VISIT_TYPE=f"visit{i}",
            TRIP_TYPE=f"trip type{i}",
            HOME_COUNTRY=f"country{i}",
            HOME_REGION=f"region{i}",
            HOME_CITY=f"city{i}",
            GOAL="Туризм",
            GENDER="gender",
            AGE=f"age{i}",
            INCOME=f"income{i}",
            DAYS_CNT=1,
            VISITORS_CNT=1,
            SPENT=1,
        )
        async_session.add(new_record)

        await async_session.commit()
        await async_session.refresh(new_record)
