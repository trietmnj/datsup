import logging


class LogManager:
    """Cookie cutter logging manager - writes to console and file"""
    logger = logging.getLogger(__name__)

    def __init__(self, filePath):
        self.setupLogger(filePath)

    def setupLogger(self, filePath):
        """Set up console and file handlers"""
        # console handler
        cHandler = logging.StreamHandler()
        cHandler.setLevel(logging.WARNING)
        cFormatting = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        cHandler.setFormatter(cFormatting)

        # file handler
        fHandler = logging.FileHandler(filePath, mode='a') 
        fHandler.setLevel(logging.ERROR)
        fFormatting = logging.Formatter(
            '%(asctime)s - %(name)s - %(message)s', '%d/%m/%Y %H:%M:%S')
        fHandler.setFormatter(fFormatting)

        self.logger.addHandler(cHandler)
        self.logger.addHandler(fHandler)

    def logError(self, exception):
        self.logger.error(exception)

    def logWarning(self, msg):
        self.logger.warning(msg)


def appendLinetoFile(filePath: str, string: str):
    with open(filePath, 'a') as f:
        f.write(f'{string}\n')
