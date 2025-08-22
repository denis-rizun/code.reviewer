from abc import ABC, abstractmethod


class IReviewerService(ABC):

    @abstractmethod
    async def review(self, link: str) -> str:
        pass
