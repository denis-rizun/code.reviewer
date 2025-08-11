from abc import ABC, abstractmethod
from typing import Generic

from src.domain.types import MessageType


class IAuthService(ABC, Generic[MessageType]):

    @abstractmethod
    async def authenticate(self, ref_code: str | None, msg: MessageType) -> None:
        pass
