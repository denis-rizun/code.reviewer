from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from typing import Callable, Any

from src.core.logger import Logger
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum

logger = Logger.setup(__name__)


class CleanupMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if message.text == PathEnum.MAIN:
            return await handler(message, data)

        state = data.get("state")
        if not state:
            return await handler(message, data)

        state_data = await state.get_data()
        last_bot_msg_id = state_data.get(StorageEnum.LAST_BOT_MESSAGE)

        if last_bot_msg_id:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=last_bot_msg_id
                )
            except TelegramBadRequest as e:
                logger.warning(f"[Middleware]: Failed to delete bot message: {e}")

        try:
            await message.delete()
        except TelegramBadRequest as e:
            logger.warning(f"[Middleware]: Failed to delete user message: {e}")

        return await handler(message, data)
