from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^rent/status', views.assets_status, name="assets_status"),
    url(r'^rent/', views.assets_rent, name="assets_rent"),
    url(r'^add/', views.assets_add, name="assets_add"),
    url('', views.assets_main, name="assets_main"),
]
