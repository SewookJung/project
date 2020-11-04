from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^$', views.document_main, name="document_main"),
    re_path(r'^upload/$', views.document_upload, name="document_upload"),
    re_path(r'^form/$', views.document_form, name="document_form"),    

    # API Urls
    re_path(r'^auth/$',
            views.document_default_auth, name="document_default_auth"),
    re_path(r'^upload/apply/$', views.document_upload_apply,
            name="document_upload_apply"),
    
    re_path(r'^(?P<client_id>\d+)/attach/lists/$',
            views.document_attach_lists, name="document_attach_lists"),
    re_path(r'^(?P<document_id>\d+)/$', views.document, name="document"),
    re_path(r'^(?P<document_id>\d+)/download/$',
            views.document_download, name="document_download"),
    re_path(r'^(?P<document_id>\d+)/permission/check/$',
            views.document_permission_check, name="document_permission_check"),

    
    re_path(r'^form/(?P<document_id>\d+)/$',
            views.document_basic_form, name="document_basic_form"),
    re_path(r'^form/upload/apply/$', views.document_form_upload_apply,name="document_form_upload_apply"),
    re_path(r'^form/(?P<document_id>\d+)/download/$',
            views.document_basic_form_download, name="document_basic_form_download"),
    re_path(r'^form/(?P<document_id>\d+)/delete/$',
            views.document_basic_form_delete, name="document_basic_form_delete"),
    
    re_path(r'^(?P<document_id>\d+)/auth/$',
            views.document_attach_auth, name="document_attach_auth"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
