# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 日志记录 control

from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins
from rest_framework import viewsets
from utils.base_view import BaseModelViewSet, BaseGenericViewSet

from .models import LogsEntry
from .serializers import LogsEntrySerializer, ContentTypeSerializer
from .filters import LogsEntryFilter

class LogsEntryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, BaseGenericViewSet):
    queryset = LogsEntry.objects.order_by('-id')
    serializer_class = LogsEntrySerializer
    ordering_fields = ('id', 'user')
    search_fields = ('message','user__username')
    filterset_class = LogsEntryFilter

class ContentTypeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ContentType.objects.order_by('-id')
    serializer_class = ContentTypeSerializer