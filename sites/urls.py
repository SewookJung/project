from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.sites_main, name="sites_main"),
    re_path(r'^add/$', views.sites_add, name="sites_add"),
    re_path(r'^add/apply$', views.sites_add_apply, name="sites_add_apply"),
]
