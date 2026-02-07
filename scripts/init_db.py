import asyncio
from pathlib import Path
import sys

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from app.infrastructure.connection import (
    create_database_if_not_exists,
    prod_engine,
)

# BASE_DIR = Path(__file__).parent
# print(BASE_DIR)

async def init_production_db():

    await create_database_if_not_exists('tourism')

    # await create_tables(prod_engine)

    await prod_engine.dispose()

async def init_test_db():
    await create_database_if_not_exists('testtourism')

async def main():
    await init_production_db()
    await init_test_db()

if __name__ == "__main__":
    asyncio.run(main())
