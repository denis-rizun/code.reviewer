import logging

from aiogram.types import Message
from httpx import post

from src.core.constants import Constants
from src.domain.dtos.review import ReviewResponseDTO
from src.domain.enums.progress import ProgressTypeEnum
from src.domain.enums.review import ReviewStatusEnum
from src.domain.interfaces.services.polling_handler import IPollingHandler
from src.domain.interfaces.services.review import IReviewService

logger = logging.getLogger(__name__)


class ReviewService(IReviewService):

    def __init__(self, message_handler: IPollingHandler) -> None:
        self._message_handler = message_handler

    async def get_review(
        self,
        message: Message,
        link: str
    ) -> tuple[ReviewResponseDTO, list[int]]:
        messages_to_delete = await self._message_handler.show_progress(
            message=message,
            check_status_callback=lambda: self._is_review_ready(
                user_id=message.from_user.id,
                link=link,
            ),
            initial_text=Constants.REVIEW_STARTING_TEXT,
            progress_type=ProgressTypeEnum.REVIEW
        )

        final_response = await self._check_review_status(message.from_user.id, link)
        logger.info(f"[ReviewService]: Review completed for user {message.from_user.id}")

        return final_response, messages_to_delete

    async def _is_review_ready(self, user_id: int, link: str) -> bool:
        response = await self._check_review_status(user_id=user_id, link=link)
        return response.status == ReviewStatusEnum.READY

    async def _check_review_status(self, user_id: int, link: str) -> ReviewResponseDTO:
        response_data = post(
            url=f"{Constants.GATEWAY_URL}/api/v1/review",
            data=self._get_request_body(user_id, link)
        )
        return ReviewResponseDTO.validate(response_data)

    @classmethod
    def _get_request_body(cls, user_id: int, link: str) -> dict:
        return {"task_id": f"{user_id}:review", "repository_link": link}
