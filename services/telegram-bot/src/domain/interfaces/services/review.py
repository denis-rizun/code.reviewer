from abc import ABC, abstractmethod

from src.domain.type import MessageType, FSMContextType


class IReviewService(ABC):

    @abstractmethod
    async def run_review(
        self,
        message: MessageType,
        state: FSMContextType,
        link: str
    ) -> None:
        pass
