from shapely.geometry import Point
from .models import Store


def findStore(area_code, stores="7-11", coordinates=[13,100], lazy=False, radius=None):
    """
    Find stores near a point using Shapely (approx. radius in degrees).

    Parameters:
        area_code (str): Area or postal code to filter stores.
        stores (list): List of store names to match.
        coordinates (tuple): (lat, lng) in decimal degrees.
        lazy (bool): Return only first match if True.
        radius (float): Radius in KM degrees (~0.001 = ~111m).

    Returns:
        Store or list of Stores.
    """


    lat, lng = coordinates
    target_point = Point(lng, lat)  # Shapely uses (x, y) = (lng, lat)

    queryset = Store.objects.filter(code=area_code)

    found = []

    for store in queryset:
        # store_point = Point(store.longitude, store.latitude)
        # if target_point.distance(store_point) <= radius_deg:
            if lazy:
                found.append({
                "lat": queryset.lat,
                "long": queryset.lng
            })  
            else:
                found.append(found.append({
                "name": queryset.name,
                "lat": queryset.lat,
                "long": queryset.lng
            }))

    return found 