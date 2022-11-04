__author__ = 'chill'

import logging

# Writing to a file

# Setting for logging (basicConfig can only be run once).
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# If we want to write over the saved log file
# logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')



