from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/', views.document_add, name="document_add"),
    url(r'^search/', views.document_search, name="document_search"),
    url('', views.document_main, name="document_main"),
]
