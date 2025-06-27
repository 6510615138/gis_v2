from .utils import get_union_coordinates 
from .models import Factory  # factory contain lat , lng field represent latitute and longtitute of the factory
# Expects code to be in format list ex [10,12,14,16]
from shapely.geometry import shape, Point, Polygon
import shapely
import json

def find_business_from_code(codes):
    if len(codes) == 0:
        return []

    geojson = get_union_coordinates(codes)  # return GeoJSON geometry string
    json_str:dict = json.loads(geojson)
    polygon = shape(json_str)   # convert GeoJSON to shapely Polygon
    factories = Factory.objects.all() # get all factory
    matched_factories = [] # array to store factory within the polygon

    error = 0
    for factory in factories:
        long = factory.long
        lat = factory.lat
        try:
            if type(lat) == "str" or type(long) == "str" :
                long = float(factory.long)
                lat = float(factory.lat)
            point = Point(long, lat)  # Create a point in shaply shapely uses (x=lng, y=lat)
        except:
            # print(f"error on factory {factory.name} (lat: {lat} long: {long})")
            error += 1
            continue
        if shapely.contains(polygon ,point):# if point in polygon
            matched_factories.append(factory)
            print(f"appended factory {factory.name} (lat: {lat} long: {long})")
    print(f"error : {error}")
    print(f"matched : {len(matched_factories)}")
    return matched_factories
    