"""djangoday4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import ckeditor_uploader
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from djangoday4.settings import MEDIA_ROOT
from user.views import index

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', index, name='index'),
    path('user/', include('user.urls', namespace='user')),
    path('article/', include('article.urls', namespace='article')),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 加载ckeditor的urls
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

]
