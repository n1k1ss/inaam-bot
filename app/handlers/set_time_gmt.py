from aiogram import Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
from datetime import datetime
import re
import zoneinfo

from handlers.only_admin import only_admin_access
from inaam_bot_logger import logger
from handlers.db import db

def register_set_time_gmt_handler(dp: Dispatcher):
    @dp.message(Command("set"))
    @only_admin_access(db, "admin")
    async def set_time_gmt(message: Message, command: CommandObject):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /set")

            await message.delete()

            if command.args:
                data = command.args.replace(" ", "")

                try:
                    continent, city = re.split(r"[\/,| ]", data)
                except ValueError:
                    continent, city = None, None

                try:
                    tz = zoneinfo.ZoneInfo(f"{continent}/{city}")
                except zoneinfo.ZoneInfoNotFoundError:
                    await message.answer("<b>Не найдено</b> ❌🔍", parse_mode=ParseMode.HTML)
                    logger.exception(f"Ошибка поиска временной зоны [set_time_gmt.py] [{data}]")
                    return

                now = datetime.now(tz)
                str_time = now.strftime("%H:%M")

                await db.execute('UPDATE set_time SET region = $1', f"{continent}/{city}")
                await message.answer(f"🔸<b>{continent}, {city}</b>🔸\n{str_time}", parse_mode=ParseMode.HTML)
            else:
                await message.answer(f"<b>Вы не ввели данные!</b> ⚠️", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /set [set_time_gmt.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)