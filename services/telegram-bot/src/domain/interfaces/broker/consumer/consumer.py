from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Callable

from src.domain.interfaces.broker.broker import IBroker
# from src.domain.interfaces.broker.consumer import IConsumerFactory


class IConsumer(IBroker, ABC):

    @abstractmethod
    async def consume(
            self,
            topic: str,
            handler: Callable[[str | None, dict], Awaitable[None]],
            # factory: IConsumerFactory | None
            factory: None
    ) -> None:
        pass
