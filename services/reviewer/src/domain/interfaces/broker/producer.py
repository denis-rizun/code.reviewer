from abc import abstractmethod

from src.domain.interfaces.broker.broker import IBroker


class IProducer(IBroker):

    @abstractmethod
    async def send(self, topic: str, key: str | None, value: dict) -> None:
        pass
