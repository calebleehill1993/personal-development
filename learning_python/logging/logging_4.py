import logging

# Changing the formatting
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')

# Here are all the log record attributes
# https://docs.python.org/3/library/logging.html#logrecord-attributes

# logging.basicConfig(format='%(levelname)s: %(asctime)s, %(created)f: %(message)s', level=logging.DEBUG)
# logging.debug('This message should appear on the console')
# logging.info('So should this')
# logging.warning('And this, too')