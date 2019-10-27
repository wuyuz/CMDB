from libs.conf import settings
from libs.utils.import_str import get_class

def get_sever_info(handler,hostname=None):
    """
    根据配置，采集对应的插件信息
    :return:
    """
    info = {}
    # 针对各个插件，触发他们的process --> linux/win
    for name,plugin in settings.PLUGINS_DICT.items():
        cls = get_class(plugin)
        obj = cls()
        ret = obj.process(handler,hostname)
        info[name] = ret

    return info