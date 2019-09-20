#coding:utf-8
# -*- coding: utf-8 -*-
#author:laoseng,feilong
#create:2018-09
#  init

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Url, Role

User = get_user_model()

init_data = [
    {
        'role':{'name':'super_admin','cname':'超级管理员', 'description':'超级管理员'},
        'urls':[{'user_type': 'customuser', 'url':'^/', 'method':'ALL'}]
    },
    {
        'role': {'name': 'user_admin', 'cname': '用户管理员', 'description': '用户管理员'},
        'urls': [{'user_type': 'customuser', 'url': '^/api/v\d/users/', 'method': 'ALL'}]
    },
    {
        'role': {'name': 'role_admin', 'cname': '角色权限管理员', 'description': '角色权限管理员'},
        'urls': [{'user_type': 'customuser', 'url': '^/api/v\d/users/roles/', 'method': 'ALL'},{'user_type': 'customuser', 'url': '/users/urls/', 'method': 'ALL'}]
    },
]

init_white_url_data = [
    {'user_type': 'anonymous', 'url':'^/xadmin/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/media/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/docs/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/static/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/swagger-docs/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/api-auth/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/social/', 'method': 'ALL'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/send_sms_code/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/email_reset_password/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/reset_password/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/login/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/phone_login/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/ssologin/$', 'method': 'GET'},
    {'user_type': 'anonymous', 'url':'^/api/v\d/users/user/$', 'method': 'POST'},
    {'user_type': 'anonymous', 'url':'^/$', 'method': 'GET'},
    #{'user_type': 'anonymous', 'url':'^/api/v\d/users/user/info/$', 'method': 'GET'},
    {'user_type': 'authenticated', 'url':'^/api/v\d/users/user/', 'method': 'ALL'},
    {'user_type': 'authenticated', 'url':'^/api/v\d/users/users/get_users/', 'method': 'GET'},
]

class Command(BaseCommand):

    def handle(self, *args, **options):

        #角色权限
        for d in init_data:
            role,created = Role.objects.get_or_create(**d['role'])
            for row in d['urls']:
                url,created  = Url.objects.get_or_create(**row)
                role.urls.add(url)
            role.save()

        #URL权限白名单
        for d in init_white_url_data:
            Url.objects.get_or_create(**d)

        #管理员用户
        username = settings.INIT_ADMIN_USERNAME
        password = settings.INIT_ADMIN_PASSWORD
        if User.objects.count() == 0:
            d = {'username':username,'email':'{}@example.com'.format(username),'password':password}
            admin_user = User.objects.create_superuser(**d)
            admin_user.roles.add(Role.objects.get(name='super_admin'))
            # 重新设置密码，解决create_superuser中设置的密码不生效
            admin_user.set_password(password)
            admin_user.save()

        print('init users done')