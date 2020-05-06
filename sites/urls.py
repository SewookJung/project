from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^$', views.sites_main, name="sites_main"),
    re_path(r'^(?P<pk>\d+)/$', views.sites_detail, name="sites_detail"),
    re_path(r'^edit/(?P<pk>\d+)/$', views.sites_edit, name="sites_edit"),
    re_path(r'^add/$', views.sites_add, name="sites_add"),
    re_path(r'^add/apply/$', views.sites_add_apply, name="sites_add_apply"),
    re_path(r'^document/(?P<project_id>\d+)/$',
            views.document_detail, name="document_detail"),
    re_path(r'^document/upload/$',
            views.document_upload, name="document_upload"),
    re_path(r'^document/reg/$',
            views.document_reg_apply, name="document_reg_apply"),
    re_path(r'^document/upload/apply/$', views.document_upload_apply,
            name="document_upload_apply"),
    re_path(r'^document/download/(?P<pk>\d+)/$',
            views.document_download, name="document_download"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
