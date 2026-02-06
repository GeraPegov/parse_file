
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrastructure.config import settings
from sqlalchemy.orm import declarative_base

async def create_database_if_not_exists(db_name: str):
    admin_engine = create_async_engine(
        settings.ADMIN_DB_URL,
        echo=False,
        isolation_level="AUTOCOMMIT"
    )

    try:
        async with admin_engine.connect() as conn:
            result = await conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            exists = result.scalar_one_or_none()

            if not exists:
                if not db_name.replace('_', '').replace('-', '').isalnum():
                    raise ValueError(f"Invalid database name: {db_name}")

                await conn.execute(
                    text(f'CREATE DATABASE "{db_name}"')
                )

    finally:
        await admin_engine.dispose()

async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

prod_engine = create_async_engine(settings.PROD_DB_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=prod_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
    )

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()