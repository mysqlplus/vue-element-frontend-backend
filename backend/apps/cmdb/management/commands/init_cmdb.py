# coding:utf-8
#author:laoseng,feilong
#create:2018-09
#  初始化
from django.core.management.base import BaseCommand
from djcelery.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from users.models import Url, Role

init_data = [
    {
        'role': {'name': 'cmdb_admin', 'cname': 'CMDB管理员', 'description': 'CMDB管理员'},
        'urls': [{'user_type': 'customuser', 'url': '^/api/v\d/cmdb/', 'method': 'ALL'}]
    },
    {
        'role': {'name': 'op', 'cname': '运维人员', 'description': '运维人员'},
        'urls': [{'user_type': 'customuser', 'url': '^/api/v\d/cmdb/', 'method': 'ALL'}]
    },
]

init_white_url_data = [
    {'user_type': 'anonymous', 'url': '^/api/v1/cmdb/hosts/get_host/$', 'method': 'GET'},
]


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 角色权限
        for d in init_data:
            role, created = Role.objects.get_or_create(**d['role'])
            for row in d['urls']:
                url, created = Url.objects.get_or_create(**row)
                role.urls.add(url)
            role.save()

        # URL权限白名单
        for d in init_white_url_data:
            Url.objects.get_or_create(**d)
