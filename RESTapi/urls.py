from django.urls import path,re_path
from . import  views

urlpatterns = [
    path('district', views.search_district),
    path("province", views.search_province),
    path("subdistrict", views.search_subdistrict),
    path("coor", views.get_coordinates),
    path("factory", views.get_factory),
    path("factory_type", views.get_factory_type),
]