# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  业务过滤条件
import datetime
from django_filters import rest_framework as filters
from .models import *

class HostFilter(filters.FilterSet):
    is_expired = filters.BooleanFilter(field_name='expired_time', label='是否过保', help_text='是否过保', method='filter_is_expired')

    def filter_is_expired(self, queryset, name, value):
        today = datetime.datetime.today()
        if value:
            return queryset.filter(expired_time__lt=today)
        else:
            return queryset.filter(expired_time__gte=today)

    class Meta:
        model = Host
        fields = {'use_status': ['exact','in'], 'host_type':['exact','in'],'run_status':['exact','in'],'os':['exact','in'], 'idc':['exact','in']}