from .base import SshAndSaltHandler # 将公共的handler提取成一个类

class SaltHandler(SshAndSaltHandler):

    def cmd(self,command,hostname):
        import salt.client
        local = salt.client.LocalClient()
        result = local.cmd(hostname,'cmd.run',[command])
        return  result


