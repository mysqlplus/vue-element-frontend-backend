# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  导入导出

import logging
from django.contrib.auth import get_user_model
from utils.base_resource import BaseResource
from import_export import fields, widgets
from .models import *
User = get_user_model()

logger = logging.getLogger('views')

class UserResource(BaseResource):

    class Meta:
        model = User
        skip_unchanged = True
        #exclude = ('password','last_login_ip','birthday')
        fields = ('id', 'username', 'cname', 'email', 'phone')
        export_order = ('id',)