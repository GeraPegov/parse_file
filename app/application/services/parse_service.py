from sqlalchemy.ext.asyncio import AsyncSession


class ParseService:
    def __init__(self, session: AsyncSession):
        self.db_session = session