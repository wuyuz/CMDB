# 系统settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER = 'root'
PWD='root1234'

SSH_PORT=22


LOG_NAME = 'logfile'
LOG_FILE_PATH = os.path.join(BASE_DIR,'log','log.log')