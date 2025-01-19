import logging
import colorlog

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = colorlog.StreamHandler()

formatter = colorlog.ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    log_colors={
        'DEBUG': 'green',
        'INFO': 'light_blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
