# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  ORM类

import os
import base64
import qrcode
import pyotp
from io import BytesIO
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.signals import user_logged_in
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from utils.base_model import BaseModel
from utils.util import deal_fields_Table


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    # filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    filename = '{}.{}'.format('avatar', ext)
    return os.path.join('avatar', instance.username, filename)


class Url(models.Model):
    """
     白名单url
    """
    USER_TYPE = (
        ('customuser', '自定义用户'),
        ('anonymous', '匿名用户'),
        ('authenticated', '已认证用户'),
        # ('is_superuser', '超级管理员'),
    )
    METHOD_TYPE = [
        ('ALL', 'all'),
        ('GET', 'list/read'),
        ('POST', 'create'),
        ('PUT', 'update'),
        ('DELETE', 'delete'),
    ]
    url = models.CharField(verbose_name="URL", help_text="URL", max_length=128)
    user_type = models.CharField(verbose_name="用户类型", help_text="用户类型", max_length=16, choices=USER_TYPE,
                                 default=USER_TYPE[2])
    method = models.CharField(verbose_name='方法类型', help_text='方法类型', choices=METHOD_TYPE, max_length=10, default='ALL')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)
    remark = models.TextField(verbose_name='备注', help_text='备注', null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.method, self.url)

    class Meta:
        unique_together = ('url', 'method',)
        verbose_name = verbose_name_plural = '白名单URL'

    @classmethod
    def get_url_by_request_url(cls, url):
        return dict(menu=Url.objects.get(url=url))

    def get_fields(self):
        """
        获取字段信息
        """
        field_dict = {}
        for field in self._meta.fields:
            field_dict[field.name] = field.verbose_name
        return field_dict

    def get_table_info(self):
        """
        获取table表
        """
        data = deal_fields_Table(self._meta.fields, True, True, 3, None, None, None)
        return data


class Role(BaseModel):
    description = models.CharField(verbose_name='角色描述', help_text='角色描述', max_length=500, blank=True)
    urls = models.ManyToManyField("Url", verbose_name="url权限", help_text='url权限', blank=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = verbose_name_plural = '用户角色'

    def get_fields(self):
        """
        获取字段信息
        """
        field_dict = {}
        for field in self._meta.fields:
            field_dict[field.name] = field.verbose_name
        return field_dict

    def get_table_info(self):
        """
        获取table表
        """
        m2mField = [{"field_name": "urls", "verbose_name": "url权限", "required": False, "show": True}]
        data = deal_fields_Table(self._meta.fields, True, True, 2, m2mField, None, None)
        data['field_select_kv'].append(
            {"urls": [[row.id, row.url] for row in Url.objects.filter(user_type='customuser')]})
        data['fields']["users"] = "用户列表"
        data['field_add_novis'] = ['users','id']
        data['field_show_order'].append("users")
        return data


class Department(BaseModel):
    """
    部门
    """
    # type_choices = (("unit", "单位"), ("department", "部门"))
    # type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父类架构", on_delete=models.SET_NULL)
    description = models.CharField(verbose_name='描述', help_text='描述', max_length=500, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = "部门"


class UserProfile(AbstractUser):
    """
    用户
    """
    GENDER = (
        ('male', '男'),
        ('female', '女'),
    )
    employee_id = models.CharField(verbose_name='员工编号', help_text='员工编号', max_length=128, null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱", help_text="邮箱", max_length=100)
    phone = models.CharField(verbose_name="手机号", help_text='手机号', unique=True, max_length=11)
    cname = models.CharField(verbose_name="姓名", help_text='姓名', max_length=30)
    birthday = models.DateField(verbose_name="出生日期", help_text='出生日期', null=True, blank=True)
    gender = models.CharField(verbose_name="性别", help_text='性别', max_length=6, choices=GENDER,
                              default="male")
    last_login_ip = models.GenericIPAddressField(verbose_name='上次登录IP', help_text='上次登录IP', null=True, blank=True)
    login_count = models.IntegerField(verbose_name='登录次数', help_text='登录次数', default=0, null=True, blank=True)
    roles = models.ManyToManyField('Role', verbose_name='角色', help_text='角色', blank=True)
    # avatar = models.ImageField(upload_to=user_avatar_path, default='avatar/default.png', verbose_name="头像", help_text='头像')
    avatar = ProcessedImageField(verbose_name="头像", help_text='头像', upload_to=user_avatar_path,
                                 default='avatar/default.jpg', processors=[ResizeToFill(120, 120)],
                                 format='JPEG', options={'quality': 60}, null=True, blank=True)
    department = models.ForeignKey('Department', verbose_name="部门", help_text='部门',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位", help_text='职位')
    superior = models.ForeignKey("self", null=True, blank=True, verbose_name="上级主管", help_text='上级主管',
                                 on_delete=models.SET_NULL)
    im = models.CharField(verbose_name='IM', help_text='IM', max_length=64, null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'cname', 'phone']

    class Meta:
        verbose_name = verbose_name_plural = "用户"

    def __str__(self):
        return self.username

    def get_logged_in(self):
        if settings.MFA_ENABLE and getattr(self, 'otp', None) is not None and self.otp.is_active == True:
            logged_in = 'no'
        else:
            logged_in = 'yes'
        return logged_in

    def get_fields(self):
        """
        获取字段信息
        """
        field_dict = {}
        for field in self._meta.fields:
            field_dict[field.name] = field.verbose_name
        return field_dict

    def get_table_info(self):
        """
        获取table表
        """
        m2mField = [{"field_name": "roles", "verbose_name": "角色", "required": True, "show": False}]
        force_fields = ['id', 'username', 'cname', 'email', 'phone', 'roles', 'date_joined', 'is_active', 'employee_id']
        data = deal_fields_Table(self._meta.fields, True, True, 2, m2mField, force_fields, None)
        data['field_select_kv'].append({"roles": [[row.id, row.cname] for row in Role.objects.order_by("-id")]})
        return data


class Otp(models.Model):
    """
    双因子认证
    """
    user = models.OneToOneField(UserProfile, verbose_name='用户', help_text='用户', related_name='otp',
                                on_delete=models.CASCADE)
    secret = models.CharField(verbose_name='密钥', help_text='密钥', max_length=50, default=pyotp.random_base32)
    issuer_name = models.CharField(verbose_name='发行人名称', help_text='发行人名称', max_length=50)
    is_active = models.BooleanField(verbose_name='是否启用', help_text='是否启用', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '双因子认证'

    def __str__(self):
        return self.secret

    def get_otp_code(self) -> str:
        """
        Get current otp code
        """
        return pyotp.TOTP(self.secret).now()

    def get_otp_uri(self) -> str:
        """
        Get otp uri
        """
        return pyotp.totp.TOTP(self.secret).provisioning_uri(
            self.user.username, issuer_name=self.issuer_name
        )

    def get_qr_code(self):
        """
        Get QR code from otp uri
        """
        # 二维码的版本号，二维码总共有1到40个版本，最小的版本号是1，对应的尺寸是21×21
        QR_VERSION = 1
        # 生成图片的像素
        QR_BOX_SIZE = 10
        # 二维码的边框宽度，4是最小值
        QR_BORDER = 4
        qr = qrcode.QRCode(
            version=QR_VERSION,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=QR_BOX_SIZE,
            border=QR_BORDER
        )
        qr.add_data(self.get_otp_uri())
        qr.make(fit=True)
        img = qr.make_image()

        output = BytesIO()
        img.save(output)
        qr_data = output.getvalue()
        output.close()

        return base64.b64encode(qr_data).decode('ascii')


class OtpRecoveryCode(models.Model):
    """
    双因子认证恢复码
    """
    user = models.ForeignKey(UserProfile, verbose_name='用户', help_text='用户', on_delete=models.CASCADE)
    code = models.CharField(verbose_name='恢复码', help_text='恢复码', max_length=12, unique=True)
    is_active = models.BooleanField(verbose_name='是否启用', help_text='是否启用', default=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '双因子认证恢复码'

    def __str__(self):
        return self.code
