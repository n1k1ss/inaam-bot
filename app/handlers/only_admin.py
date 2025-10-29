from aiogram.types import Message
from aiogram.enums import ParseMode
from functools import wraps

from inaam_bot_logger import logger

async def is_admin(user_id: int, type: str,  db) -> bool:
    try:
        if type == "admin":
            query = "SELECT 1 FROM main_admin_ids WHERE id = $1"
            row = await db.fetchrow(query, user_id)
            return row is not None

        elif type == "both":
            query = "SELECT id FROM main_admin_ids WHERE id = $1 UNION SELECT id FROM worker_ids WHERE id = $1"
            row = await db.fetchrow(query, user_id)
            return row is not None
    except Exception as e:
        logger.exception(f"Ошибка в функции is_admin [only_admin.py] [{e}]")

def only_admin_access(db, type):
    try:
        def decorator(func):
            @wraps(func)
            async def wrapper(message: Message, *args, **kwargs):
                if not await is_admin(message.from_user.id, type, db):
                    logger.info(f"[{message.from_user.id}] Попытка использовать команду / нажать на кнопку [{message.from_user.first_name}]")
                    await message.delete()
                    await message.answer("🚫 <b>У вас нет доступа к этой команде</b>", parse_mode=ParseMode.HTML)
                    return
                return await func(message, *args, **kwargs)
            return wrapper
        return decorator
    except Exception as e:
        logger.exception(f"Ошибка в функции only_admin_access [only_admin.py] [{e}]")

#