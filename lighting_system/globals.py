import logging
from logging import handlers
import sys

COMMENT_DELIMITER = "#"
LOGGER_FILENAME = ".log"
LOG_FORMAT_STRING = '[%(processName)s:%(funcName)s][%(asctime)s][%(levelname)s]%(message)s'
LOG_FORMAT = logging.Formatter(LOG_FORMAT_STRING)

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(LOG_FORMAT)
logger.addHandler(ch)

fh = logging.handlers.RotatingFileHandler(LOGGER_FILENAME, maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(LOG_FORMAT)
logger.addHandler(fh)

# Todo: Read form configuration file
HABITAT_LIGHTING_SYSTEM_PORT = 9000
HABITAT_ADDRESS = "localhost"
COMMANDER_ADDRESS = "localhost"
# Todo: Read from configuration file
LIGHT_PERIOD_CONTROL_CYCLE = 0.050