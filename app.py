import asyncio
from loguru import logger

from loader import bot, dp, db
from BotCore.handlers.main_router import router
from BotCore.middlewares.update_users import UpdateUsersMiddleware


async def on_startup() -> None:
    await db.setup()
    logger.success("Бот успешно запущен!")


async def on_shutdown() -> None:
    await db.close()
    logger.warning("Бот выключен!")


async def register_middlewares() -> None:
    dp.message.middleware(UpdateUsersMiddleware())
    dp.callback_query.middleware(UpdateUsersMiddleware())
    dp.inline_query.middleware(UpdateUsersMiddleware())


async def main() -> None:
    dp.include_router(router)
    await register_middlewares()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
