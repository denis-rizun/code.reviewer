from asyncio import CancelledError
from dataclasses import asdict

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from httpx import post

from src.core.constants import Constants
from src.core.logger import Logger
from src.domain.dtos.review import ReviewResponseDTO, ReviewRequestDTO
from src.domain.enums.progress import ProgressTypeEnum
from src.domain.enums.review import ReviewStatusEnum
from src.domain.interfaces.services.polling_handler import IPollingHandler
from src.domain.interfaces.services.review import IReviewService
from src.presentation.ui.keyboard import KeyboardGetter

logger = Logger.setup(__name__)


class ReviewService(IReviewService):

    def __init__(self, message_handler: IPollingHandler) -> None:
        self._message_handler = message_handler

    async def run_review(self, message: Message, state: FSMContext, link: str) -> None:
        try:
            response, msg_to_delete = await self.get_review(
                message=message,
                link=link
            )

            for msg_id in msg_to_delete:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )

            await message.answer(
                text=(
                    f"{Constants.REVIEW_RESULT_TEXT}\n\n"
                    f"{response.data.repository_link}\n\n"
                    f"{response.data.overview}"
                ),
                reply_markup=KeyboardGetter.back()
            )

        except CancelledError:
            raise
        finally:
            await state.clear()

    async def _get_review(
        self,
        message: Message,
        link: str
    ) -> tuple[ReviewResponseDTO, list[int]]:
        logger.info(f"[ReviewService]: Review started for user {message.from_user.id}")
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
            json=asdict(self._get_request_body(user_id, link)),
        )
        return ReviewResponseDTO.validate(response_data.json())

    @classmethod
    def _get_request_body(cls, user_id: int, link: str) -> ReviewRequestDTO:
        return ReviewRequestDTO(
            task_id=f"{user_id}:review",
            repository_link=link,
        )
