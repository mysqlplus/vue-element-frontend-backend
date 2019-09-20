# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  url mapping
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, base_name='user')
router.register(r'users', UsersViewSet, base_name='users')
router.register(r'urls', UrlViewSet, base_name='urls')
router.register(r'roles', RoleViewSet, base_name='roles')
router.register(r'otps', OtpViewSet, base_name='otps')
urlpatterns = router.urls