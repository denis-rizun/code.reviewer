from abc import ABC, abstractmethod

from src.domain.type import MessageType


class IAuthService(ABC):

    @abstractmethod
    async def authenticate(self, ref_code: str | None, msg: MessageType) -> None:
        pass
