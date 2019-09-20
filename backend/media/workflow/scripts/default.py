#!/usr/bin/env python
#coding=utf-8
import os
import sys
import json
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from django.conf import settings
from workflow.models import WorkOrder

try:
    workorder_id = sys.argv[1]
    log_file = '{}/logs/workflow/{}.log'.format(settings.BASE_DIR, workorder_id)
    instance = WorkOrder.objects.get(pk=workorder_id)
    workflow = instance.workflow
    #Form表单数据
    data = json.loads(instance.data)
    print('python -u {} {} &>{}'.format(workflow.script.path, workorder_id, log_file))
    print('脚本开始执行')
    print('task_mark_percent=10')
    print('申请人是{}'.format(instance.creator))
    #time.sleep(10)
    #如果脚本执行失败打印task_mark_error=1
    #print('task_mark_error=1')
    print('脚本已执行完成')
except Exception as e:
    print('脚本执行失败: {}'.format(e))
    print('task_mark_error=1')
finally:
    print('task_mark_percent=100')