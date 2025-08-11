from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.presentation.ui.keyboard import KeyboardGetter
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.domain.enums.text import TextEnum

support_router = Router()


@support_router.message(F.text == PathEnum.SUPPORT)
async def support(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=TextEnum.SUPPORT,
        reply_markup=KeyboardGetter.back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})


