# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09

from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'logsentrys', LogsEntryViewSet, base_name='logsentry')
router.register(r'models', ContentTypeViewSet, base_name='model')

urlpatterns = router.urls
