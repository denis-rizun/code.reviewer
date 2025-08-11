from abc import ABC, abstractmethod


class IChunker(ABC):

    @abstractmethod
    def chunk(self, files: dict[str, str], max_tokens: int) -> None:
        pass
