from handlers.db import db
from inaam_bot_logger import logger

async def get_current_balance():
    row = await db.fetchrow('SELECT amount FROM balance')
    return row["amount"]