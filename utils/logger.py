from loguru import logger
from datetime import datetime
from pathlib import Path
import logging
import json
import sys

from config import LOG_LEVEL  # Should be 'DEBUG', 'INFO', etc.

# Custom handler for the discord.py logger
class DiscordHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.log(record.levelno, log_entry)

def setup_logging():
    logs_path = Path("logs")
    logs_path.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_path / f"{today}-skywalker.log"

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | <cyan>{file}</cyan>:<yellow>{function}</yellow> | "
        "<level>{message}</level>"
    )

    # Remove any default handlers and set up our own
    logger.remove()

    logger.add(sys.stdout, level=LOG_LEVEL, format=log_format, colorize=True)
    logger.add(log_file, level=LOG_LEVEL, format=log_format)

    # Setup discord.py logging
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_handler = DiscordHandler()
    discord_logger.handlers = [discord_handler]
    discord_logger.propagate = False

def log_json(json_obj, level="DEBUG"):
    """Pretty-print JSON into the logs."""
    logger.log(level, json.dumps(json_obj, indent=4))

# Initialize logger at import
setup_logging()
