from colorlog import ColoredFormatter
import logging

LOG_LEVEL = logging.INFO

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s:%(reset)s     %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "white",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("ait_logger")
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
logger.propagate = False
