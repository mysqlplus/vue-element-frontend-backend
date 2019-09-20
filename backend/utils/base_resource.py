# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 导入导出 字段定义 基础类

from import_export import resources

class BaseResource(resources.ModelResource):
    def __init__(self):
        super().__init__()
        field_list = self._meta.model._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_choices_key(self, value, chioces):
        dic = {v: k for k, v in dict(chioces).items()}
        if value in dic: return dic[value]
        return value

    def get_choices_value(self, key, chioces):
        dic = dict(chioces)
        if key in dic: return dic[key]
        return key

    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
            else:
                field.column_name = field_name
        return fields