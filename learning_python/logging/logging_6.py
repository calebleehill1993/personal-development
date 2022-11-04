__author__ = 'chill'
import extra_logging_package
import logging

format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

logger = logging.Logger(__name__)
logger.setLevel(logging.DEBUG)
logger.info(__name__)

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create a file handler and set level to debug
fh = logging.FileHandler(filename='file_handler_test.log')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(format)

# add formatter to ch
ch.setFormatter(formatter)

# add formatter to fh
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# add fh to logger
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')