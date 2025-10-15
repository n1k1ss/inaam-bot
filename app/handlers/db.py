import asyncpg
import os
from dotenv import load_dotenv

from inaam_bot_logger import logger

load_dotenv()

class Database:
    def __init__(self):
        try:
            self.pool = None
        except Exception as e:
            logger.exception(f"Ошибка в pool [db.py] [{e}]")

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except Exception as e:
            logger.exception(f"Ошибка ввода данных для подключения к БД [db.py] [{e}]")

    async def disconnect(self):
        try:
            await self.pool.close()
        except Exception as e:
            logger.exception(f"Ошибка отключения от БД [db.py] [{e}]")

    async def fetch(self, query, *args):
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetch(query, *args)
        except Exception as e:
            logger.exception(f"Ошибка в fetch [db.py] [{e}]")

    async def fetchrow(self, query, *args):
        try:
            async with self.pool.acquire() as conn:
                return await conn.fetchrow(query, *args)
        except Exception as e:
            logger.exception(f"Ошибка в fetchrow [db.py] [{e}]")

    async def execute(self, query, *args):
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    return await conn.execute(query, *args)
        except Exception as e:
            logger.exception(f"Ошибка в execute [db.py] [{e}]")

db = Database()