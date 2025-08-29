from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.constants import Constants
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.presentation.ui.keyboard import KeyboardGetter

back_router = Router()


@back_router.message(F.text == PathEnum.BACK)
async def back(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=Constants.INFO_TEXT,
        reply_markup=KeyboardGetter.main_without_back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})
