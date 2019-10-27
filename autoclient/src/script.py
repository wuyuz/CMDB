from libs.conf import settings
#  懒加载settings，将触发所有的配置，并加载给settings
from libs.utils.import_str import get_class


def run():
    """
    程序的入口
    :return:
    """
    # 获得对应的采集的类路径
    class_path = settings.ENGINES_DICT.get(settings.ENGINE)
    cls = get_class(class_path)
    obj = cls()
    obj.handler()

