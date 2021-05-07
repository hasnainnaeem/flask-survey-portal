import logging
logging.basicConfig(filename = 'logs',
					format   = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s : %(message)s', 
					datefmt  = '%m/%d/%Y %H:%M:%S',
					level    = logging.INFO)
logger = logging.getLogger(__name__)