# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 序列化 control
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import LogsEntry

class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'

class LogsEntrySerializer(serializers.ModelSerializer):
    """模块日志 序列化模型"""
    user = serializers.CharField(source='user.username', read_only=True)
    model = serializers.CharField(source='content_type.model', read_only=True)
    action = serializers.CharField(source='get_action_flag_display', read_only=True)
    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        return obj.get_message()

    class Meta:
        model = LogsEntry
        fields = ('id', 'user', 'model', 'action_flag', 'action', 'object_id', 'time_added', 'message')
