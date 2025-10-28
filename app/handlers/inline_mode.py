from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os
from inaam_bot_logger import logger

load_dotenv()

def register_inline_mode_handler(dp):
    @dp.inline_query()
    async def inline_mode(inline_query: InlineQuery):
        inaam_web_site = InlineQueryResultArticle(
            id="1",
            thumbnail_url="https://i.postimg.cc/bJshP6p2/INAAM-WEB-SITE.png",
            title="Сайт 🌐",
            input_message_content=InputTextMessageContent(message_text="<a href='https://inaam.ru'><b>Сайт INAAM 🌐</b></a>", parse_mode=ParseMode.HTML)
        )

        inaam_admin_phone = InlineQueryResultArticle(
            id="2",
            thumbnail_url="https://i.postimg.cc/5yBkWvY3/INAAM-PHONE.png",
            title="Телефон 📞",
            input_message_content=InputTextMessageContent(message_text=f"📞 <b>Телефон INAAM</b>\n\n〰️ <code>{os.getenv('PHONE_NUMBER')}</code> 〰️", parse_mode=ParseMode.HTML),
            parse_mode=ParseMode.HTML
        )

        inaam_admin_email = InlineQueryResultArticle(
            id="3",
            thumbnail_url="https://i.postimg.cc/RFnDG2vP/INAAM-EMAIL.png",
            title="Почта 📨",
            input_message_content=InputTextMessageContent(message_text=f"📨 <b>Почта INAAM</b>\n\n〰️ <code>{os.getenv('EMAIL')}</code> 〰️", parse_mode=ParseMode.HTML)
        )

        await inline_query.answer(results=[inaam_web_site, inaam_admin_phone, inaam_admin_email], cache_time=1)
        logger.info("Вызван inline мод")