from aiogram.fsm.state import StatesGroup, State


class ChatWithUser(StatesGroup):
	text = State()
