from .utils import get_union_coordinates
from .models import Province,District,Subdistrict
from .models import Factory  # factory contain lat , lng field represent latitute and longtitute of the factory
# Expects code to be in format list ex [10,12,14,16]
from shapely.geometry import shape, Point, Polygon
import shapely
import json
from django.db.models import Q

def find_business_from_code_coor(codes):
    if not codes:
        return []

    geojson = get_union_coordinates(codes)  # return GeoJSON geometry string

    # print(geojson)
    json_dict = json.loads(geojson)
    polygon = shape(json_dict)  # convert GeoJSON to shapely Polygon

    factories = Factory.objects.all()
    matched_factories = []

    error = 0
    for factory in factories:
        long = factory.long
        lat = factory.lat
        try:
            point = Point(lat,long) 
            if polygon.contains(point):
                factory_data = list(Factory.objects.values("registration_num","name", "lat", "long"))
                matched_factories.append(factory_data)
        except Exception as e:
            error += 1
            continue
    print(f"Error count: {error}")
    print(f"Matched factories: {len(matched_factories)}")
    print(matched_factories)
    return matched_factories



def find_business_from_code(codes):
    if not codes:
        return []
    
    area = {
        'province': [],
        'district': [],
        'subdistrict': []
    }

    for code in codes:
        try:
            if code <= 99:
                province = Province.objects.get(code=code)
                area['province'].append(province.name)
            elif code <= 9999:
                district = District.objects.get(code=code)
                area['district'].append(district.name)
            elif code <= 999999:
                subdistrict = Subdistrict.objects.get(code=code)
                area['subdistrict'].append(subdistrict.name)
        except (Province.DoesNotExist, District.DoesNotExist, Subdistrict.DoesNotExist):
            print(f"Code not found: {code}")
            continue



    factories = Factory.objects.filter(
        Q(province__in=area['province']) |
        Q(district__in=area['district']) |
        Q(subdistrict__in=area['subdistrict'])
    ).distinct()

    matched_factories = []

    for factory in factories:
        matched_factories.append({
            "registration_num": factory.registration_num,
            "name": factory.name,
            "lat": factory.lat,
            "long": factory.long
        })
    print(f"Matched factories: {len(matched_factories)}")
    return matched_factories