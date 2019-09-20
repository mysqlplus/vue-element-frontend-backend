# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 业务control 基础类

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from modellog.mixins import LoggingViewSetMixin
from rest_framework.response import Response
from rest_framework.decorators import action

class DefaultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000

class BaseModelViewSet(LoggingViewSetMixin, viewsets.ModelViewSet):
    pagination_class = DefaultPagination

    @action(methods=['get'], detail=False)
    def get_table_info(self, request):
        '''
        获取表字段名和过滤选项
        '''
        data = {}
        if hasattr(self.queryset.model(), 'get_table_info'):
            data = self.queryset.model().get_table_info()

        return Response(data)

class BaseGenericViewSet(LoggingViewSetMixin, viewsets.GenericViewSet):
    pagination_class = DefaultPagination