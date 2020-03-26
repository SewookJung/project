from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^check/$', views.login_process, name="login_process"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^', views.login, name="login"),
]
