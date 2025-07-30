# your_app/admin.py
from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'branch_name', 'store_id', 'branch_type', 'format',
        'owner', 'address', 'lat', 'lng', 'province', 'district',
        'subdistrict', 'code'
    )
    search_fields = ('branch_name', 'store_id', 'province', 'district', 'subdistrict', 'owner')
    list_filter = ('province', 'district', 'branch_type', 'format', 'owner')
