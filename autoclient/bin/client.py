import os
import sys
ret = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ret)  #手动添加环境路径，Pycharm默认添加


if __name__ == '__main__':
    # os.environ是系统的环境变量,借鉴于django的manager.py,也就是相当于字典，可以设置键值，后面后可以找到该键值
    os.environ.setdefault('USER_SETTINGS','conf.settings')
    from src.script import run
    run()