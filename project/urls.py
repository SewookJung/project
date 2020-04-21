"""assets_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import re_path, include
from django.urls import path
from django.contrib import admin
from login.views import redirect_root

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^assets/', include('assets.urls')),
    re_path(r'^document/', include('document.urls')),
    re_path(r'^equipment/', include('equipment.urls')),
    re_path(r'^login/', include('login.urls')),
    re_path(r'^sites/', include('sites.urls')),
    re_path(r'^weekly/', include('weekly.urls')),
    re_path(r'^$', redirect_root),
]
