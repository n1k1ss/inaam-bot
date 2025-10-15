from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode

from handlers.db import db
from handlers.only_admin import only_admin_access
from keyboards.admin_keyboard import get_confirm_adding_new_wor
from inaam_bot_logger import logger

def register_add_wor_handler(dp: Dispatcher, bot):
    @dp.message(Command("add"))
    @only_admin_access(db, "admin")
    async def add_main_adm(message: Message, command: CommandObject):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /add")
            await message.delete()
            new_wor_id = command.args
            if new_wor_id:
                if new_wor_id != "7167370884":
                    try:
                        photos = await bot.get_user_profile_photos(user_id=new_wor_id, limit=1)
                        avatar_file_id = photos.photos[0][-1].file_id if photos.total_count > 0 else None
                        chat = await bot.get_chat(new_wor_id)
                        first_name = chat.first_name

                        if avatar_file_id:

                            await message.answer_photo(
                                photo=avatar_file_id,
                                caption=f"<a href='tg://user?id={new_wor_id}'><b>{first_name}</b></a>\n<b>Роль:</b> <i>Работник</i> 👨‍💻",
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_confirm_adding_new_wor(new_wor_id)
                            )
                        else:
                            await message.answer_photo(
                                photo="AgACAgIAAxkBAAIDBWjglFY3fd-ZP7_NvWkAAe_HzO6DlAAC5vQxG7r9CEuIFuHWYcTuEgEAAwIAA20AAzYE",
                                caption=f"<a href='tg://user?id={new_wor_id}'><b>{first_name}</b></a>\n<b>Роль:</b> <i>Работник</i> 👨‍💻",
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_confirm_adding_new_wor(new_wor_id))
                    except:
                        await message.answer("<b>Пользователь не найден</b> 🤷‍♂️", parse_mode=ParseMode.HTML)
                else:
                    await message.answer("<b>Создателю нельзя изменить роль</b> 🔏", parse_mode=ParseMode.HTML)
            else:
                await message.answer("<b>ID не был введен!</b> ❌", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /add [control_workers.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

def register_remove_wor_handler(dp: Dispatcher):
    @dp.message(Command("remove"))
    @only_admin_access(db, "admin")
    async def remove_main_adm(message: Message, command: CommandObject):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /remove")
            await message.delete()
            past_wor_id = command.args
            if past_wor_id:
                if past_wor_id != "7167370884":
                    person_to_remove = await db.fetchrow('SELECT * FROM worker_ids WHERE id=$1', int(past_wor_id))
                    if person_to_remove:
                        await db.execute('DELETE FROM worker_ids WHERE id=$1', int(past_wor_id))
                        await message.answer("<b>Удален</b> 🗑", parse_mode=ParseMode.HTML)
                    else:
                        await message.answer("<b>Человек и так не работник</b> ❌", parse_mode=ParseMode.HTML)
                else:
                    await message.answer("<b>Создателю нельзя изменить роль</b> 🔏", parse_mode=ParseMode.HTML)
            else:
                await message.answer("<b>ID не был введен!</b> ❌", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /remove [control_workers.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)