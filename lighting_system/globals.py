import logging
COMMENT_DELIMITER = "#"
LOGGER_FILENAME = ".log"
logging.basicConfig(filename=LOGGER_FILENAME,
                    format='[%(asctime)s][%(levelname)s]   %(message)s',
                    level=logging.DEBUG)
logging.info("Logger started.")