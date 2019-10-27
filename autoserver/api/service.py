from repository import models


def process_basic(info):
    server_info = {}

    basic = info['basic']['data']
    main_board = info['main_board']['data']
    cpu = info['cpu']['data']
    server_info.update(basic)
    server_info.update(main_board)
    server_info.update(cpu)

    hostname = info['basic']['data']['hostname']  # 新的hostname
    old_hostname = info.get('old_hostname')  # 老的hostname

    server_list = models.Server.objects.filter(hostname=old_hostname if old_hostname else hostname)
    server_list.update(**server_info)
    server = models.Server.objects.filter(hostname=hostname).first()
    return server


def process_disk(info, server):
    disk_info = info['disk']['data']  # 新提交的数据

    disk_slot_set = set(disk_info)
    disk_slot__db_set = {i.slot for i in models.Disk.objects.filter(server=server)}

    # 新增  删除  更新
    add_slot_set = disk_slot_set - disk_slot__db_set  # 新增的槽位
    del_slot_set = disk_slot__db_set - disk_slot_set  # 删除的槽位
    update_slot_set = disk_slot__db_set & disk_slot_set  # 更新的槽位

    # 新增硬盘
    add_disk_lit = []
    add_record_lit = []
    for slot in add_slot_set:
        disk = disk_info.get(slot)

        """
        disk =  {
            'slot': '0',
            'pd_type': 'SAS',
            'capacity': '279.396',
            'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'
        }
                
        """
        "插槽位：0；类型：SAS "
        tpl_list = []  # ['插槽位 : 0', '磁盘类型 : SAS', '磁盘容量GB : 279.396', '磁盘型号 : SEAGATE ST300MM0006     LS08S0K2B5NV']
        for name, value in disk.items():
            verbose_name = models.Disk._meta.get_field(name).verbose_name
            tpl_list.append("{}:{}".format(verbose_name, value))  # 插槽位 : 0    磁盘型号: SAS
        add_record_lit.append(models.AssetRecord(server=server,content="新增一块硬盘，硬盘详细信息如下：{}".format('; '.join(tpl_list))))
        add_disk_lit.append(models.Disk(**disk, server=server))

    if add_disk_lit:
        models.Disk.objects.bulk_create(add_disk_lit)
        models.AssetRecord.objects.bulk_create(add_record_lit)

    # 删除硬盘
    if del_slot_set:
        models.Disk.objects.filter(server=server, slot__in=del_slot_set).delete()
        models.AssetRecord.objects.create(server=server,content='槽位{}的硬盘被移除了。'.format(','.join(del_slot_set)))


    # 更新硬盘
    update_record_list = []    # 变更记录对象的列表
    for slot in update_slot_set:
        disk = disk_info.get(slot)  # 新提交的数据
        disk_obj = models.Disk.objects.filter(server=server, slot=slot).first() # 老硬盘的对象

        tpl_list = [] # 临时存放  ’{}由{}变更为{}‘

        update_dict = {}  # 更新字段的值
        for name,value in disk.items():
            old_value = getattr(disk_obj,name)  # 通过反射获取老的值
            if value != str(old_value):
                update_dict[name] = value
                verbose_name = models.Disk._meta.get_field(name).verbose_name
                tpl_list.append("{}由{}变更为{}".format(verbose_name,old_value,value))

        if tpl_list:
            update_record_list.append(models.AssetRecord(server=server,content='槽位{}上的硬盘发生变更，变更信息如下：{}'.format(slot,'; '.join(tpl_list))))
            models.Disk.objects.filter(server=server, slot=slot).update(**update_dict)

    if update_record_list:
        models.AssetRecord.objects.bulk_create(update_record_list)


def process_memory(info, server):
    # 更新内存
    memory_info = info['memory']['data']  # 新提交的数据

    memory_slot_set = set(memory_info)
    memory_slot__db_set = {i.slot for i in models.Memory.objects.filter(server=server)}

    # 新增  删除  更新
    add_slot_set = memory_slot_set - memory_slot__db_set  # 新增的槽位
    del_slot_set = memory_slot__db_set - memory_slot_set  # 删除的槽位
    update_slot_set = memory_slot__db_set & memory_slot_set  # 更新的槽位

    # 新增内存

    add_memory_lit = []
    for slot in add_slot_set:
        memory = memory_info.get(slot)
        add_memory_lit.append(models.Memory(**memory, server=server))

    if add_memory_lit:
        models.Memory.objects.bulk_create(add_memory_lit)

    # 删除内存
    if del_slot_set:
        models.Memory.objects.filter(server=server, slot__in=del_slot_set).delete()

    # 更新内存
    for slot in update_slot_set:
        memory = memory_info.get(slot)
        models.Memory.objects.filter(server=server, slot=slot).update(**memory)


def process_nic(info, server):
    nic_info = info['nic']['data']  # 新提交的数据

    nic_name_set = set(nic_info)
    nic_name__db_set = {i.name for i in models.NIC.objects.filter(server=server)}

    # 新增  删除  更新
    add_name_set = nic_name_set - nic_name__db_set  # 新增的槽位
    del_name_set = nic_name__db_set - nic_name_set  # 删除的槽位
    update_name_set = nic_name__db_set & nic_name_set  # 更新的槽位

    # 新增网卡

    add_nic_lit = []
    for name in add_name_set:
        nic = nic_info.get(name)
        nic['name'] = name
        add_nic_lit.append(models.NIC(**nic, server=server))

    if add_nic_lit:
        models.NIC.objects.bulk_create(add_nic_lit)

    # 删除网卡
    if del_name_set:
        models.NIC.objects.filter(server=server, name__in=del_name_set).delete()

    # 更新网卡
    for name in update_name_set:
        nic = nic_info.get(name)
        nic['name'] = name
        models.NIC.objects.filter(server=server, name=name).update(**nic)
