import importlib

def get_class(path_str):

    module_str,cls_str = path_str.rsplit('.',maxsplit=1)
    # 通过importlib模块来动态路径获取 模块对象，并反射取类
    module = importlib.import_module(module_str)
    cls = getattr(module,cls_str)
    return cls