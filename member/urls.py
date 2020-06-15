from django.conf.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.member_profile, name="member_profile"),
    re_path(r'^password/$', views.member_password, name="member_password"),
    re_path(r'^password/apply/$', views.member_password_apply,
            name="member_password_apply"),
]
