from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from inaam_bot_logger import logger

def register_send_request_adm_handler(dp: Dispatcher, bot: Bot):
    @dp.message(Command("send_req_adm"))
    async def send_request_adm(message: Message):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} отправил запрос на админа 👨‍💼")
            await message.delete()
            await bot.send_message(7167370884, f"<a href='tg://user?id={message.from_user.id}'><b>{message.from_user.first_name}</b></a>\n\n<i>Запрос на админа</i> 👨‍💼\n\n<code>/addm {message.from_user.id}</code>", parse_mode=ParseMode.HTML)
            await message.answer("<b>Запрос отправлен</b> ✅", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /send_req_adm {[e]}")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

def register_send_request_wor_handler(dp: Dispatcher, bot: Bot):
    @dp.message(Command("send_req_wor"))
    async def send_request_wor(message: Message):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} отправил запрос на работника 👨‍💻")
            await message.delete()
            await bot.send_message(7167370884, f"<a href='tg://user?id={message.from_user.id}'><b>{message.from_user.first_name}</b></a>\n\n<i>Запрос на работника</i> 👨‍💻\n\n<code>/add {message.from_user.id}</code>", parse_mode=ParseMode.HTML)
            await message.answer("<b>Запрос отправлен</b> ✅", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /send_req_wor [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)