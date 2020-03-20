from django.conf.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$', views.sites_main, name="sites_main"),
    re_path(r'^add/$', views.sites_add, name="sites_add"),
    re_path(r'^add/apply/$', views.sites_add_apply, name="sites_add_apply"),
    re_path(r'^document/upload/$',
            views.document_upload, name="document_upload"),
    re_path(r'^document/upload/apply/$', views.document_upload_apply,
            name="document_upload_apply"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
