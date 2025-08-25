from abc import ABC, abstractmethod


class IReviewerPipeline(ABC):

    @abstractmethod
    async def run(self, key: str, value: dict[str, str]) -> None:
        pass
