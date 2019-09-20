# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  导入到处类
import logging
from collections import OrderedDict
from utils.base_resource import BaseResource
from import_export import fields, widgets
from .models import *
logger = logging.getLogger('views')

class IdcResource(BaseResource):

    class Meta:
        model = Idc
        skip_unchanged = True
        exclude = ('create_time', 'update_time')
        export_order = ('id', 'name',)

class HostResource(BaseResource):

    idc = fields.Field(column_name='idc', attribute='idc', widget=widgets.ForeignKeyWidget(Idc, 'name'))

    def dehydrate_host_type(self, obj):
        return self.get_choices_value(obj.host_type, Host.HOST_TYPE)

    def dehydrate_use_status(self, obj):
        return self.get_choices_value(obj.use_status, Host.USE_STATUS)

    def dehydrate_run_status(self, obj):
        return self.get_choices_value(obj.run_status, Host.RUN_STATUS)

    def dehydrate_salt_status(self, obj):
        return self.get_choices_value(obj.salt_status, Host.SALT_STATUS)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        data = []
        for row in dataset.dict:
            tmp = OrderedDict()
            for item in row:
                if item == self.vname_dict['host_type']:
                    tmp[item] = self.get_choices_key(row[item], Host.HOST_TYPE)
                elif item == self.vname_dict['use_status']:
                    tmp[item] = self.get_choices_key(row[item], Host.USE_STATUS)
                elif item == self.vname_dict['run_status']:
                    tmp[item] = self.get_choices_key(row[item], Host.RUN_STATUS)
                elif item == self.vname_dict['salt_status']:
                    tmp[item] = self.get_choices_key(row[item], Host.SALT_STATUS)
                else:
                    tmp[item] = row[item]
            data.append(tmp)
        dataset.dict = data

    class Meta:
        model = Host
        skip_unchanged = True
        exclude = ('create_time', 'update_time')
        export_order = ('id', 'hostname', 'ip', 'host_type', 'idc')