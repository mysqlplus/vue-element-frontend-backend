# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# ORM control
import json

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.contrib.auth import get_user_model
from django.utils import timezone
# from django.contrib.admin.models import LogEntry
# 获取到用户的Model，有可能是自定义的User，也可能是Django自带的User
User = get_user_model()

# Create your models here.


def get_model_path(model):
    """
    获取Model的路径
    :param model: Django的Model
    :return: 字符串型，Model的路径，比如：article.models.Category
    """
    return '{}.{}'.format(model.__module__, model.__qualname__)


class LogEntryManager(models.Manager):
    """
    日志管理器
    Django自带了LogEntry
    """

    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag,
                   message=''):
        """
        添加日志
        :param user_id: 用户的ID
        :param content_type_id: 模型内容的id
        :param object_id: 对象的id
        :param object_repr: 对象 __repr__返回值或者 __str__
        :param action_flag: 操作标志
        :param message: 消息内容，默认为空
        :return:
        """

        if isinstance(message, list):
            message = json.dumps(message)
        self.model.objects.create(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=object_id,
            object_repr=object_repr,
            action_flag=action_flag,
            message=message
        )

    def get_actions(self, user=None, action_flag=None, content_type=None, object_id=None):
        """
        获取用户的操作日志
        :param user: 用户
        :param action_flag: 操作标志：1.增加；2.修改；3.删除
        :param content_type: 模型的content_type
        :param object_id:
        :return:
        """
        if user or action_flag or content_type or object_id:
            fields_all = {'user': user, 'action_flag': action_flag,
                          'content_type': content_type, 'object_id': object_id}
            fields = {}
            for field in fields_all:
                if fields_all[field]:
                    fields[field] = fields_all[field]

            return self.filter(**fields)
        else:
            return []


@python_2_unicode_compatible
class LogsEntry(models.Model):
    """
    模型的日志
    为了跟django.contrib.admin.models.LogEntry区分，就加个s
    如果不加s，还需要制定几个related_name
    """
    ACTION_FLAG_CHOICES = (
        (1, '添加'),
        (2, '修改'),
        (3, '删除')
    )
    time_added = models.DateTimeField(verbose_name="时间", default=timezone.now, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="用户")
    # 当模型对象被删除了，日志这个字段就设置为空，所以当前字段需要允许为null
    content_type = models.ForeignKey(to=ContentType, on_delete=models.SET_NULL,
                                     verbose_name="Content Type", blank=True, null=True)
    object_id = models.IntegerField(verbose_name="对象ID")
    object_repr = models.CharField(verbose_name="对象", max_length=200)
    # 操作标志：
    action_flag = models.PositiveSmallIntegerField(verbose_name="操作标志",
                                                   choices=ACTION_FLAG_CHOICES)
    message = models.TextField(verbose_name="变更消息", blank=True)

    # 使用自定义的管理器
    objects = LogEntryManager()

    class Meta:
        verbose_name = "Model日志"
        verbose_name_plural = verbose_name
        ordering = ('-time_added', )

    def __repr__(self):
        return force_text(self.time_added)

    def __str__(self):
        return force_text(self.time_added)

    def get_edited_object(self):
        """
        返回日志对象
        """
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_message(self):
        message = self.message
        if message and message.startswith(('[', '{')):
            try:
                message = json.loads(message)
                return message
            except Exception:
                return message
        else:
            return message
