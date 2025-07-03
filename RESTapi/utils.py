import json
import shapely
from shapely import unary_union
from shapely.geometry import Polygon,MultiPolygon,mapping
from .search import *
from .models import Province, District, Subdistrict 
import glob
import os

def get_province_polygon(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # processing data for the plot
    center_lat = float(data['center']['lat'])
    center_lng = float(data['center']['lng'])

    coordinates = data['coordinates']
    island = [] #A list of tuple
    for blob in coordinates:
        plot_coordinate= []
        for point in blob:
            point_tuple = (point['lat'],point['lng'])
            plot_coordinate.append(point_tuple)
        island.append(Polygon(plot_coordinate))
    if len(island) == 1:
        print(f"returned {file} as a Polygon")
        return Polygon(island[0])#create polygon
    print(f"returned {file} as a MultiPolygon")
    return MultiPolygon(island)#create Multipolygon in case of multiple landmass


def get_district_polygon(file:str):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # processing data for the plot
    center_lat = float(data['coordinates'][0]['center']['lat'])
    center_lng = float(data['coordinates'][0]['center']['lng'])

    coordinates = data['coordinates']
    island = [] #A list of tuple
    for blob in coordinates:
        plot_coordinate = []
        for point in blob["coor"]:
            point_tuple = (point['lat'],point['lng'])
            plot_coordinate.append(point_tuple)
        island.append(Polygon(island))
    if len(island) == 1:
        print(f"returned {file} as a Polygon")
        return Polygon(island[0])#create polygon
    print(f"returned {file} as a MultiPolygon")
    return MultiPolygon(island)#create Multipolygon in case of multiple landmass



def get_polygon_coordinates_detailed(regions):
    list_of_regions_polygons = []    

    for code in regions:
        root = "data/"
        code_str = str(code)

        if len(code_str) == 2:
            root += "province_coordinates/"
            model = Province
        elif len(code_str) == 4:
            root += "district_coordinates/"
            model = District
        elif len(code_str) == 6:
            root += "subdistrict_coordinates/"
            model = Subdistrict
        else:
            print(f"Invalid area code: {code}")
            continue

        try:
            area = model.objects.get(code=code)
        except model.DoesNotExist:
            print(f"{model.__name__} not found for code {code}")

        # Find and parse JSON file
        pattern = os.path.join(root, f"{area.code}*")
        matches = glob.glob(pattern)

        if not matches:
            print(f"No file found for pattern: {pattern}")

        try:
            filename = matches[0]  # use first match
        except  Exception as e:
            print(f"Polygon coordinates not founf for {area.code}: {e}")
        try:
            if model is Province:
                polygon = get_province_polygon(filename)
            else:
                polygon = get_district_polygon(filename)
            list_of_regions_polygons.append(polygon)
        except Exception as e:
            print(f"Failed to create polygon for {area.code}: {e}")

    # Merge and return hGeoJSON
    print(f"{list_of_regions_polygons} tpye : {type(list_of_regions_polygons)}")
    json_serial = [mapping(geom) for geom in list_of_regions_polygons]
    return json_serial





#========== Actively using code above ==========


#========== Below this is not currently called/use but keep for futi=ure use ==========



def merge_polygon(poly1,poly2):
    mergedPolys = unary_union([poly1,poly2])
    return mergedPolys

def merge_polygon_list(pols):
    mergedPolys = unary_union(pols)
    return mergedPolys


#code of regions ex [10,12,14,16]
def get_union_coordinates(regions):
    list_of_regions_polygons = []    

    for code in regions:
        root = "data/"
        code_str = str(code)

        if len(code_str) == 2:
            root += "province_coordinates/"
            model = Province
        elif len(code_str) == 4:
            root += "district_coordinates/"
            model = District
        elif len(code_str) == 6:
            root += "subdistrict_coordinates/"
            model = Subdistrict
        else:
            print(f"Invalid area code: {code}")
            continue

        try:
            area = model.objects.get(code=code)
        except model.DoesNotExist:
            print(f"{model.__name__} not found for code {code}")

        # Find and parse JSON file
        pattern = os.path.join(root, f"{area.code}*")
        matches = glob.glob(pattern)

        if not matches:
            print(f"No file found for pattern: {pattern}")

        try:
            filename = matches[0]  # use first match
        except  Exception as e:
            print(f"Polygon coordinates not founf for {area.code}: {e}")
        try:
            if model is Province:
                polygon = get_province_polygon(filename)
            else:
                polygon = get_district_polygon(filename)
            list_of_regions_polygons.append(polygon)
        except Exception as e:
            print(f"Failed to create polygon for {area.code}: {e}")

    # Merge and return hGeoJSON
    merged = merge_polygon_list(list_of_regions_polygons)
    return shapely.to_geojson(merged)