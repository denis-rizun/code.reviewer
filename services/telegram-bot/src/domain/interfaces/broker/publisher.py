from abc import ABC, abstractmethod

from src.domain.interfaces.broker.broker import IBroker


class IPublisher(IBroker, ABC):

    @abstractmethod
    async def publish(self, topic: str, key: str | None, value: dict) -> None:
        pass
