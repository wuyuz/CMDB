import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoserver.settings")

import django

django.setup()

from repository import models
#
# for field in models.Disk._meta.fields:
#     print(field.name, field.verbose_name)

data = {
    'slot': '0',
    'pd_type': 'SAS',
    'capacity': '279.396',
    'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'
}
# field = models.Disk._meta.get_field('pd_type')
# print(field.verbose_name)


tpl_list = []
for name,value in data.items():
    verbose_name = models.Disk._meta.get_field(name).verbose_name
    tpl_list.append("{} : {}".format(verbose_name,value))  # 插槽位 : 0    磁盘型号: SAS


print(tpl_list)



