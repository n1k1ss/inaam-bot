import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

class Formatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        return f"{msg}\n##############################"

logger = logging.getLogger("inaam-bot")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "logs/inaam-bot.log",
    maxBytes=5_000_000,
    backupCount=5,
    encoding="utf-8"
)

formatter = Formatter (
    fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)