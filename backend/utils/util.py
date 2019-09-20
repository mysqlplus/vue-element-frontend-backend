# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 工具 基础类

import json
import pytz
import datetime
import decimal
import base64
import logging
import subprocess
from django.core.mail import EmailMessage
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer as utsr
from cryptography.fernet import Fernet
from django.db import models
from inspect import isfunction
from xpinyin import Pinyin

logger = logging.getLogger('views')


def local_cmd(cmd, iswait=True):
    """
    执行Shell命令
    """
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if iswait: ret.wait()
    return ret


def is_valid_mobile_phone(phone):
    '''
    判断是否为手机号
    '''
    import re
    return re.match('^1[34578]\d{9}$', phone)


def is_safe_password(password):
    '''
    检查密码强度
    密码要求包含大小写字母和数字,密码长度至少8位
    '''
    import re
    return re.match('(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', password)


def make_crypt_password(password, salt=settings.SECRET_KEY):
    '''
    crypt加密
    '''
    import crypt
    return crypt.crypt(password, salt)


def random_char_list(num, type=1):
    # type 1:纯数字 2:纯小写字母 3:数字+小写字母 4: 数字+小写字母+大写字母
    import random
    if type == 1:
        chars = list(range(10))
    elif type == 2:
        chars = [chr(i) for i in range(97, 123)]
    elif type == 3:
        chars = list(range(10)) + [chr(i) for i in range(97, 123)]
    elif type == 4:
        chars = list(range(10)) + [chr(i) for i in range(65, 91) + range(97, 123)]
    else:
        return []
    return random.sample(chars, num)


def make_password(length=8):
    '''
    生成随机密码
    '''
    from random import choice
    import string
    chars = string.ascii_letters + string.digits
    return ''.join([choice(chars) for i in range(length)])


def request_get(url, timeout=5, headers=None):
    """
    发送get请求
    默认超时5秒
    默认http请求，如果https请求url中必须是https://开发
    headers = {'User-Agent': 'hhrtest'}
    ret, err = request_get('http://ip.taobao.com/service/getIpInfo.php?ip=122.88.60.28', headers=headers)
    if not err: print ret.text
    状态码：ret.status_code
    返回Unicode型的数据，如文本文件：ret.text
    返回bytes型也就是二进制的数据，如图片、文件等：ret.content
    返回json数据：ret.json()
    headers: ret.request.headers['User-Agent']
    直接获取返回json串内容 ret.json()['data']['country']
    """
    import re
    import requests
    ret = err = None
    requests.packages.urllib3.disable_warnings()
    if not re.match('https?://', url.strip()): url = 'http://' + url
    try:
        ret = requests.get(url, timeout=timeout, headers=headers)
    except Exception as e:
        return ret, e
    return ret, err


def request_post(url, post_data, timeout=5, headers=None):
    """
    发送post请求
    默认http请求，如果https请求url中必须是https://开发
    post_data = {'key1': 'value1', 'key2': 'value2'}
    ret, err = request_post('http://httpbin.org/post', post_data=post_data)
    if not err: print ret.text
    状态码：ret.status_code
    文本内容：ret.text
    headers: ret.request.headers['User-Agent']
    直接获取返回json串内容 ret.json()['data']['country']
    """
    import re
    import requests
    ret = err = None
    requests.packages.urllib3.disable_warnings()
    if not re.match('https?://', url.strip()): url = 'http://' + url
    try:
        ret = requests.post(url, post_data, timeout=timeout, headers=headers)
    except Exception as e:
        return ret, e
    return ret, err


def send_sms(phones, content):
    """
    发送短信
    """
    headers = {"Token": settings.HERMES_TOKEN}
    for phone in phones.split(','):
        data = {'phone': phone, 'content': content}
        ret, err = request_post(settings.HERMES_API + '/send/sms/', data, headers=headers)
        if err: logger.error(err)
    return 'done'

def send_html_mail(tos, subject, content, fromer=None, cc=None, bcc=None):
    '''
    发送html邮件
    '''
    if fromer:
        _fromer = '%s<%s>' % (fromer, settings.EMAIL_HOST_USER)
    else:
        _fromer = settings.EMAIL_HOST_USER

    msg = EmailMessage(subject, content, _fromer, tos.split(','))
    msg.content_subtype = "html"
    if cc: msg.cc = cc.split(',')
    if bcc: msg.bcc = bcc.split(',')
    ret = msg.send(fail_silently=True)
    if ret == 1:
        ret = True
    else:
        ret = False
    return ret


# True 第一个表示是否使用默认搜索（所有的select都成为搜索条件）
# True 第二个 是否开启 多选搜索
# 第三个表示 排序  1表示使用 requiredlist值作为show 2。需要调整的放到后边，3,全部显示
# 参数isShow  显示顺序 几种 组合
# m2mList 多选  添加  一般处理多对多 字段
# 参数 forceFields 强制 字段  编辑，查看，v表，只显示这几个 None 无效
def deal_fields_Table(fields, isSearchDef, isSearchMulDef, isShow, m2mList, forceFields,hiddenFields):
    '''
    处理fields 生成 创建前端 table 需要的属性
    '''
    table_dict = {}
    field_dict = {}
    field_select_list = []
    field_select_mul_list = []
    field_select_kv_list = []
    field_textarea_list = []
    field_radio_list = []
    field_datetime_list = []
    field_date_list = []
    field_time_list = []
    field_required_list = []
    field_default_list = []

    for field in fields:
        if forceFields and field.name not in forceFields:
            continue
        # name
        field_dict[field.name] = field.verbose_name

        # type
        if isinstance(field, models.TextField):
            field_textarea_list.append(field.name)
        elif isinstance(field, models.BooleanField):
            field_radio_list.append(field.name)
        elif isinstance(field, models.ForeignKey):
            field_select_list.append(field.name)
        elif isinstance(field, models.ManyToManyField):
            field_select_mul_list.append(field.name)

        elif isinstance(field, models.DateTimeField):
            field_datetime_list.append(field.name)
        elif isinstance(field, models.DateField):
            field_date_list.append(field.name)
        elif isinstance(field, models.TimeField):
            field_time_list.append(field.name)

        # select add value lable
        if field.choices and len(field.choices) > 0:
            field_select_list.append(field.name)
            field_select_kv_list.append({field.name: field.choices})

        # valueDefault
        if field.default is not models.fields.NOT_PROVIDED and isfunction(field.default) is False:
            if field.default != -1:
                field_default_list.append({field.name: field.default})

        # required
        if field.blank is False:
            field_required_list.append(field.name)

    # 调整顺序
    if forceFields:
        field_dict_tmp = {}
        table_dict["field_show_order"] = []
        for f in forceFields:
            if f in field_dict:
                field_dict_tmp[f] = field_dict[f]
                table_dict["field_show_order"].append(f)

        table_dict["fields"] = field_dict_tmp

    else:
        table_dict["fields"] = field_dict

    table_dict["field_required"] = field_required_list

    table_dict["field_type"] = {}

    table_dict["field_type"]["select"] = field_select_list
    table_dict["field_type"]["select_mul"] = field_select_mul_list
    table_dict["field_type"]["textarea"] = field_textarea_list
    table_dict["field_type"]["radio"] = field_radio_list
    table_dict["field_type"]["datetime"] = field_datetime_list
    table_dict["field_type"]["date"] = field_date_list
    table_dict["field_type"]["time"] = field_time_list

    table_dict["field_default"] = field_default_list

    table_dict["field_select_kv"] = field_select_kv_list
    table_dict["field_sort"] = ['id']

    table_dict["field_add_remove"] = []
    table_dict["field_update_remove"] = []

    if isSearchDef:
        table_dict["field_search"] = field_select_list + field_radio_list
    if isSearchMulDef:
        table_dict["field_search_mul"] = field_select_mul_list

    table_dict["field_after_order"] = ["create_time", "update_time", "remark"]
    if hiddenFields:
        table_dict["field_hidden"] = ["id", "create_time", "update_time", "remark"]+hiddenFields
    else:
        table_dict["field_hidden"] = ["id", "create_time", "update_time", "remark"]
    # 默认顺序
    if isShow == 1:
        table_dict["field_show_order"] = field_required_list
        field_hidden_list = []
        for key in field_dict:
            if key not in field_required_list:
                field_hidden_list.append(key)
        table_dict["field_hidden"] = field_hidden_list
    # 默认这几个并且没有调整过顺序
    elif isShow == 2:
        if forceFields is None:
            field_show_list = []
            for key in field_dict:
                if key not in table_dict["field_after_order"]:
                    field_show_list.append(key)
            table_dict["field_show_order"] = field_show_list
    # all 显示所有
    elif isShow == 3:
        field_show_list = []
        for key in field_dict:
            field_show_list.append(key)
        table_dict["field_show_order"] = field_show_list
        table_dict["field_hidden"] = []

    # 多选
    if m2mList:
        for filed in m2mList:
            table_dict["fields"][filed["field_name"]] = filed["verbose_name"]
            table_dict["field_type"]["select"].append(filed["field_name"])
            table_dict["field_type"]["select_mul"].append(filed["field_name"])
            if filed["required"]:
                table_dict["field_required"].append(filed["field_name"])
            if filed["show"]:
                table_dict["field_show_order"].append(filed["field_name"])

    table_dict['field_add_novis'] = []
    return table_dict


class Token:
    def __init__(self, security_key=settings.SECRET_KEY):
        self.security_key = security_key
        self.salt = base64.encodestring(bytes(security_key, 'utf-8')).strip()

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)


class Prpcrypt:
    key = 'absdfasdfasdfasdfawefasdfasdfasfd09_dasf_@##_d'

    @classmethod
    def encrypt(cls, password):
        fn = Fernet(cls.key)
        password_encode = password.encode()
        token = fn.encrypt(password_encode)
        return token.decode()

    @classmethod
    def decrypt(cls, password):
        fn = Fernet(cls.key)
        password_encode = password.encode()
        token = fn.decrypt(password_encode)
        return token.decode()


class DateEncoder(json.JSONEncoder):
    ''' 数据解码器 '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def convert_from_utc(date_time,time_zone):
    tz = pytz.timezone(time_zone)
    utc = pytz.timezone('UTC')
    return date_time.replace(tzinfo=utc).astimezone(tz)

def utc2local(utc_dtm):
    # UTC时间转本地时间
    local_tm = datetime.datetime.fromtimestamp(0)
    utc_tm = datetime.datetime.utcfromtimestamp(0)
    offset = local_tm - utc_tm
    return utc_dtm + offset

def local2utc(local_dtm):
    # 本地时间转UTC时间
    return datetime.datetime.utcfromtimestamp(local_dtm.timestamp())

def get_pinyin(zh_name):
    ''' 中文转拼音 '''
    p = Pinyin()
    return p.get_pinyin(zh_name, '')