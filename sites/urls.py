from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^$', views.sites_main, name="sites_main"),
    re_path(r'^(?P<pk>\d+)/$', views.sites_detail, name="sites_detail"),
    re_path(r'^(?P<pk>\d+)/delete/$', views.sites_delete, name="sites_delete"),
    re_path(r'^edit/(?P<pk>\d+)/$', views.sites_edit, name="sites_edit"),
    re_path(r'^add/$', views.sites_add, name="sites_add"),
    re_path(r'^add/apply/$', views.sites_add_apply, name="sites_add_apply"),
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
    re_path(r'^document/upload/$',
            views.document_upload, name="document_upload"),
    re_path(r'^document/auth/$',
            views.document_default_auth, name="document_default_auth"),
    re_path(r'^document/reg/$',
            views.document_reg_apply, name="document_reg_apply"),
    re_path(r'^document/upload/apply/$', views.document_upload_apply,
            name="document_upload_apply"),
    re_path(r'^document/attach/detail/apply/$', views.document_attach_detail_upload_apply,
            name="document_attach_detail_upload_apply"),
    re_path(r'^document/download/(?P<pk>\d+)/$',
            views.document_download, name="document_download"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
