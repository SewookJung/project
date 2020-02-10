from django.conf.urls import url
from . import views


urlpatterns = [
    url('', views.project_main, name="project_main"),
]
