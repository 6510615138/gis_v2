from rest_framework import serializers
from .models import Province, District, Subdistrict

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['code', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['code', 'name', 'province_code']

class SubdistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdistrict
        fields = ['code', 'name', 'district_code', 'is_island']