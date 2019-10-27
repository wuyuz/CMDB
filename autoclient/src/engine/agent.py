import requests,json,os,time
from .base import BaseHandler
from ..plugins import get_sever_info
from libs.conf import settings
from libs.utils.auth import gen_key

class AgentHandler(BaseHandler):

    def cmd(self,command,hostname=None):
        import subprocess
        ret = subprocess.getoutput(command)
        return ret

    def handler(self):
        """
        收集硬件信息 汇报给API
        :return:
        """
        info = get_sever_info(self)

        # 客户端没有认证文件，表示新的主机
        if not os.path.exists(settings.CERT_PATH):
            info['action'] = 'create'  # 携带action
        else:
            # 老的主机名，认证文件已经存在
            with open(settings.CERT_PATH,'r',encoding='utf-8') as f:
                old_hostname = f.read()
            hostname = info['basic']['data']['hostname']
            if hostname == old_hostname:
                # 相当于主机名没有更改，告诉API只更新资产信息
                info['action'] = 'update'
            else:
                # 修改主机名，告知API更新资产信息 + 主机名
                info['action'] = 'update_host'
                info['old_hostname'] = old_hostname

        #发送数据给API, 但是这是同步的，显得特别慢，因为有多个主机

        # ctime = time.time()

        ret = requests.post(
            url=self.asset_url,
            # params={'key':gen_key(ctime),'ctime':ctime},
            data=json.dumps(info).encode('utf-8'), # 需要编码，否则过去解码不行
            headers = {'content-type': 'application/json'}  # 没有会抛415
        )
        res = ret.json()

        if res.get('status'):
            with open(settings.CERT_PATH,'w',encoding='utf-8') as f:
                f.write(res['hostname'])

