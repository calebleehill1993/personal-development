__author__ = 'chill'

import logging

class CustomFormatter():

    # The colors come from ANSI escape code found at: https://en.wikipedia.org/wiki/ANSI_escape_code
    # There are several options. There is another learning module that will cover ANSI text coloring and formatting.
    blue = "\x1b[38;2;0;200;255m"
    grey = "\x1b[39;20m"
    yellow = "\x1b[38;2;255;255;0m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[38;2;255;0;0;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    # The logging.Formatter has a format function that this is using to create the colors for each level of logging.
    # The record itself is coming from the logger ever time that the log is writen to.
    # All this Custom formatting class does is adds a middle step between the standard logging.Formatter and the record
    # so that the record can be dynamically formatted depending on the level.
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")