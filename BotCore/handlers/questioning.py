from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery, Message

from loader import bot, db
from .main_router import router
from BotCore.states.chat_with_user import ChatWithUser


@router.inline_query(F.query == "select_user")
async def select_user(inline_query: InlineQuery) -> None:
    users = await db.get_all_users()

    result = [
        InlineQueryResultArticle(
            id=str(i["_id"]),
            title=i["full_name"],
            description=f"Username: \"{i['username']}\"",
            input_message_content=InputTextMessageContent(message_text=f"Отправить сообщение пользователю {i['_id']}"),
            thumb_width=100,
            thumb_height=100,
        ) for i in users
    ]

    result.reverse()
    await bot.answer_inline_query(inline_query.id, results=result, cache_time=0)


@router.message(F.text, F.via_bot)
async def send_me_text(message: Message, state: FSMContext) -> None:
    user_id = int(message.text.split(" ")[-1])
    await message.answer("Пришлите мне текст для отправки пользователю")
    await state.set_state(ChatWithUser.text)
    await state.update_data({"user_id": user_id})


@router.message(F.text, ChatWithUser.text)
async def send_message_to_user(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    text = message.text
    user_id = state_data["user_id"]
    await bot.send_message(user_id, text + "\n\nОт бота: проверено!")
    await message.answer("Сообщение успешно отправлено пользователю!")
    await state.clear()
