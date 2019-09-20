# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  后台
import xadmin
from .models import *
from .resources import *

class IdcAdmin(object):
    list_display = ['name', 'cname', 'phone', 'create_time']
    list_filter = ['name', 'cname', 'phone']
    search_fields = ['name', ]

class HostAdmin(object):
    import_export_args = {'import_resource_class': HostResource, 'export_resource_class': HostResource}
    list_display = ['hostname', 'ip', 'host_type', 'sn', 'create_time']
    list_filter = ['hostname', 'ip', 'host_type']
    search_fields = ['hostname', 'ip']
    resource_class = HostResource

xadmin.site.register(Idc, IdcAdmin)
xadmin.site.register(Host, HostAdmin)