from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.presentation.ui.keyboard import KeyboardGetter
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.domain.enums.text import TextEnum

donate_router = Router()


@donate_router.message(F.text == PathEnum.DONATION)
async def donate_menu(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=TextEnum.DONATE,
        reply_markup=KeyboardGetter.back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})
