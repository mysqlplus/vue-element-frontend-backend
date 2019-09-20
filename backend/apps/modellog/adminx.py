# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 后台 control

import xadmin
from .models import LogsEntry

class LogsEntryAdmin(object):
    list_display = ["time_added", "user", "object_repr", "action_flag", "message"]

xadmin.site.register(LogsEntry, LogsEntryAdmin)