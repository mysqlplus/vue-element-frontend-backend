# -*- coding: utf-8 -*-
#author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
#create:2018-09
# 总体 url mapping控制


from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
import xadmin

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^xadmin/', xadmin.site.urls),
    url('^swagger-docs/', get_schema_view(title=settings.PROJECT_ZHNAME, renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])),
    url(r'^docs/', include_docs_urls(title=settings.PROJECT_ZHNAME, permission_classes=[])),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'social/', include('social_django.urls', namespace='social')),
]
#自动添加路由
urls = [url(r'^api/v1/{}/'.format(app),  include('{}.urls'.format(app))) for app in settings.APPS]
urlpatterns.extend(urls)