from aiogram.fsm.state import StatesGroup, State


class ReviewStates(StatesGroup):
    waiting_for_link = State()
