# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 导入到处 中间件 基础类

import datetime
import logging
import xlrd
import tablib
from django.utils.six import moves
from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from utils.util import Prpcrypt

logger = logging.getLogger('views')

class SetEncryptMixin(object):
    encrypt_field = 'passwd'

    def create(self, validated_data):
        password = validated_data.get(self.encrypt_field)
        validated_data[self.encrypt_field] = Prpcrypt.encrypt(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get(self.encrypt_field)
        if password != instance.__dict__[self.encrypt_field]:
            validated_data[self.encrypt_field] = Prpcrypt.encrypt(password)
        return super().update(instance, validated_data)


class ExportMixin(object):
    @action(methods=['get'],detail=False)
    def export_data(self, request):
        '''
        导出数据<br>
            query_params:<br>
                file_format: 文件格式：xls、csv、json、html、yaml，默认：xls<br>
                filename: 文件名，默认：download.xls<br>
                scope: 导出范围：all、header_only、selected (选中的，以英文逗号分隔)，默认：all<br>
                
        '''
        resource = self.resource_class()
        model = resource._meta.model
        file_format = request.query_params.get('file_format', 'xls')
        filename = request.query_params.get('filename', '{}-{}.{}'.format(model._meta.model_name, datetime.datetime.now().strftime('%Y-%m-%d'), file_format))
        scope = request.query_params.get('scope', 'all')
        ids = request.query_params.get('ids', '')
        if scope == 'all':
            queryset = self.filter_queryset(self.get_queryset())
        elif scope == 'header_only':
            queryset = []
        elif scope == 'selected':
            queryset = []
            if ids: queryset = self.filter_queryset(self.get_queryset().filter(pk__in=ids.split(',')))
        export_data = resource.export(queryset)
        export_data.title = model._meta.verbose_name
        content_type = '{};charset=gbk'.format(settings.CONTENT_TYPE[file_format])
        response = HttpResponse(getattr(export_data,file_format), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(label="上传文件", help_text="上传文件", required=True)

class ImportMixin(object):

    import_data_serializer_class = UploadSerializer

    def create_dataset(self, in_stream, format, **kwargs):
        dataset = tablib.Dataset()
        if format == 'json': dataset.json = in_stream
        if format == 'csv': dataset.csv = in_stream
        if format == 'xls':
            xls_book = xlrd.open_workbook(file_contents=in_stream)
            sheet = xls_book.sheets()[0]
            dataset.headers = sheet.row_values(0)
            for i in moves.range(1, sheet.nrows):
                dataset.append(sheet.row_values(i))
        return dataset

    @action(methods=['post'],detail=False)
    def import_data(self, request):
        ''' 
        导入数据<br>
            param：<br>
                file: 文件: json、csv、xls格式文件，默认: xls格式<br>
        '''
        file_format = request.query_params.get('file_format', 'xls')
        import_file = request.FILES['file']
        resource = self.resource_class()
        dataset = self.create_dataset(import_file.read(), file_format)
        result = resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            errors = ['{}:{}'.format(row[1][0].error,str(row[1][0].row)) for row in result.row_errors()]
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = resource.import_data(dataset, dry_run=False)
        return Response(result.totals)

    @action(methods=['post'],detail=False)
    def import_json_data(self, request):
        ''' 
        前端JSON数据导入<br>
            param：<br>
                jsondata: json数据<br>
        '''
        data = request.data['jsondata']
        resource = self.resource_class()
        dataset = tablib.Dataset()
        dataset.json = data
        result = resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            errors = [str(row[1][0].error) for row in result.row_errors()]
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = resource.import_data(dataset, dry_run=False)
        return Response(result.totals)

