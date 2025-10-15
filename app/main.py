from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio
from inaam_bot_logger import logger

from aiogram.types import Message
from aiogram import F

from handlers.command_start import register_start_handler
from handlers.get_id import register_get_id_handler
from handlers.control_main_admins import register_add_main_adm_handler, register_remove_main_adm_handler
from handlers.control_workers import register_add_wor_handler, register_remove_wor_handler
from handlers.send_requests import register_send_request_adm_handler, register_send_request_wor_handler
from handlers.set_time_gmt import register_set_time_gmt_handler
from handlers.all_commands_note import register_all_commands_note_handler
from keyboards.admin_keyboard import register_adm_callbacks

from handlers.db import db

logger.info("Запуск бота")

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

register_start_handler(dp)
register_get_id_handler(dp, bot)
register_add_main_adm_handler(dp, bot)
register_add_wor_handler(dp, bot)
register_remove_wor_handler(dp)
register_remove_main_adm_handler(dp)
register_adm_callbacks(dp, bot)
register_send_request_adm_handler(dp, bot)
register_send_request_wor_handler(dp, bot)
register_set_time_gmt_handler(dp)
register_all_commands_note_handler(dp)

@dp.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(message.photo[-1].file_id)

async def main():
    await db.connect()

    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS main_admin_ids (
                id BIGINT UNIQUE
            )
        """)
        db_main_admin_ids_exists = await db.fetchrow("SELECT 1 FROM main_admin_ids")
        if not db_main_admin_ids_exists:
            await db.execute("INSERT INTO main_admin_ids (id) VALUES ($1)", 7167370884)
    except:
        logger.exception("Ошибка создания БД [main_admin_ids]")

    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS worker_ids (
                id BIGINT UNIQUE
            )
        """)
    except:
        logger.exception("Ошибка создания БД [worker_ids]")

    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS balance (
                amount BIGINT
            )
        """)
        db_balance_exists = await db.fetchrow("SELECT 1 FROM balance")
        if not db_balance_exists:
            await db.execute("INSERT INTO balance (amount) VALUES (0)")
    except:
        logger.exception("Ошибка создания БД [balance]")

    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS balance_expenses (
                doer TEXT,
                doer_username TEXT,
                section TEXT,
                day BIGINT,
                month BIGINT,
                year BIGINT,
                amount BIGINT
            )
        """)
    except:
        logger.exception("Ошибка создания БД [balance_expenses]")

    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS set_time (
                region TEXT
            )
        """)
        db_set_time_exists = await db.fetchrow("SELECT 1 FROM set_time")
        if not db_set_time_exists:
            await db.execute("INSERT INTO set_time (region) VALUES ('America/New_York')")
    except:
        logger.exception("Ошибка создания БД [set_time]")

    try:
        await dp.start_polling(bot)
    except:
        logger.exception("Во время работы бота произошла ошибка")
    finally:
        await db.disconnect()
        logger.info("Отключение бота")

if __name__ == "__main__":
    asyncio.run(main())