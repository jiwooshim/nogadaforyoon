import os
import sys
import logging
from datetime import datetime
from utils import module_path, starttime


today = datetime.today().date().strftime('%Y%m%d')

"""Set up logging"""
log_path = os.path.join(module_path, 'log', f'{today}.log')

logger = logging.getLogger('newton-log')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s - %(message)s', datefmt='%Y%m%d %H:%M:%S')

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
file_handler.set_name('my_file_handler')
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
console_handler.set_name('my_console_handler')
logger.addHandler(console_handler)

logger.info('=' * 65)
logger.info('Scraper started at {0}'.format(datetime.fromtimestamp(starttime).strftime('%Y%m%d %H:%M:%S')))
logger.info('Command line:\t{0}'.format(sys.argv[0]))
logger.info('Arguments:\t\t{0}'.format(' '.join(sys.argv[:])))
logger.info('=' * 65)
