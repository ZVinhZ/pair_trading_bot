# this file is for general-purpose functions apart from trading logic

# logging package to track everything the bot is doing
import logging
from pathlib import Path
from .config import BASE_DIRECTORY

LOG_DIRECTORY = BASE_DIRECTORY / "logs"
LOG_DIRECTORY.mkdir(exist_ok = True)

# level = INFO so the logger can only message that are INFO level are above (WARNING, ERROR, CRITICAL)
# Hide DEBUG which is only for developer
def setup_logger(name: str = "pair trading", level = logging.INFO):
    logger = logging.getLogger(name)



