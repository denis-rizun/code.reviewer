from abc import ABC, abstractmethod

from src.domain.type import ExcTB, ExcVal, ExcType


class IBroker(ABC):

    async def __aenter__(self) -> None:
        await self._start()

    async def __aexit__(self, exc_type: ExcType, exc_val: ExcVal, exc_tb: ExcTB) -> None:
        await self._stop()

    @abstractmethod
    async def _start(self) -> None:
        pass

    @abstractmethod
    async def _stop(self) -> None:
        pass
