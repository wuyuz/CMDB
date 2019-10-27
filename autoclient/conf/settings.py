import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 用户配置settings
USER = 'root'
PWD='root1234'

SSH_USER='root'
SSH_PWD='root1234'


# 设置采集模式
ENGINE = 'agent'

# 采集模式，采用字典可以支持反射
ENGINES_DICT = {
    'agent':'src.engine.agent.AgentHandler',
    'ssh':'src.engine.ssh.SshHandler',
    'salt':'src.engine.salt.SaltHandler',
}

# 采集数据类型
PLUGINS_DICT = {
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.NIC',
    'basic':'src.plugins.basic.Basic',
    'cpu':'src.plugins.cpu.Cpu',
    'main_board':'src.plugins.main_board.MainBoard',
}

#开发者模式
DEBUG=True

# API后端
POST_ASSET_URL = 'http://127.0.0.1:8000/api/asset/'

# 日志文件位置
LOG_NAME = 'logfile'
LOG_FILE_PATH = os.path.join(BASE_DIR,'log','log.log')

# 认证证书文件
CERT_PATH = os.path.join(BASE_DIR,'conf','cert')

# API验证KEY
KEY= 'dadfafadfadfadf23415@#$#$@'