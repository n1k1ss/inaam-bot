from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from handlers.only_admin import only_admin_access
from handlers.db import db

from inaam_bot_logger import logger

def register_all_commands_note_handler(dp):
    @dp.message(Command("help"))
    @only_admin_access(db, "admin")
    async def send_packet_with_all_commands(message: Message):
        logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /help")
        await message.delete()
        await message.answer("<blockquote><i>/start</i>\n 🔹 <b>Старт</b> 🤖</blockquote>\n\n<blockquote><i>/id</i>\n 🔹 <b>Отправить ID</b> ✉️</blockquote>\n\n<blockquote><i>/send_req_adm</i>\n 🔹 <b>Запрос на админа</b> 👨‍💼</blockquote>\n\n<blockquote><i>/send_req_wor</i>\n 🔹 <b>Запрос на работника</b> 👨‍💻</blockquote>\n\n<blockquote><i>/addm *ID*</i>\n 🔹 <b>Добавить админа</b> 👨‍💼</blockquote>\n\n<blockquote><i>/removem *ID*</i>\n 🔹 <b>Удалить админа</b> 👨‍💼</blockquote>\n\n<blockquote><i>/add *ID*</i>\n 🔹 <b>Добавить работника</b> 👨‍💻</blockquote>\n\n<blockquote><i>/remove *ID*</i>\n 🔹 <b>Удалить работника</b> 👨‍💻</blockquote>\n\n<blockquote><i>/set *continent / city*</i>\n 🔹 <b>Сменить временную зону бота (\"_\" вместо пробелов в словах)</b></blockquote>", parse_mode=ParseMode.HTML)