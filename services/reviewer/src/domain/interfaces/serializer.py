from abc import ABC, abstractmethod
from typing import Any


class ISerializer(ABC):

    @classmethod
    @abstractmethod
    def serialize(cls, obj: Any) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, obj: bytes) -> Any:
        pass
