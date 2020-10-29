from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^$', views.document_main, name="document_main"),
    re_path(r'^upload/$', views.document_upload, name="document_upload"),
    re_path(r'^(?P<document_id>\d+)/$', views.document, name="document"),
    re_path(r'^(?P<document_id>\d+)/download/$',
            views.document_download, name="document_download"),

    # API Urls
    re_path(r'^auth/$',
            views.document_default_auth, name="document_default_auth"),
    re_path(r'^upload/apply/$', views.document_upload_apply,
            name="document_upload_apply"),
    re_path(r'^(?P<client_id>\d+)/attach/lists/$',
            views.document_attach_lists, name="document_attach_lists"),
    
    re_path(r'^document/(?P<project_id>\d+)/$',
            views.document_detail, name="document_detail"),
    
    re_path(r'^document/(?P<document_id>\d+)/delete/$',
            views.document_delete, name="document_delete"),
    re_path(r'^document/attach/(?P<attachment_id>\d+)/delete/$',
            views.document_attach_delete, name="document_attach_delete"),
    re_path(r'^document/(?P<document_id>\d+)/detail/$',
            views.document_attach_detail, name="document_attach_detail"),
    re_path(r'^document/attach/(?P<document_id>\d+)/(?P<kind>[A-Z]+)/(?P<middle_class>.+)/detail/$',
            views.document_attach_kind_detail, name="document_attach_kind_detail"),
    re_path(r'^document/attach/(?P<project_id>\d+)/list/$',
            views.document_attach_kind_get_detail, name="document_attach_kind_get_detail"),
    re_path(r'^document/(?P<document_id>\d+)/detail/apply/$',
            views.document_attach_detail_apply, name="document_attach_detail_apply"),
    re_path(r'^document/(?P<document_id>\d+)/auth/$',
            views.document_attach_auth, name="document_attach_auth"),
    
    re_path(r'^document/reg/delete/$',
            views.document_reg_delete, name="document_reg_delete"),
    
    re_path(r'^document/attach/detail/apply/$', views.document_attach_detail_upload_apply,
            name="document_attach_detail_upload_apply"),
    re_path(r'^document/download/check/(?P<pk>\d+)/$',
            views.document_download_check, name="document_download_check"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
