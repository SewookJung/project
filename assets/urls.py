from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.assets_main, name="assets_main"),
    path('add/', views.assets_add, name="assets_add"),
    path('add/apply', views.assets_add_apply, name="asset_add_apply"),
    path('status/', views.assets_status, name="assets_status"),
    path('status/apply/', views.assets_rent, name="assets_rent"),
    path('status/return/',
         views.assets_return, name="assets_return"),
]
