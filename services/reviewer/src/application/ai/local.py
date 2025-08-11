from typing import Self

from src.domain.interfaces.ai.model import IAIModel
from src.domain.type import ExcType, ExcVal, ExcTB


class LocalAIModel(IAIModel):
    MAX_TOKENS = ...
    MODEL = ...

    async def __aenter__(self) -> Self:
        pass

    async def __aexit__(self, exc_type: ExcType, exc_val: ExcVal, exc_tb: ExcTB) -> None:
        pass


    async def ask(self, prompt: str) -> str:
        pass
