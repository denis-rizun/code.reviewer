from abc import ABC, abstractmethod

from src.domain.dtos.review import ReviewResponseDTO
from src.domain.type import MessageType


class IReviewService(ABC):

    @abstractmethod
    async def get_review(
        self,
        message: MessageType,
        link: str
    ) -> tuple[ReviewResponseDTO, list[int]]:
        pass
