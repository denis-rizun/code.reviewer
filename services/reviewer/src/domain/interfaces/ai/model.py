from abc import ABC, abstractmethod
from typing import ClassVar, Self

from src.domain.type import ExcType, ExcVal, ExcTB


class IAIModel(ABC):
    MAX_TOKENS: ClassVar[int]
    MODEL: ClassVar[str]

    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: ExcType, exc_val: ExcVal, exc_tb: ExcTB) -> None:
        pass

    @abstractmethod
    async def ask(self, prompt: str) -> str:
        pass
