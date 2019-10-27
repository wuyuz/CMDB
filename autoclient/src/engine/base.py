from libs.conf import settings
import requests,json
from ..plugins import get_sever_info
from concurrent.futures import ThreadPoolExecutor

class BaseHandler:
    def __init__(self):
        self.asset_url = settings.POST_ASSET_URL

    def handler(self):
        """
        收集硬件信息 汇报给API
        :return:
        """
        raise NotImplementedError('handler 函数必须显示实现')


class SshAndSaltHandler(BaseHandler):

    def handler(self):
        # 获取要采集信息的主机
        ret = requests.get(
            url=self.asset_url
        )
        # 反序列化
        host_list = ret.json()
        pool = ThreadPoolExecutor(20)

        for host_name in host_list:
            pool.submit(self.task,host_name)

    def task(self,host_name):
        info = get_sever_info(self, host_name)
        ret = requests.post(
            url=self.asset_url,
            data=json.dumps(info).encode('utf-8'),  # 需要编码，否则过去解码不行
            headers={'content-type': 'application/json'}  # 没有会抛415
        )

        print(ret.text)