import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("wedding_invites_logger")
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

handler.stream.reconfigure(encoding="utf-8")
logger.addHandler(handler)

file_handler = RotatingFileHandler(
    "logs/wedding_invites.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
