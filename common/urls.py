from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^member/info/$', views.member_info, name="member_info"),
    re_path(r'^weekly/permission/$', views.weekly_permission,
            name="weekly_permission"),
    re_path(r'^client/dup/check/$', views.client_dup_check,
            name="client_dup_check"),
    re_path(r'^client/add/apply/$', views.client_add_apply,
            name="client_add_apply"),
    re_path(r'^get/mnfacture/(?P<mnfacture>[-\w]+)/id/$',
            views.get_mnfacture_id, name="get_mnfacture_id"),
    re_path(r'^get/model/(?P<mnfacture_id>\d+)/lists/$', views.get_product_model_lists,
            name="get_product_model_lists"),
    re_path(r'^get/model/(?P<model>[-\w]+)/id/$', views.get_model_id,
            name="get_model_id"),
]
