from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.presentation.ui.keyboard import KeyboardGetter
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.domain.enums.text import TextEnum

review_router = Router()


@review_router.message(F.text == PathEnum.REVIEW)
async def review(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=TextEnum.REVIEW,
        reply_markup=KeyboardGetter.back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})

