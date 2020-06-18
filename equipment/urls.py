from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.equipment_main, name="equipment_main"),
    re_path(r'^form/', views.equipment_form, name="equipment_form"),
    re_path(r'^input/', views.equipment_input, name="equipment_input"),
    re_path(r'^upload/', views.equipment_upload, name="equipment_upload"),
    re_path(r'^upload_check/', views.equipment_upload_check, name="equipment_upload_check"),
    re_path(r'^upload_complete/', views.equipment_upload_complete, name="equipment_upload_complete"),
    re_path(r'^upload_cancel/', views.equipment_upload_cancel, name="equipment_upload_cancel"),
]
