import os
import importlib
from . import global_settings

class Settings:
    def __init__(self):
        #系统settings
        for i in dir(global_settings): # 加载系统 设置，系统应该放最前面，会进行覆盖
            if i.isupper():  # 全局设置必须大写
                v = getattr(global_settings, i)  # 使用反射获取属性/方法
                self.__setattr__(i, v)  # 也可以使用setattr(self,i,v)

        # 用户settings
        path = os.environ.get('USER_SETTINGS')
        # 通过path路径拿到模块对象 module,导入用户的settings，在项目启动时加载到了环境变量中
        module = importlib.import_module(path)
        # 但是不不知道用户settings中 保证他会写这些属性，可以通过dir看module属性
        for i in dir(module):
            if i.isupper():  # 全局设置必须大写
                v = getattr(module,i)  # 使用反射获取属性/方法
                self.__setattr__(i,v)  # 也可以使用setattr(self,i,v)

    # def __setattr__(self, key, value):
    #     # 通过__setattr__可以做二次开发
    #     if key == 'USER':
    #         key = 'OK'
    #     super().__setattr__(key,value)


# 借鉴于django的懒加载setting+global_settings, 全部的setting配置都给了settings
settings = Settings()
# 下次在其他模块中通过import 导入settings默认是单例