from django.conf.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    re_path(r'^(?P<client_id>\d+)/lists/$',
            views.client_project_lists, name="client_project_lists"),
]