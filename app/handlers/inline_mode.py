from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from aiogram.enums import ParseMode

def register_inline_mode_handler(dp):
    @dp.inline_query()
    async def inline_echo(inline_query: InlineQuery):
        web_site = InlineQueryResultArticle(
            id="1",
            title="Сайт",
            input_message_content=InputTextMessageContent(message_text=f"<a href='https://inaam.ru'><b>Сайт INAAM</b></a>", parse_mode=ParseMode.HTML)
        )
        await inline_query.answer(results=[web_site], cache_time=1)