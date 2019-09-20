# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  ORM类
from django.db import models
from utils.base_model import BaseModel
from utils.util import deal_fields_Table


class Idc(BaseModel):
    ''' 机房 '''
    short_name = models.CharField(verbose_name='名称简写', max_length=32, unique=True)
    address = models.CharField(verbose_name='机房地址', help_text='机房地址', max_length=128, blank=True, null=True)
    contact = models.CharField(verbose_name='联系人', help_text='联系人', max_length=32, blank=True, null=True)
    phone = models.CharField(verbose_name='联系电话', help_text='联系电话', max_length=32, blank=True, null=True)
    cabinet = models.CharField(verbose_name='机柜信息', help_text='机柜信息', max_length=512, blank=True, null=True)
    bandwidth = models.CharField(verbose_name='机房带宽(M)', help_text='机房带宽(M)', max_length=32, blank=True, null=True)
    network = models.TextField(verbose_name='网段', help_text='网段', blank=True, null=True)
    operator = models.CharField(verbose_name='运营商', help_text='运营商', max_length=64, blank=True, null=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = "IDC机房"
        verbose_name_plural = verbose_name

    def get_table_info(self):
        """
        获取table表
        """
        data = deal_fields_Table(self._meta.fields, True, True, 2, None,None,None)
        return data


class Host(models.Model):
    ''' 主机 '''
    HOST_TYPE = (
        (1, '物理机'),
        (2, '虚拟机'),
        (3, 'Docker'),
    )
    USE_STATUS = (
        (0, '未使用'),
        (1, '已使用'),
        (2, '故障'),
        (3, '报废'),
    )
    RUN_STATUS = (
        (-1, '未知'),
        (0, '已关机'),
        (1, '运行中'),
        (2, '启动中'),
        (3, '停止中'),
    )
    SALT_STATUS = (
        (-1, '未知'),
        (0, 'DOWN'),
        (1, 'UP'),
    )

    hostname = models.CharField(verbose_name='主机名', help_text='主机名', max_length=128, unique=True)
    ip = models.GenericIPAddressField(verbose_name='主机IP', help_text='主机IP', unique=True)
    host_type = models.IntegerField(verbose_name='主机类型', help_text='主机类型', choices=HOST_TYPE, default=1)
    idc = models.ForeignKey(Idc, verbose_name='机房', help_text='机房', on_delete=models.SET_NULL, null=True)
    os = models.CharField(verbose_name='操作系统', help_text='操作系统', max_length=64, blank=True, null=True)
    cpu = models.CharField(verbose_name='CPU', help_text='CPU', max_length=64, blank=True, null=True)
    memory = models.CharField(verbose_name='内存', help_text='内存', max_length=64, blank=True, null=True)
    disk = models.CharField(verbose_name='硬盘', help_text='硬盘', max_length=128, blank=True, null=True)
    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', help_text='管理IP', blank=True, null=True)
    run_status = models.IntegerField(verbose_name='运行状态', help_text='运行状态', choices=RUN_STATUS, blank=True, default=-1)
    cabinet = models.CharField(verbose_name='机柜', help_text='机柜', max_length=64, blank=True, null=True)
    position = models.CharField(verbose_name='U位', help_text='U位', max_length=16, blank=True, null=True)
    up_time = models.DateField(verbose_name='上架时间', help_text='上架时间', blank=True, null=True)
    expired_time = models.DateField(verbose_name='过保时间', help_text='过保时间', blank=True, null=True)
    asset_no = models.CharField(verbose_name='资产编号', help_text='资产编号', max_length=64, blank=True, null=True)
    vendor = models.CharField(verbose_name='供应商', help_text='供应商', max_length=50, blank=True)
    use_status = models.IntegerField(verbose_name='使用状态', help_text='使用状态', choices=USE_STATUS, default=1)
    public_ip = models.GenericIPAddressField(verbose_name='公网IP', help_text='公网IP', blank=True, null=True)
    other_ip = models.GenericIPAddressField(verbose_name='其他IP', help_text='其他IP', blank=True, null=True)
    port = models.IntegerField(verbose_name='SSH端口号', help_text='SSH端口号', default=22)
    model = models.CharField(verbose_name='型号', help_text='型号', max_length=64, blank=True, null=True)
    sn = models.CharField(verbose_name='SN编号', help_text='SN编号', max_length=128, unique=True, blank=True, null=True)
    salt_status = models.IntegerField(verbose_name='SALT状态', help_text='SALT状态', choices=SALT_STATUS, blank=True,
                                      default=-1)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)
    remark = models.TextField(verbose_name='备注', help_text='备注', null=True, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = '主机资产'
        verbose_name_plural = verbose_name

    def get_fields(self):
        """
        获取字段信息
        """
        field_dict = {}
        field_required_list = []
        for field in self._meta.fields:
            field_dict[field.name] = field.verbose_name
            if field.blank and field.null:
                field_required_list

        return field_dict

    def get_table_info(self):
        """
        获取table表
        """
        data = deal_fields_Table(self._meta.fields, True, True, 2, None,None,None)
        data['field_select_kv'].append({"idc": [[row.id, row.cname] for row in Idc.objects.all()]})
        return data
