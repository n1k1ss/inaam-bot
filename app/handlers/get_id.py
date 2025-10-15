from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from inaam_bot_logger import logger

def register_get_id_handler(dp: Dispatcher, bot: Bot):
    @dp.message(Command("id"))
    async def get_id(message: Message):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /id")
            await message.delete()

            await message.answer(
                f"⚙️ <b>Ваш ID -</b> <code>{message.from_user.id}</code>",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в в команде /id [get_id.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)