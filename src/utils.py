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
    
    # check whether the logger already has any handlers attached
    # avoid duplicate logger
    if logger.handlers:
        return logger
    
    logger.setLevel = level

    format_logger = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    
    # console handler used for sending log message to the terminal
    # log appears live in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format_logger)

    logger.addHandler(console_handler)

    # file handler used for saving log into a file
    file_handler = logging.FileHandler(LOG_DIRECTORY / f"{name}.log")
    file_handler.setFormatter(format_logger)
    
    logger.addHandler(file_handler)

    return logger


