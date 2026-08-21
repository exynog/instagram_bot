from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    waiting_username = State()
    waiting_quantity = State()
    confirming = State()
    waiting_receipt = State()