import asyncpg
from typing import List
from datetime import datetime
from asyncpg import Pool, Record
from loguru import logger


class DictRecord(Record):
    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, Record):
            return DictRecord(value)
        return value

    def to_dict(self):
        return self._convert_records_to_dicts(dict(super().items()))

    def _convert_records_to_dicts(self, obj):
        if isinstance(obj, dict):
            return {k: self._convert_records_to_dicts(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_records_to_dicts(item) for item in obj]
        elif isinstance(obj, Record):
            return dict(obj)
        else:
            return obj

    def __repr__(self):
        return str(self.to_dict())


class DB:
    db: Pool

    def __init__(self, host: str, port: int, user: str, password: str, db_name: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._db_name = db_name

    async def close(self) -> None:
        await self.db.close()
        logger.warning("Соединение с базой данных завершено!")

    async def setup(self) -> None:
        self.db = await asyncpg.create_pool(
            host=self._host, port=self._port, user=self._user,
            password=self._password, database=self._db_name,
            record_class=DictRecord, init=self._init_database
        )
        logger.success("Соединение с базой данных успешно установлено!")

    @staticmethod
    async def _init_database(db: asyncpg.Connection) -> None:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS \"users\"(
                _id BIGINT NOT NULL PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT now(),
                updated_at TIMESTAMP DEFAULT now()
        )""")

        await db.execute("SET TIME ZONE 'Europe/Moscow'")

    async def get_user_info(self, user_id: int) -> dict:
        response = await self.db.fetchrow("SELECT * FROM users WHERE _id = $1", user_id)
        return response.to_dict()

    async def add_user(self, user_id: int, username: str, full_name: str) -> dict:
        if not await self.user_existence(user_id):
            response = (
                await self.db.fetchrow(
                    "INSERT INTO users(_id, username, full_name) VALUES($1, $2, $3) RETURNING *",
                    user_id, username, full_name
                )
            ).to_dict()
        else:
            response = await self.get_user_info(user_id)

        return response

    async def update_user_activity(self, user_id: int):
        if await self.user_existence(user_id):
            await self.db.execute("UPDATE users SET updated_at=$1", datetime.now())

    async def user_existence(self, user_id: int) -> bool:
        response = await self.db.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE _id=$1)", int(user_id))
        return response

    async def get_all_users(self) -> List[dict]:
        response = await self.db.fetch("SELECT * FROM users")
        return response
