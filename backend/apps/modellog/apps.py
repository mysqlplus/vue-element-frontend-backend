import os
from django.apps import AppConfig

app_name = os.path.basename(os.path.dirname(__file__))

class AppConfig(AppConfig):
    name = app_name
    verbose_name = '操作日志记录管理'
