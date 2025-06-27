from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

try:
    a = 1/0
except Exception as e:
    logging.info("Exception occured")
    raise NetworkSecurityException(e)
    