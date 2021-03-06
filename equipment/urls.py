from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.equipment_main, name="equipment_main"),
    re_path(r'^info/$', views.equipment_info, name="equipment_info"),
    re_path(r'^(?P<equipment_id>\d+)/detail/$',
            views.equipment_detail, name="equipment_detail"),
    re_path(r'^(?P<equipment_id>\d+)/detail/edit/apply/$',
            views.equipment_detail_apply, name="equipment_detail_apply"),
    re_path(r'^(?P<equipment_id>\d+)/delete/$',
            views.equipment_delete, name="equipment_delete"),
    re_path(r'^form/$', views.equipment_form, name="equipment_form"),
    re_path(r'^form/apply/$', views.equipment_form_apply,
            name="equipment_form_apply"),
    re_path(r'^status/change/$', views.equipment_status_change,
            name="equipment_status_change"),
    re_path(r'^(?P<client_id>\d+)/all/list/$', views.equipment_all_list,
            name="equipment_all_list"),
    re_path(r'^(?P<client_id>\d+)/mnfacture/list/$', views.equipment_client_mnfacture_list,
            name="equipment_client_mnfacture_list"),
    re_path(r'^(?P<client_id>\d+)/(?P<mnfacture_id>\d+)/list/$', views.equipment_selected_list,
            name="equipment_selected_list"),
    re_path(r'^client/(?P<client_id>\d+)/detail/$', views.equipment_client_detail,
            name="equipment_client_detail"),
    re_path(r'^client/(?P<client_id>\d+)/(?P<mnfacture_id>\d+)/detail/$', views.equipment_mnfacture_detail,
            name="equipment_mnfacture_detail"),
    re_path(r'^client/(?P<client_id>\d+)/(?P<mnfacture_id>\d+)/(?P<model_id>\d+)/detail/$', views.equipment_model_detail,
            name="equipment_model_detail"),
    re_path(r'^upload/$', views.equipment_upload, name="equipment_upload"),
    re_path(r'^upload_check/$', views.equipment_upload_check,
            name="equipment_upload_check"),
    re_path(r'^upload_complete/$', views.equipment_upload_complete,
            name="equipment_upload_complete"),
    re_path(r'^upload_cancel/$', views.equipment_upload_cancel,
            name="equipment_upload_cancel"),
    re_path(r'^download/sample/$', views.equipment_sample_download,
            name="equipment_sample_download"),
    re_path(r'^download/sample/check/$', views.equipment_download_check,
            name="equipment_download_check"),

    re_path(r'^stock/$', views.equipment_stock, name="equipment_stock"),
    re_path(r'^stock/test/$', views.equipment_stock_test,
            name="equipment_stock_test"),
    re_path(r'^stock/form/$', views.equipment_stock_form,
            name="equipment_stock_form"),
    re_path(r'^stock/form/apply/$', views.equipment_stock_form_apply,
            name="equipment_stock_form_apply"),
    re_path(r'^stock/multi/apply/$', views.equipment_stock_multi_apply,
            name="equipment_stock_multi_apply"),
    re_path(r'^stock/multi/delete/$', views.equipment_stock_multi_delete,
            name="equipment_stock_multi_delete"),
    re_path(r'^stock/multi/return/$', views.equipment_stock_multi_return,
            name="equipment_stock_multi_return"),
    re_path(r'^stock/multi/disposal/$', views.equipment_stock_multi_disposal,
            name="equipment_stock_multi_disposal"),
    re_path(r'^stock/get/list/$', views.equipment_stock_get_list,
            name="equipment_stock_get_list"),
    re_path(r'^stock/get/list/test/$', views.equipment_stock_get_list_test,
            name="equipment_stock_get_list_test"),
    re_path(r'^stock/permission/check/$', views.equipment_stock_permission_check,
            name="equipment_stock_permission_check"),
    re_path(r'^stock/delivery/apply/$', views.equipment_stock_delivery_apply,
            name="equipment_stock_delivery_apply"),
    re_path(r'^stock/return/apply/$', views.equipment_stock_return_apply,
            name="equipment_stock_return_apply"),
    re_path(r'^stock/disposal/apply/$', views.equipment_stock_disposal_apply,
            name="equipment_stock_disposal_apply"),
    re_path(r'^stock/(?P<stock_id>\d+)/delete/$',
            views.equipment_stock_delete, name="equipment_stock_delete"),
    re_path(r'^stock/(?P<stock_id>\d+)/detail/$',
            views.equipment_stock_edit, name="equipment_stock_edit"),
    re_path(r'^stock/(?P<model_id>\d+)/(?P<model_status>\w+)/$',
            views.equipment_stock_detail, name="equipment_stock_detail"),
    re_path(r'^stock/(?P<mnfacture_id>\d+)/all/detail/$',
            views.equipment_stock_mnfacture_detail, name="equipment_stock_mnfacture_detail"),
    re_path(r'^stock/(?P<stock_id>\d+)/detail/edit/apply/$',
            views.equipment_stock_detail_apply, name="equipment_stock_detail_apply"),
    re_path(r'^stock/upload/$', views.equipment_stock_upload,
            name="equipment_stock_upload"),
    re_path(r'^stock/upload-check/$', views.equipment_stock_upload_check,
            name="equipment_stock_upload_check"),
    re_path(r'^stock/upload-complete/$', views.equipment_stock_upload_complete,
            name="equipment_stock_upload_complete"),
    re_path(r'^stock/upload-cancel/$', views.equipment_stock_upload_cancel,
            name="equipment_stock_upload_cancel"),
    re_path(r'^download/stock/sample/$', views.equipment_stock_sample_download,
            name="equipment_stock_sample_download"),
    re_path(r'^download/stock/sample/check/$', views.equipment_stock_download_check,
            name="equipment_stock_download_check"),

    re_path(r'^test/$', views.equipment_test, name="equipment_test"),
]
