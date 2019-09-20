# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 过滤 control

from django_filters import rest_framework as filters
from .models import LogsEntry


class LogsEntryFilter(filters.FilterSet):
    date_range = filters.DateRangeFilter(field_name='time_added', help_text='时间范围')

    class Meta:
        model = LogsEntry
        fields = ('user', 'content_type','action_flag', 'date_range')