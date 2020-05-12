from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.weekly_main, name="weekly_main"),
    re_path(r'^add/$', views.weekly_add, name="weekly_add"),
    re_path(r'^add/apply/$', views.weekly_add_apply, name="weekly_add_apply"),
    re_path(r'^(?P<selected_id>\d+)/(?P<selected_all>\d+)/$',
            views.weekly_main, name="weekly_main"),
    re_path(r'^(?P<client_id>\d+)/(?P<product_id>\d+)/(?P<selected_id>\d+)/detail/$',
            views.weekly_detail, name="weekly_detail"),
    re_path(r'^edit/(?P<client_id>\d+)/$', views.weekly_detail_apply,
            name="weekly_detail_apply"),
    re_path(r'^(?P<report_id>\d+)/detail/$',
            views.weekly_report_detail, name="weekly_report_detail"),
    re_path(r'^edit/report/(?P<report_id>\d+)/$',
            views.weekly_report_detail_apply, name="weekly_report_detail"),
    re_path(r'^(?P<pk>\d+)/delete/$',
            views.weekly_delete, name="weekly_delete"),
]
