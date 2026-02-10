from abc import ABC, abstractmethod


class IParseRepository(ABC):
    @abstractmethod
    def __init__(self, session):
        pass

    @abstractmethod
    async def save(self, records: list[dict]):
        pass
