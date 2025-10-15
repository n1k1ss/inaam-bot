from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode

from handlers.db import db
from handlers.only_admin import only_admin_access
from keyboards.admin_keyboard import get_confirm_adding_new_main_adm
from inaam_bot_logger import logger

def register_add_main_adm_handler(dp: Dispatcher, bot):
    @dp.message(Command("addm"))
    @only_admin_access(db, "admin")
    async def add_main_adm(message: Message, command: CommandObject):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /addm")
            await message.delete()
            new_main_adm_id = command.args
            if new_main_adm_id:
                if new_main_adm_id != "7167370884":
                    try:
                        photos = await bot.get_user_profile_photos(user_id=new_main_adm_id, limit=1)
                        avatar_file_id = photos.photos[0][-1].file_id if photos.total_count > 0 else None
                        chat = await bot.get_chat(new_main_adm_id)
                        first_name = chat.first_name

                        if avatar_file_id:

                            await message.answer_photo(
                                photo=avatar_file_id,
                                caption=f"<a href='tg://user?id={new_main_adm_id}'><b>{first_name}</b></a>\n<b>Роль:</b> <i>Администратор</i> 👨‍💼",
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_confirm_adding_new_main_adm(new_main_adm_id)
                            )
                        else:
                            await message.answer_photo(
                                photo="AgACAgIAAxkBAAIDBWjglFY3fd-ZP7_NvWkAAe_HzO6DlAAC5vQxG7r9CEuIFuHWYcTuEgEAAwIAA20AAzYE",
                                caption=f"<a href='tg://user?id={new_main_adm_id}'><b>{first_name}</b></a>\n<b>Роль:</b> <i>Администратор</i> 👨‍💼",
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_confirm_adding_new_main_adm(new_main_adm_id))
                    except:
                        await message.answer("<b>Пользователь не найден</b> 🤷‍♂️", parse_mode=ParseMode.HTML)
                else:
                    await message.answer("<b>Создателю нельзя изменить роль</b> 🔏", parse_mode=ParseMode.HTML)
            else:
                await message.answer("<b>ID не был введен!</b> ❌", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /addm [control_main_admins.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

def register_remove_main_adm_handler(dp: Dispatcher):
    @dp.message(Command("removem"))
    @only_admin_access(db, "admin")
    async def remove_main_adm(message: Message, command: CommandObject):
        try:
            logger.info(f"[{message.from_user.id}] {message.from_user.first_name} вызвал команду /removem")
            await message.delete()
            past_main_adm_id = command.args
            if past_main_adm_id:
                if past_main_adm_id != "7167370884":
                    person_to_remove = await db.fetchrow('SELECT 1 FROM main_admin_ids WHERE id=$1', int(past_main_adm_id))
                    if person_to_remove:
                        await db.execute('DELETE FROM main_admin_ids WHERE id=$1', int(past_main_adm_id))
                        await message.answer("<b>Удален</b> 🗑", parse_mode=ParseMode.HTML)
                    else:
                        await message.answer("<b>Человек и так не админ</b> ❌", parse_mode=ParseMode.HTML)
                else:
                    await message.answer("<b>Создателю нельзя изменить роль</b> 🔏", parse_mode=ParseMode.HTML)
            else:
                await message.answer("<b>ID не был введен!</b> ❌", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в команде /removem [control_main_admins.py] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)