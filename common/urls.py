from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^member/info/$', views.member_info, name="member_info"),
    re_path(r'^weekly/permission/$', views.weekly_permission,
            name="weekly_permission"),
]
