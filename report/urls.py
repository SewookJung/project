from django.conf.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^project/$', views.report_project, name="report_project"),
    re_path(r'^project/detail$', views.report_project_detail,
            name="report_project_detail"),
    re_path(r'^maintenance/$', views.report_maintenance,
            name="report_maintenance"),
    re_path(r'^maintenance/client/$', views.report_maintenance_client,
            name="report_maintenance_client"),
    re_path(r'^maintenance/client/detail/$', views.report_maintenance_client_detail,
            name="report_maintenance_client_detail"),
    re_path(r'^support/$', views.report_support,
            name="report_support"),
    re_path(r'^support/client/detail/$', views.report_support_detail,
            name="report_support_detail"),
    re_path(r'^edu/$', views.report_edu,
            name="report_edu"),
    re_path(r'^edu/client/detail$', views.report_edu_detail,
            name="report_edu_detail"),
    re_path(r'^etc/$', views.report_etc,
            name="report_etc"),
    re_path(r'^etc/client/detail$', views.report_etc_detail,
            name="report_etc_detail"),
]
