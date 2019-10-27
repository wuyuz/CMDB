from libs.conf import settings

class BasePlugin:
    def __init__(self):
        self.debug = settings.DEBUG
        self.base_dir = settings.BASE_DIR

    def get_os(self,handler,hostname=None):
        # linux 会返回Linux,这里先注释

        # ret = handler.cmd('uname',hostname)
        return 'Linux'

    # 会自动触发父级的process方法，在此判断操作系统，并调用self的linux，但必须自己有
    def process(self,handler,hostname=None):
        os = self.get_os(handler,hostname)
        if os == 'Linux':
            return self.linux(handler,hostname)
        else:

            return self.win(handler,hostname)


    def linux(self,handler,hostname=None):
        raise NotImplementedError('linux() must be Implement')

    def win(self,handler,hostname=None):
        raise NotImplementedError('win() must be Implement')