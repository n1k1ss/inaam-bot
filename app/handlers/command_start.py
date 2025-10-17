from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
import re

from keyboards.admin_keyboard import get_adm_keyboard, get_wor_keyboard
from keyboards.user_keyboard import get_user_keyboard
from handlers.db import db
from handlers.get_current_balance import get_current_balance

from inaam_bot_logger import logger

def register_start_handler(dp: Dispatcher):
    @dp.message(CommandStart())
    async def start(message: Message):
        try:
            await message.delete()

            row_main = await db.fetchrow('SELECT 1 FROM main_admin_ids WHERE id=$1', message.from_user.id)
            row_worker = await db.fetchrow('SELECT 1 FROM worker_ids WHERE id=$1', message.from_user.id)

            position = (
                "<i>Руководитель</i> 👨‍💼" if row_main else
                "<i>Работник</i> 👨‍💻" if row_worker else
                None
            )

            if position != None:
                if row_main:
                    keyboard = get_adm_keyboard()
                elif row_worker:
                    keyboard = get_wor_keyboard()

                logger.info(f"[{message.from_user.id}] {message.from_user.first_name} запустил бота [Роль: {re.sub(r"</?i>", "", position)}]")

                current_balance = await get_current_balance()

                await message.answer(
                    f"<b>Привет, {message.from_user.first_name}</b> 👋\n<b>Роль:</b> {position}\n💸 <b>Баланс:</b> <i>{current_balance}₽</i>",
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML
                )

            else:
                logger.info(f"[{message.from_user.id}] {message.from_user.first_name} запустил бота [Роль: Пользователь 🙎‍♂️]")

                keyboard_user = get_user_keyboard()

                await message.answer(
                    f"<b>Привет, {message.from_user.first_name}</b> 👋",
                    reply_markup=keyboard_user,
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /start [command_start.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)