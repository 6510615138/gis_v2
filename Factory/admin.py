from django.contrib import admin
from .models import FactoryCoordinates, FactoryType

@admin.register(FactoryCoordinates)
class FactoryCoordinatesAdmin(admin.ModelAdmin):
    list_display = (
        'registration_num', 'name', 'type', 'province', 'district',
        'subdistrict', 'status', 'lat', 'lng'
    )
    search_fields = (
        'registration_num', 'name', 'province', 'district',
        'subdistrict', 'owner_name', 'purpose'
    )
    list_filter = ('province', 'status', 'type')
    ordering = ('province', 'district')

@admin.register(FactoryType)
class FactoryTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'num', 'type', 'class1', 'class2', 'class3')
    search_fields = ('code', 'num', 'type', 'class1', 'class2', 'class3')
    list_filter = ('class1', 'class2', 'class3')
    ordering = ('type',)
