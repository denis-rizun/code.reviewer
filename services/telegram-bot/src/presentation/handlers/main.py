from aiogram import Router, Dispatcher
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.constants import Constants
from src.domain.enums.storage import StorageEnum
from src.presentation.handlers.filters import IsPrivate
from src.presentation.ui.keyboard import KeyboardGetter

main_router = Router()


@main_router.message(CommandStart(), IsPrivate())
async def start(
    message: Message,
    command: CommandObject,
    state: FSMContext,
    dispatcher: Dispatcher
) -> None:
    await state.clear()

    sent = await message.answer(
        text=Constants.INFO_TEXT,
        reply_markup=KeyboardGetter.main_without_back()
    )
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})

    auth_service = dispatcher.workflow_data[StorageEnum.AUTH_SERVICE.value]
    referral_code = command.args or None
    await auth_service.authenticate(ref_code=referral_code, msg=message)
