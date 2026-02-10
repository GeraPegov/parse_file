from typing import Awaitable, Callable, ParamSpec, TypeVar
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    OperationalError,
    ProgrammingError,
    InvalidRequestError,
)

from app.domain.interfaces.parse_repository import IParseRepository
from app.infrastructure.database.models.tourismdata import TourismData

P = ParamSpec("P")
T = TypeVar("T")


def handle_db_errors(
    func: Callable[P, Awaitable[T]],
) -> Callable[P, Awaitable[T | dict[str, str]]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | dict[str, str]:
        try:
            return await func(*args, **kwargs)
        except OperationalError as e:
            return {"error": f"проблемы с подключением: {e}"}
        except ProgrammingError as e:
            return {"error": f"ошибка SQL: {e}"}
        except InvalidRequestError as e:
            return {"error": f"проблемы с сессией: {e}"}
        except Exception as e:
            return {"error": f"неизвестная ошибка: {e}"}

    return wrapper


class ParseRepository(IParseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_db_errors
    async def save(self, records: list[dict]) -> dict:
        await self.session.execute(insert(TourismData).values(records))
        await self.session.commit()

        return {"status": "success"}
