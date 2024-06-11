from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from loader import bot, db
from .main_router import router
from BotCore.keyboards import ikb
from BotCore.utils.photos_manager import Photo


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()

    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    await bot.send_photo(
        chat_id=message.from_user.id,
        caption="Привет. Здесь ты можешь переписываться с друзьями!",
        photo=(await Photo.file()),
        reply_markup=ikb.start_menu
    )

    await bot.delete_message(message.from_user.id, message.message_id)
