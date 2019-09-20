# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
#  url mapping  类
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register(r'idcs', IdcViewSet)
router.register(r'hosts', HostViewSet)
urlpatterns = router.urls
