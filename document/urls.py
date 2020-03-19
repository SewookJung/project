from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    re_path(r'^$', views.document_main, name="document_main"),
]
