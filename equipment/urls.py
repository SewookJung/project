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
    re_path(r'^stock/form/$', views.equipment_stock_form,
            name="equipment_stock_form"),
    re_path(r'^stock/form/apply/$', views.equipment_stock_form_apply,
            name="equipment_stock_form_apply"),
    re_path(r'^stock/(?P<stock_id>\d+)/detail/$',
            views.equipment_stock_detail, name="equipment_stock_detail"),
    re_path(r'^stock/(?P<stock_id>\d+)/detail/edit/apply/$',
            views.equipment_stock_detail_apply, name="equipment_stock_detail_apply"),
    re_path(r'^stock/(?P<stock_id>\d+)/delete/$',
            views.equipment_stock_delete, name="equipment_stock_delete"),
    re_path(r'^stock/delivery/apply/$', views.equipment_stock_delivery_apply,
            name="equipment_stock_delivery_apply"),
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
