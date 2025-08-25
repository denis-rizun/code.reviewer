from abc import abstractmethod
from typing import Callable

from src.domain.interfaces.broker.broker import IBroker
from src.domain.interfaces.broker.factory import IFactory


class IConsumer(IBroker):

    @abstractmethod
    async def consume(
            self,
            topic: str,
            group: str,
            handler: Callable,
            factory: IFactory,
    ) -> None:
        pass

    @abstractmethod
    async def start_consuming(self) -> None:
        pass
