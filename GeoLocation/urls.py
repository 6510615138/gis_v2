from django.urls import path
from . import views  

urlpatterns = [

    path('province', views.ProvinceSearchByName.as_view()),
    path("district", views.DistrictSearchByName.as_view()),
    path("subdistrict", views.SubdistrictSearchByName.as_view()),

    path("coor", views.GetCoordinatesAPIView.as_view()),
]