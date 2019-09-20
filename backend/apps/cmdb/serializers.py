# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  序列化类
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class IdcSerializer(serializers.ModelSerializer):
    idc_name = serializers.CharField(source='idc.name', read_only=True)

    class Meta:
        model = Idc
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['idc_detail'] = None
        if instance.idc: ret['idc_detail'] = {'name': instance.idc.name, 'cname': instance.idc.cname, 'id':instance.idc.id}
        return ret