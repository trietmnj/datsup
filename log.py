import logging
import sys


class LogManager:
    """Cookie cutter logging manager - writes to console and file"""
    logger = logging.getLogger(__name__)

    def __init__(self, filePath):
        self.setupLogger(filePath)

    def setupLogger(self, filePath):
        """Set up console and file handlers"""
        # console handler
        cHandler = logging.StreamHandler(sys.stdout)
        cHandler.setLevel(logging.WARNING)
        # file handler
        fHandler = logging.FileHandler(filePath, mode='a') 
        fHandler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')
        cHandler.setFormatter(formatter)
        fHandler.setFormatter(formatter)
        self.logger.addHandler(cHandler)
        self.logger.addHandler(fHandler)

    def logError(self, exception):
        self.logger.error(exception)

    def logWarning(self, msg):
        self.logger.warning(msg)
