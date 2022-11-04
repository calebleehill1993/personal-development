__author__ = 'chill'
import logging

# LEVELS
# By default the logger is set to the warning level so only warnings and higher will be written to the console.

logging.debug('Detailed information, typically of interest only when diagnosing problems.')
logging.info('Confirmation that things are working as expected.')
logging.warning('An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.')
logging.error('Due to a more serious problem, the software has not been able to perform some function.')
logging.critical('A serious error, indicating that the program itself may be unable to continue running.')