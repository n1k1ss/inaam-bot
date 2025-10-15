from handlers.db import db
from inaam_bot_logger import logger

async def get_current_region():
    row = await db.fetchrow('SELECT region FROM set_time')
    return row["region"]