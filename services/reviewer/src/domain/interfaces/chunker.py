from abc import ABC, abstractmethod


class IChunkerService(ABC):

    @abstractmethod
    def chunk(self, files: dict[str, str], max_tokens: float) -> list[str]:
        pass
