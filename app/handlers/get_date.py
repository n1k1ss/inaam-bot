from datetime import datetime
import zoneinfo

from handlers.get_current_region import get_current_region
from inaam_bot_logger import logger
from handlers.db import db

async def get_datetime(part: str) -> int:
    current_region = await get_current_region()
    tz = zoneinfo.ZoneInfo(current_region)

    now = datetime.now(tz)
    return getattr(now, part)