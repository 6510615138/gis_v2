from django.urls import path
from .views import FactorySearchAPIView, FactoryTypeSearchAPIView

urlpatterns = [
    path('factory/', FactorySearchAPIView.as_view(), name='factory'),
    path('factory-types/', FactoryTypeSearchAPIView.as_view(), name='factory-type'),
]
