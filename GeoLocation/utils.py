import json
import glob
import os
from shapely import unary_union
from shapely.geometry import Polygon, MultiPolygon, mapping
from .search import *
from .models import Province, District, Subdistrict

def get_province_polygon(file):
    """
    Load and parse a province-level JSON file to construct a Polygon or MultiPolygon.

    Args:
        file (str): Path to the province JSON file.

    Returns:
        Polygon or MultiPolygon: Geometry representing the province.
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    coordinates = data['coordinates']
    islands = [Polygon([(pt['lat'], pt['lng']) for pt in blob]) for blob in coordinates]

    if len(islands) == 1:
        print(f"Returned {file} as a Polygon")
        return islands[0]
    print(f"Returned {file} as a MultiPolygon")
    return MultiPolygon(islands)

def get_district_polygon(file):
    """
    Load and parse a district/subdistrict-level JSON file to construct a Polygon or MultiPolygon.

    Args:
        file (str): Path to the district/subdistrict JSON file.

    Returns:
        Polygon or MultiPolygon: Geometry representing the district or subdistrict.
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    coordinates = data['coordinates']
    islands = [Polygon([(pt['lat'], pt['lng']) for pt in blob['coor']]) for blob in coordinates]

    if len(islands) == 1:
        print(f"Returned {file} as a Polygon")
        return islands[0]
    print(f"Returned {file} as a MultiPolygon")
    return MultiPolygon(islands)

def get_polygon_coordinates_detailed(regions):
    """
    Load and return a list of GeoJSON-compatible polygon geometries for given region codes.

    Args:
        regions (list[int]): List of region codes (province, district, or subdistrict).

    Returns:
        list[dict]: List of GeoJSON geometries.
    """
    polygons = []

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
            continue

        pattern = os.path.join(root, f"{area.code}*")
        matches = glob.glob(pattern)

        if not matches:
            print(f"No file found for pattern: {pattern}")
            continue

        try:
            filename = matches[0]
            polygon = get_province_polygon(filename) if model is Province else get_district_polygon(filename)
            polygons.append(polygon)
        except Exception as e:
            print(f"Failed to create polygon for {area.code}: {e}")

    print(f"{polygons} type: {type(polygons)}")
    return [mapping(geom) for geom in polygons]

def merge_polygon(poly1, poly2):
    """
    Merge two polygons using unary union.

    Args:
        poly1 (Polygon or MultiPolygon): First geometry.
        poly2 (Polygon or MultiPolygon): Second geometry.

    Returns:
        MultiPolygon or Polygon: Merged geometry.
    """
    return unary_union([poly1, poly2])

def merge_polygon_list(polygons):
    """
    Merge a list of polygons into one geometry using unary union.

    Args:
        polygons (list): List of Polygon or MultiPolygon.

    Returns:
        MultiPolygon or Polygon: Merged geometry.
    """
    return unary_union(polygons)

def get_union_coordinates(regions):
    """
    Merge multiple region polygons into a single GeoJSON geometry.

    Args:
        regions (list[int]): List of region codes.

    Returns:
        str: GeoJSON representation of merged geometry.
    """
    polygons = []

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
            continue

        pattern = os.path.join(root, f"{area.code}*")
        matches = glob.glob(pattern)

        if not matches:
            print(f"No file found for pattern: {pattern}")
            continue

        try:
            filename = matches[0]
            polygon = get_province_polygon(filename) if model is Province else get_district_polygon(filename)
            polygons.append(polygon)
        except Exception as e:
            print(f"Failed to create polygon for {area.code}: {e}")

    merged = merge_polygon_list(polygons)
    return shapely.to_geojson(merged)


