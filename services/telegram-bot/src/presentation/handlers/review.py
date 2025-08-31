from asyncio import create_task

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
    task = create_task(
        review_service.run_review(
            message=message,
            state=state,
            link=link
        )
    )
    await state.update_data({"review_task": task})
