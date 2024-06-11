from aiogram import Bot, Dispatcher

from General import cfg
from General.database import DB


bot: Bot = Bot(token=cfg.BOT_TOKEN, parse_mode="HTML")
dp: Dispatcher = Dispatcher()
db: DB = DB(
    cfg.DB_HOST, cfg.DB_PORT, cfg.DB_USER,
    cfg.DB_PASSWORD, cfg.DB_NAME
)
