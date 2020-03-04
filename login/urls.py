from django.conf.urls import url
from . import views


urlpatterns = [
    url('check', views.login_process, name="login_process"),
    url('', views.login, name="login"),
]
