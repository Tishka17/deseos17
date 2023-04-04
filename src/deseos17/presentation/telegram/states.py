from aiogram.fsm.state import StatesGroup, State


class NewWish(StatesGroup):
    text = State()
    preview = State()
