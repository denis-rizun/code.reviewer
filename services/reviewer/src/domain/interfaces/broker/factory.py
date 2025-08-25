from abc import ABC, abstractmethod
from typing import Any


class IFactory(ABC):

    @abstractmethod
    def create(self, **_: Any) -> Any:
        pass
