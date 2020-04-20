from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.equipment_main, name="equipment_main"),
    re_path(r'^form/', views.equipment_form, name="equipment_form"),
    re_path(r'^input/', views.equipment_input, name="equipment_input"),
    re_path(r'^bulk/', views.equipment_bulk, name="equipment_bulk"),
    re_path(r'^bulk_check/', views.equipment_bulk_check, name="equipment_bulk_check"),    
    re_path(r'^upload/', views.equipment_upload, name="equipment_upload"),
]
