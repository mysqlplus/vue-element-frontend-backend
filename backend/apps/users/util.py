# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  工具类
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from ipware import get_client_ip
from utils.util import send_html_mail, make_password, make_crypt_password, random_char_list
from .ldap_tool import LdapTool

def get_ip_address(request):
    """
    返回request里的IP地址
    提示：
        为了开发方便，这个函数会返回类似127.0.0.1之类无法在公网被路由的地址，
        在生产环境中，类似地址不会被返回
    """
    ip, is_routable = get_client_ip(request)
    if settings.DEBUG:
        return ip
    else:
        if ip is not None and is_routable:
            return ip
    return None

def login_set_cookie(response, token, domain=None, logged_in='no'):
    response.set_cookie('logged_in', logged_in, max_age=api_settings.JWT_EXPIRATION_DELTA.total_seconds(),domain=domain)
    response.set_cookie(settings.TOKEN_NAME, token, max_age=api_settings.JWT_EXPIRATION_DELTA.total_seconds(),domain=domain)
    response.set_cookie('token_name', settings.TOKEN_NAME, max_age=api_settings.JWT_EXPIRATION_DELTA.total_seconds(),domain=domain)
    return response

def logout_del_cookie(response, domain=None):
    response.delete_cookie('logged_in', domain=domain)
    response.delete_cookie(settings.TOKEN_NAME, domain=domain)
    response.delete_cookie('token_name', domain=domain)
    return response

def login_set_otp_cookie(response, domain=None, logged_in='yes'):
    ''' 双因子认证登录更新logged_in '''
    response.set_cookie('logged_in', logged_in, max_age=api_settings.JWT_EXPIRATION_DELTA.total_seconds(),domain=domain)
    return response

def generate_otp_recovery_code(user):
    OtpRecoveryCode.objects.filter(user=user).delete()
    code_list = []
    for row in xrange(3):
        code = random_char_list(12, 3)
        code_list.append(code)
        OtpRecoveryCode.objects.create(user=user,code=code,is_active=True)
    return code_list

def perform_create_user(instance):
    password = make_password()
    instance.set_password(password)
    instance.save()
    subject = '运维云平台账号已开通，请登录自行修改密码'
    content = '<br>{}，您好：<br><br>    您的账号: {} ,密码: {}<br> <a href="{}" target="_blank">运维云平台</a> 请登录自行修改密码并妥善保管，谢谢！'.format(
        instance.cname, instance.username, password, settings.PROJECT_URL)
    send_html_mail(instance.email, subject, content)
    if settings.LDAP_ENABLE:
        data = {}
        uid = instance.email.split('@')[0]
        data['uid'] = uid
        data['cn'] = uid
        data['sn'] = instance.cname
        data['telephonenumber'] = instance.phone
        data['mail'] = instance.email
        data['userPassword'] = '{crypt}' + make_crypt_password(password)
        s = LdapTool()
        s.add_user(data)

def perform_update_user(instance):
    if settings.LDAP_ENABLE:
        data = {}
        data['sn'] = instance.cname
        data['telephonenumber'] = instance.phone
        data['mail'] = instance.email
        s = LdapTool()
        s.modify_user(instance.username, attrs=data)

def perform_destroy_user(instance, operator):
    subject = 'LDAP账号删除通知'
    content = '<br>{}({})的LDAP账号已由管理员({})删除！'.format(instance.username, instance.cname, operator.username)
    send_html_mail(settings.ADMIN_EMAIL, subject, content)
    if settings.LDAP_ENABLE:
        s = LdapTool()
        s.del_user(instance.username)

def ldap_change_password(instance, password):
    if settings.LDAP_ENABLE:
        data = {}
        data['userPassword'] = '{crypt}' + make_crypt_password(password)
        s = LdapTool()
        s.modify_user(instance.username, attrs=data)
