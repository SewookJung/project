from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^$', views.assets_main, name="assets_main"),
    re_path(r'^add/$', views.assets_add, name="assets_add"),
    re_path(r'^add/apply$', views.assets_add_apply, name="asset_add_apply"),
    re_path(r'^status/$', views.assets_status, name="assets_status"),
    re_path(r'^status/apply/$', views.assets_rent, name="assets_rent"),
    re_path(r'^status/return/$',
            views.assets_return, name="assets_return"),
]
