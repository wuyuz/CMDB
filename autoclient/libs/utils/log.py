import logging
from libs.conf import settings

class Logger:
    # 最好单例
    def __init__(self,name,log_file,level=logging.DEBUG):
        file_handler = logging.FileHandler(log_file, 'a', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
        file_handler.setFormatter(fmt)

        self.logger = logging.Logger(name, level=level)
        self.logger.addHandler(file_handler)

    def info(self,msg):
        self.logger.info(msg)

    def debug(self,msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

logger = Logger(settings.LOG_NAME,settings.LOG_FILE_PATH)