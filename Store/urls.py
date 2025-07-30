from django.urls import path
from .views import *

urlpatterns = [
    path('store/', StoreAPIView.as_view(), name='factory'),
]
