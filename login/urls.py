from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login_main, name="login_main"),
    url(r'^check/$', views.login_process, name="login_process"),
    url(r'^logout/$', views.logout_process, name="logout_process"),
]
