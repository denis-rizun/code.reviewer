from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.constants import Constants
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.presentation.ui.keyboard import KeyboardGetter

donate_router = Router()


@donate_router.message(F.text == PathEnum.DONATION)
async def donate_menu(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=Constants.DONATE_TEXT,
        reply_markup=KeyboardGetter.back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})
