from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json


# Create your views here.
def asset(request):
    # ret = json.loads(request.body.decode('utf-8'))
    # print(ret,type(ret))
    print(request.body)
    print(request.POST)
    return JsonResponse({'code': 200, 'msg': '保存成功'})


from rest_framework.views import APIView
from rest_framework.response import Response

from repository import models
from .service import process_basic, process_disk, process_memory, process_nic

def gen_key(ctime):
    key = "{}|{}".format(KEY, ctime)

    md5 = hashlib.md5()
    md5.update(key.encode('utf-8'))

    return md5.hexdigest()


key_record = {}

class AuthView(APIView):

    def dispatch(self, request, *args, **kwargs):

        if request.method != 'POST':
            return super().dispatch(request, *args, **kwargs)

        ret = {'stauts': True, 'msg': 'ok'}

        client_key = request.GET.get('key')
        now = time.time()

        ctime = request.GET.get('ctime',now)

        server_key = gen_key(ctime,)


        if now - float(ctime) > 2:
            # 时间超时
            ret['stauts'] = False
            ret['msg'] = '来的有点晚了'
            return JsonResponse(ret)

        if client_key in key_record:
            # 已经使用过验证
            ret['stauts'] = False
            ret['msg'] = '可以已经被使用了'
            return JsonResponse(ret)


        if client_key != server_key:
            ret['stauts'] = False
            ret['msg'] = '验证不通过'
            return JsonResponse(ret)

        else:
            key_record[client_key] = ctime
            return super().dispatch(request, *args, **kwargs)



class Asset(AuthView):
    def get(self, request):
        host_list = ['c1.com', 'c2.com'] * 100
        return Response(host_list)

    def post(self, request):
        info = request.data
        action = info.get('action')

        hostname = info['basic']['data']['hostname']

        result = {
            'status': True,
            'hostname': hostname
        }
        # print(info)

        if action == 'create':
            # 新增资产信息
            # 新增server
            server_info = {}

            basic = info['basic']['data']
            main_board = info['main_board']['data']
            cpu = info['cpu']['data']
            server_info.update(basic)
            server_info.update(main_board)
            server_info.update(cpu)

            server = models.Server.objects.create(**server_info)
            # 新增disk
            disk_info = info['disk']['data']
            disk_obj_list = []
            for disk in disk_info.values():
                disk_obj_list.append(models.Disk(**disk, server=server))
            if disk_obj_list:
                models.Disk.objects.bulk_create(disk_obj_list)

            # 新增memory

            memory_info = info['memory']['data']
            memory_obj_list = []
            for memory in memory_info.values():
                memory_obj_list.append(models.Memory(**memory, server=server))
            if memory_obj_list:
                models.Memory.objects.bulk_create(memory_obj_list)

            # 新增nic
            nic_info = info['nic']['data']
            nic_obj_list = []
            for name, nic in nic_info.items():
                nic_obj_list.append(models.NIC(**nic, name=name, server=server))
            if nic_obj_list:
                models.NIC.objects.bulk_create(nic_obj_list)

        elif action == 'update' or action == 'update_host':
            # 只更新资产信息
            # 更新主机表
            server = process_basic(info)
            process_disk(info, server)
            process_memory(info, server)
            process_nic(info, server)

        return Response(result)


KEY = 'alkdjwqm,ensklhjkrhwfeqnsdah'
import hashlib
import time



class Test(APIView):

    def post(self, request):
        ret = {'stauts': True, 'msg': 'ok'}

        client_key = request.GET.get('key')
        ctime = request.GET.get('ctime')
        server_key = gen_key(ctime)

        now =time.time()

        if now - float(ctime) > 2:
            # 时间超时
            ret['stauts'] = False
            ret['msg'] = '来的有点晚了'


        if client_key in key_record:
            # 已经使用过验证
            ret['stauts'] = False
            ret['msg'] = '可以已经被使用了'

        if client_key != server_key:
            ret['stauts'] = False
            ret['msg'] = '验证不通过'

        key_record[client_key] = ctime

        return Response(ret)
