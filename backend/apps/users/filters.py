# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  查询过滤条件

from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from .models import Url

User = get_user_model()


class UrlFilter(filters.FilterSet):
    class Meta:
        model = Url
        fields = {'user_type': ['exact', 'in'], 'method': ['exact', 'in']}


class UsersFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ('is_active', 'is_superuser', 'is_staff')
