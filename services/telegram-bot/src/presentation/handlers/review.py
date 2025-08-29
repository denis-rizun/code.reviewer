from aiogram import Router, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.constants import Constants
from src.domain.enums.path import PathEnum
from src.domain.enums.storage import StorageEnum
from src.presentation.states import ReviewStates
from src.presentation.ui.keyboard import KeyboardGetter

review_router = Router()


@review_router.message(F.text == PathEnum.REVIEW)
async def review_start(message: Message, state: FSMContext) -> None:
    sent = await message.answer(
        text=Constants.REVIEW_REQUEST_TEXT,
        reply_markup=KeyboardGetter.back()
    )

    await state.set_state(ReviewStates.waiting_for_link)
    await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})


@review_router.message(ReviewStates.waiting_for_link, F.text)
async def review_process_link(
    message: Message,
    state: FSMContext,
    dispatcher: Dispatcher
) -> None:
    link = message.text
    if not link.startswith('https://'):
        sent = await message.answer(
            text=Constants.REVIEW_INCORRECT_LINK_TEXT,
            reply_markup=KeyboardGetter.back()
        )
        await state.update_data({StorageEnum.LAST_BOT_MESSAGE: sent.message_id})
        return

    await state.clear()
    review_service = dispatcher.workflow_data[StorageEnum.REVIEW_SERVICE.value]
    response, messages_to_delete = await review_service.get_review(message=message, link=link)

    for msg_id in messages_to_delete:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

    await message.answer(
        text=(
            f"{Constants.REVIEW_RESULT_TEXT}\n\n"
            f"{response.data.repository_link}\n\n"
            f"{response.data.rating}"
        ),
        reply_markup=KeyboardGetter.back()
    )
