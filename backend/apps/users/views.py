# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  业务 contorl
import re
import json
import logging
import pyotp
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_encode_handler, jwt_payload_handler
from utils.base_mixin import ImportMixin, ExportMixin
from utils.util import random_char_list, send_sms, send_html_mail, Token, request_get
from utils.base_view import BaseModelViewSet, BaseGenericViewSet
from social_django.models import UserSocialAuth
from .util import get_ip_address, login_set_cookie, logout_del_cookie, login_set_otp_cookie, perform_create_user, \
    perform_update_user, perform_destroy_user, ldap_change_password
from .serializers import *
from .resources import *
from .models import *
from .filters import *


logger = logging.getLogger('views')

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, BaseGenericViewSet):
    """
    个人中心
    """
    queryset = []

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        elif self.action == 'modify':
            return UserUpdateSerializer
        elif self.action == 'upload_avatar':
            return AvatarSerializer
        elif self.action == 'change_password':
            return PasswordSerializer
        elif self.action == 'email_reset_password':
            return EmailResetPasswordSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        elif self.action == 'send_sms_code':
            return SmsCodeSerializer
        elif self.action == 'send_email_code':
            return EmailCodeSerializer
        elif self.action == 'phone_login':
            return PhoneLoginSerializer
        elif self.action == 'del_social':
            return SocialProviderSerializer
        elif self.action == 'login':
            return JSONWebTokenSerializer
        elif self.action == 'otp':
            return OtpSerializer
        elif self.action == 'otp_login':
            return OtpLoginSerializer
        elif self.action == 'otp_recovery_codes':
            return OtpRecoveryCodeSerializer
        elif self.action == 'otp_recovery_code_login':
            return OtpRecoveryCodeLoginSerializer
        elif self.action == 'otp_disable':
            return OtpDisableSerializer
        elif self.action == 'otp_enable':
            return OtpEnableSerializer
        elif self.action == 'sso_user_info':
            return SsoUserInfoSerializer
        return UserDetailSerializer

    # def get_permissions(self):
    #     action_list = ['create', 'send_sms_code', 'email_reset_password', 'reset_password', 'login', 'phone_login',
    #                    'logout', 'ssologin']
    #     if self.action in action_list: return []
    #     return super().get_permissions()

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        instance = serializer.save()
        perform_create_user(instance)

    @action(methods=['put'], detail=False)
    def modify(self, request):
        """
        修改用户信息
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        perform_update_user(instance)
        return Response({'status': 'ok'})

    @action(methods=['put'], detail=False)
    def change_password(self, request):
        """
        修改密码
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data["old_password"]
        password = serializer.validated_data["password"]
        if user.check_password(old_password):
            user.set_password(password)
            user.save()
            ldap_change_password(user, password)
            return Response({'status': 'ok'})
        else:
            return Response({'detail': ['旧密码错误']}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def email_reset_password(self, request):
        """
        通过邮箱重置密码
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user_obj = User.objects.get(email=email)
            token_obj = Token()
            token = token_obj.generate_validate_token(email)
            reset_url = '{}/#/resetpwd?token={}'.format(settings.PROJECT_URL, token)
            subject = '重置您的密码'
            content = '<br>{}，您好：<br><br>    点击以下链接重置您的密码： {} <br><br>如果您没有请求重置密码，请忽略该邮件。'.format(
                user_obj.username, reset_url)
            send_html_mail(user_obj.email, subject, content)
        except Exception as e:
            return Response({'detail': ['邮箱不存在']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'ok'})

    @action(methods=['post'], detail=False)
    def reset_password(self, request):
        """
        重置密码
        """
        token = request.query_params.get('token', None)
        if token is None: return Response({'detail': ['参数错误']}, status=status.HTTP_400_BAD_REQUEST)
        token_obj = Token()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        try:
            email = token_obj.confirm_validate_token(token, expiration=600)
            user_obj = User.objects.get(email=email)
            user_obj.set_password(password)
            user_obj.save()
            ldap_change_password(user_obj, password)
        except Exception as e:
            return Response({'detail': ['token错误']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'ok'})

    @action(methods=['get'], detail=False)
    def info(self, request):
        """
        用户详情
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def sso_user_info(self, request):
        """
        用户
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def urls(self, request):
        """
        用户有权限
        """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        '''
        账号密码登录
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        auth_login(request, user)
        logged_in = user.get_logged_in()
        request.session['logged_in'] = logged_in
        # 记录登录IP、统计登录次数
        user.login_count += 1
        ip = get_ip_address(request)
        if ip:
            user.last_login_ip = ip
            user.save()
        response = Response({'username': user.username, 'token': token})
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        response = login_set_cookie(response, token, domain=domain, logged_in=logged_in)
        return response

    @action(methods=['post'], detail=False)
    def phone_login(self, request):
        """
        手机验证码登录
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        try:
            user = User.objects.get(phone=phone)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            logged_in = user.get_logged_in()
            request.session['logged_in'] = logged_in
            # 记录登录IP、统计登录次数
            user.login_count += 1
            ip = get_ip_address(request)
            if ip:
                user.last_login_ip = ip
                user.save()
            domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
            response = Response({'username': user.username, 'token': token})
            response = login_set_cookie(response, token, domain, logged_in=logged_in)
            return response
        except Exception as e:
            return Response({"detail": e[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def logout(self, request, *args, **kwargs):
        '''
        退出登录
        '''
        auth_logout(request)
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        redirect = request.query_params.get('redirect', '/')
        if settings.SSO_CLIENT_ENABLE:
            redirect = 'http://sso.siku.cn/auth-web/?redirectUrl={}#/logout'.format(settings.PROJECT_URL)
        response = HttpResponseRedirect(redirect)
        response = logout_del_cookie(response, domain)
        #if tokenKey:
        #   sso_logout_url = 'https://flying.siku.cn/auth/login/logout?tokenKey={}'.format(tokenKey)
        #   r, err = request_get(sso_logout_url)
        #   if err: return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        #response.delete_cookie('tokenKey', domain=domain)
        return response

    @action(methods=['get'], detail=False)
    def ssologin(self, request, *args, **kwargs):
        '''
        单点登录
        '''
        tokenKey = request.query_params.get('tokenKey', '')
        redirect = request.query_params.get('redirect', '')
        redirect_url = 'http://sso.siku.cn/auth-web/?redirectUrl={}{}'.format(settings.PROJECT_URL,request.get_full_path())
        if not tokenKey:
            response = HttpResponseRedirect(redirect_url)
            return response
        get_user_info_url = 'http://flying.siku.cn/auth/login/findLoginUser?tokenKey={}'.format(tokenKey)
        r,err = request_get(get_user_info_url)
        if err: return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        rets = r.json()
        if not rets['data']: return HttpResponseRedirect(redirect_url)
        data = json.loads(rets['data'])
        d = {}
        email = data['userEmail']
        username = email.split('@')[0]
        d['email'] = email
        d['username'] = username
        d['phone'] = data['userPhone']
        d['cname'] = data['userName']
        d['employee_id'] = data['userJobNumber']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = User.objects.create(**d)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        logged_in = user.get_logged_in()
        request.session['logged_in'] = logged_in
        # 记录登录IP、统计登录次数
        user.login_count += 1
        ip = get_ip_address(request)
        if ip:
            user.last_login_ip = ip
            user.save()
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        if redirect:
            response = HttpResponseRedirect(redirect)
        else:
            response = HttpResponseRedirect(settings.PROJECT_URL)
        #response.set_cookie('tokenKey', tokenKey,domain=domain)
        #response = Response({'username': user.username, 'token': token})
        response = login_set_cookie(response, token, domain, logged_in=logged_in)
        return response

    @action(methods=['put'], detail=False)
    def upload_avatar(self, request):
        """
        上传头像
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.get_object(), self.request.data)
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def send_sms_code(self, request):
        """
        发送短信验证码
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        char_list = map(str, random_char_list(4))
        code = ''.join(char_list)
        try:
            cache.set(phone, code, 3 * 60)
            content = '您的验证码是: %s ,该验证码有效期3分钟, 如非本人操作请忽略此短信!' % code
            send_sms(phone, content)
        except Exception as e:
            return Response({"detail": e[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"phone": phone}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def send_email_code(self, request):
        """
        发送邮箱验证码
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        char_list = map(str, random_char_list(4))
        code = ''.join(char_list)
        try:
            cache.set(email, code, 3 * 60)
            subject = content = '您的验证码是: %s ,该验证码有效期3分钟, 如非本人操作请忽略此邮件!' % email_code
            send_html_mail(email, subject, content)
        except Exception as e:
            return Response({"detail": e[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"email": email}, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def social(self, request):
        """
        已绑定第三方登录列表
        """
        user = self.get_object()
        queryset = UserSocialAuth.objects.filter(user_id=user.id)
        serializer = UserSocialAuthSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def del_social(self, request):
        """
        解除第三方登录
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]
        UserSocialAuth.objects.filter(user_id=user.id, provider=provider).delete()
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def social_login_set_cookie(self, request, *args, **kwargs):
        '''
        第三方登录成功后种cookie
        '''
        user = self.get_object()
        payload = jwt_payload_handler(user)
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        token = jwt_encode_handler(payload)
        request.session['logged_in'] = user.get_logged_in()
        response = HttpResponseRedirect('/')
        # response = login_set_cookie(response, token, domain, logged_in=logged_in)
        response = login_set_cookie(response, token, domain)
        return response

    @action(methods=['get'], detail=False)
    def otp(self, request):
        """
        获取双因子认证信息
        """
        user = self.get_object()
        if getattr(user, 'otp', None) is not None:
            instance = user.otp
        else:
            data = {}
            data['user'] = user
            data['secret'] = pyotp.random_base32()
            data['issuer_name'] = settings.PROJECT_ZHNAME
            instance = Otp.objects.create(**data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def otp_enable(self, request):
        """
        开启双因子认证
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.data["otp_code"]
        if not hasattr(user, 'otp'): return Response({'detail': ['用户Otp表记录不存在']}, status=status.HTTP_400_BAD_REQUEST)
        otp_instance = user.otp
        if otp_instance.get_otp_code() != otp_code:
            return Response({'detail': ['动态码错误']}, status=status.HTTP_400_BAD_REQUEST)
        otp_instance.is_active = True
        otp_instance.save()
        otp_recovery_codes = generate_otp_recovery_code(user)
        return Response(otp_recovery_codes)

    @action(methods=['post'], detail=False)
    def otp_disable(self, request):
        """
        关闭双因子认证
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data["password"]
        if not user.check_password(password):
            return Response({'detail': ['账号密码错误']}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(user, 'otp'): user.otp.delete()
        user.otprecoverycode_set.all().delete()
        return Response({'status': 'ok'})

    @action(methods=['post'], detail=False)
    def otp_login(self, request):
        '''
        双因子认证 动态码登录
        '''
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.data["otp_code"]
        if user.otp.get_otp_code() != otp_code:
            return Response({'detail': ['动态码错误']}, status=status.HTTP_400_BAD_REQUEST)
        logged_in = 'yes'
        request.session['logged_in'] = logged_in
        response = Response({'username': user.username, 'otp_code': otp_code})
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        response = login_set_otp_cookie(response, domain=domain, logged_in=logged_in)
        return response

    @action(methods=['post'], detail=False)
    def otp_recovery_login(self, request):
        '''
        双因子认证 动态码恢复码登录
        '''
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.data["code"]
        if not user.otprecoverycode_set.filter(code=code, is_active=True):
            return Response({'detail': ['恢复码错误']}, status=status.HTTP_400_BAD_REQUEST)
        logged_in = 'yes'
        request.session['logged_in'] = logged_in
        response = Response({'username': user.username, 'code': code})
        domain = re.search(r'(?<=\.)\w+\.\w+$', request.META['HTTP_HOST'].split(':')[0]).group()
        response = login_set_otp_cookie(response, domain=domain, logged_in=logged_in)
        return response

    @action(methods=['get'], detail=False)
    def otp_recovery_codes(self, request):
        """
        动态码恢复码列表
        """
        user = self.get_object()
        queryset = OtpRecoveryCode.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RoleViewSet(BaseModelViewSet):
    queryset = Role.objects.order_by('-id')
    serializer_class = RoleSerializer
    ordering_fields = ('id', 'name')
    search_fields = ('name', 'cname')

    def get_serializer_class(self):
       if self.action == 'add_user' or self.action == 'remove_user' or self.action == 'add_users':
           return RoleUserSerializer
       else:
           return self.serializer_class

    @action(methods=['post'], detail=True)
    def add_user(self, request, pk):
        """
        添加用户
        """
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ids = serializer.data["users"]
        users = User.objects.filter(pk__in=user_ids)
        for add_user in users:
            add_user.roles.add(instance)
        return Response({'status': 'ok'})

    @action(methods=['post'], detail=True)
    def remove_user(self, request, pk):
        """
        移除用户
        """
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ids = serializer.data["users"]
        users = User.objects.filter(pk__in=user_ids)
        for del_user in users:
            del_user.roles.remove(instance)
        return Response({'status': 'ok'})

class UrlViewSet(BaseModelViewSet):
    queryset = Url.objects.order_by('-id')
    serializer_class = UrlSerializer
    ordering_fields = ('id', 'url')
    search_fields = ('user_type', 'url', 'method')
    filterset_class = UrlFilter


class UsersViewSet(ImportMixin, ExportMixin, BaseModelViewSet):
    # queryset = User.objects.filter(is_active=True).order_by('-id')
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
    ordering_fields = ('id', 'username')
    search_fields = ('username', 'cname', 'phone', 'email')
    filterset_class = UsersFilter
    resource_class = UserResource

    def get_serializer_class(self):
        if self.action == 'get_users':
            return GetUsersSerializer
        elif self.action == 'import_data':
            return self.import_data_serializer_class
        else:
            return self.serializer_class

    @action(methods=['get'], detail=False)
    def get_users(self, request):
        """
        获取用户列表，登录用户有权限,用于选择用户下拉框
        """
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['delete'], detail=True)
    def leaved(self, request, pk):
        """
        离职
        """
        instance = self.get_object()
        if instance.is_active:
            perform_destroy_user(instance, self.request.user)
            instance.username = 'leaved_{}'.format(instance.username)
            instance.email = 'leaved_{}'.format(instance.email)
            instance.roles.clear()
            instance.is_active = False
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        perform_destroy_user(instance, self.request.user)

class OtpViewSet(BaseModelViewSet):
    queryset = Otp.objects.all()
    serializer_class = OtpSerializer
    ordering_fields = ('id',)
    search_fields = ('secret', 'issuer_name', 'user__username')
    # filterset_class = DbClusterFilter
