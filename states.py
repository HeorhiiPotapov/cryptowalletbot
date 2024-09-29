from aiogram.fsm.state import StatesGroup, State


class EnterAddress(StatesGroup):
    address = State()
