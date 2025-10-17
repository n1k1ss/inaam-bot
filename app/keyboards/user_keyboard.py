from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo, CopyTextButton

def get_user_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сайт 🌐", web_app=WebAppInfo(url="https://inaam.ru"))
        ],
        [
            InlineKeyboardButton(text="Почта 📨", copy_text=CopyTextButton(text="info@inaam.ru")),
            InlineKeyboardButton(text="Телефон 📞", copy_text=CopyTextButton(text="+79852320202"))
        ],
        [
            InlineKeyboardButton(text="Telegram 💬", url="t.me/oleynik_INAAM")
        ]
    ])