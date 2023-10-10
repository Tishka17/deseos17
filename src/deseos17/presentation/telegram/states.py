from aiogram.fsm.state import StatesGroup, State


class CreateWish(StatesGroup):
    text = State()
    preview = State()
