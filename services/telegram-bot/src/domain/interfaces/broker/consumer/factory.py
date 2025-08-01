from abc import ABC, abstractmethod
from typing import Generic

from src.domain.types import ConsumerType


class IConsumerFactory(ABC, Generic[ConsumerType]):

    @abstractmethod
    def create(self, topic: str, group_id: str) -> ConsumerType:
        pass
