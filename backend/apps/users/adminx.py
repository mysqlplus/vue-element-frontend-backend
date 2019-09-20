# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  后台

import xadmin
from .models import *

class RoleAdmin(object):
    list_display = ["name", "cname","create_time"]

class UrlAdmin(object):
    list_display = ["user_type", "url", "method"]

class DepartmentAdmin(object):
    list_display = ["name", "parent", "create_time"]
    search_fields = ['name', ]

class OtpAdmin(object):
    list_display = ["secret", "issuer_name", "is_active", "create_time"]

class OtpRecoveryCodeAdmin(object):
    list_display = ["code", "is_active", "create_time"]

xadmin.site.register(Role, RoleAdmin)
xadmin.site.register(Url, UrlAdmin)
xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(Otp, OtpAdmin)
xadmin.site.register(OtpRecoveryCode, OtpRecoveryCodeAdmin)