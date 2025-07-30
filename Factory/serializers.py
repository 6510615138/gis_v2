from rest_framework import serializers
from .models import FactoryCoordinates, FactoryType

class FactoryCoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryCoordinates
        fields = ['registration_num', 'name','type', 'lat', 'lng']

class FactoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryType
        fields = ['code', 'type']
