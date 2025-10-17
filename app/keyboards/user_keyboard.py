from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import WebAppInfo, CopyTextButton
from dotenv import load_dotenv
import os

load_dotenv()

def get_user_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сайт 🌐", web_app=WebAppInfo(url="https://inaam.ru"))
        ],
        [
            InlineKeyboardButton(text="Почта 📨", copy_text=CopyTextButton(text="info@inaam.ru")),
            InlineKeyboardButton(text="Телефон 📞", copy_text=CopyTextButton(text=os.getenv("PHONE_NUMBER")))
        ],
        [
            InlineKeyboardButton(text="Telegram 💬", url="t.me/oleynik_INAAM")
        ]
    ])