
from .models import Store
from django.db.models import Q

def get_stores_by_province(province_name):
    return Store.objects.filter(province__iexact=province_name)

def get_stores_by_district(district_name):
    return Store.objects.filter(district__iexact=district_name)

def get_stores_by_code(code):
    return Store.objects.filter(code=code)

def get_stores_by_owner(owner_name):
    return Store.objects.filter(owner__icontains=owner_name)

def get_stores_by_branch_type(branch_type):
    return Store.objects.filter(branch_type__iexact=branch_type)

def get_stores_by_coordinates(lat, lng, radius_km=5):
    """
    Basic radius filter using Pythagorean approximation (not precise for large areas).
    Assumes lat/lng in degrees. 1 degree ≈ 111 km.
    """
    delta = radius_km / 111.0
    return Store.objects.filter(
        lat__gte=lat - delta,
        lat__lte=lat + delta,
        lng__gte=lng - delta,
        lng__lte=lng + delta
    )

def search_stores(keyword):
    """
    Search across multiple fields
    """
    return Store.objects.filter(
        Q(branch_name__icontains=keyword) |
        Q(owner__icontains=keyword) |
        Q(address__icontains=keyword) |
        Q(province__icontains=keyword) |
        Q(district__icontains=keyword)
    )

