from asyncio import sleep
from typing import Callable, ClassVar

from aiogram.types import Message

from src.core.constants import Constants
from src.domain.enums.progress import ProgressTypeEnum
from src.domain.interfaces.services.polling_handler import IPollingHandler
from src.presentation.ui.keyboard import KeyboardGetter


class PollingMessageHandler(IPollingHandler):
    PROGRESS_TEXT_MAP: ClassVar[dict[ProgressTypeEnum, list[str]]] = {
        ProgressTypeEnum.REVIEW: [
            Constants.REVIEW_WAITING_1_TEXT,
            Constants.REVIEW_WAITING_2_TEXT,
            Constants.REVIEW_WAITING_3_TEXT
        ],
    }
    
    def __init__(self, interval_seconds: int = 45) -> None:
        self._interval_seconds = interval_seconds
    
    async def show_progress(
        self,
        message: Message,
        check_status_callback: Callable,
        initial_text: str,
        progress_type: ProgressTypeEnum
    ) -> list[int]:
        init_msg = await message.answer(
            text=initial_text,
            reply_markup=KeyboardGetter.back()
        )
        
        messages_to_delete = [init_msg.message_id]
        progress_messages = self.PROGRESS_TEXT_MAP[progress_type]
        message_count = 0
        
        while not await check_status_callback():
            if message_count < len(progress_messages):
                msg = await message.answer(text=progress_messages[message_count])
                messages_to_delete.append(msg.message_id)
                message_count += 1

            await sleep(self._interval_seconds)
        
        return messages_to_delete
