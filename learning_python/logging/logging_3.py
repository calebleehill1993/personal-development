__author__ = 'chill'

import logging

# Formatting
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
logging.info('This is one way of adding variables: %s, %s, %d', 'var1', 'var2', 3)
logging.info('Here is another way: {var1}, {var2}, {var3}'.format(var1='var1', var2='var2', var3=3))
