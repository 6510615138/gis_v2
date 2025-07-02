import json
import matplotlib.pyplot as plt
import shapely
from shapely import unary_union
from shapely.geometry import Polygon,MultiPolygon, mapping
import io
from PIL import Image
from .search import *
from .models import Province, District, Subdistrict 
def generate_img(file:str):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # processing data for the plot
    center_lat = float(data['center']['lat'])
    center_lng = float(data['center']['lng'])

    coordinates = data['coordinates']

    plot_coordinate = [] #A list of tuple
    for blob in coordinates:
        for point in blob:
            point_tuple = (point['lat'], point['lng'])
            #print(point_tuple)  #debug
            plot_coordinate.append(point_tuple)


    polygon = Polygon(plot_coordinate)#create polygon
    fig, ax = plt.subplots(figsize=(8, 8))#create the layout polygon
    ax.grid(False) #remove grid

    # plotting
    x, y = polygon.exterior.xy
    ax.plot(y, x, color='blue', linewidth=2,)
    ax.fill(y,x)# fill hollow polygons
    ax.scatter(center_lng,center_lat,  color='red', marker='x',)
    ax.grid(False)

    #remove all labels
    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xlabel("")

    #remove spines 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #remove ticks
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

    # 1:1 ratio
    plt.axis("equal")

    #create a buffer, savefig to that buffer then read from that buffer and return PIL image
    buf = io.BytesIO()
    plt.savefig(buf,transparent=True)
    buf.seek(0)
    img = Image.open(buf)
    return img

def get_province_polygon(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # processing data for the plot
    center_lat = float(data['center']['lat'])
    center_lng = float(data['center']['lng'])

    coordinates = data['coordinates']
    len(coordinates)
    plot_coordinate = [] #A list of tuple
    for blob in coordinates:
        island = []
        for point in blob:
            point_tuple = (point['lat'],point['lng'])
            island.append(point_tuple)
        plot_coordinate.append(Polygon(island))
    return MultiPolygon(plot_coordinate)#create polygon


def get_district_polygon(file:str):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # processing data for the plot
    center_lat = float(data['coordinates'][0]['center']['lat'])
    center_lng = float(data['coordinates'][0]['center']['lng'])

    print(f"lat : {center_lat}  lng : {center_lng}")

    coordinates = data['coordinates'][0]['coor']

    plot_coordinate = [] #A list of tuple
    for blob in coordinates:
        island = []
        for point in blob:
            point_tuple = (point['lat'],point['lng'])
            island.append(point_tuple)
        plot_coordinate.append(Polygon(island))


    polygon = MultiPolygon(plot_coordinate)#create polygon
    return polygon

def merge_polygon(poly1,poly2):
    mergedPolys = unary_union([poly1,poly2])
    return mergedPolys

def merge_polygon_list(pols):
    mergedPolys = unary_union(pols)
    return mergedPolys

import glob
import os

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

def get_polygon_coordinates_corse(regions):
    list_of_polygons = []

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

        filename = matches[0]
        try:
            if model is Province:
                polygon = get_province_polygon(filename)
            else:
                polygon = get_district_polygon(filename)

            if isinstance(polygon, (Polygon, MultiPolygon)):
                list_of_polygons.append(polygon)
        except Exception as e:
            print(f"Failed to create polygon for {area.code}: {e}")
            continue

    # Remove inner polygons
    non_contained = []
    for i, poly in enumerate(list_of_polygons):
        is_inside = False
        for j, other in enumerate(list_of_polygons):
            if i != j and poly.within(other):
                is_inside = True
                break
        if not is_inside:
            non_contained.append(poly)

    if not non_contained:
        return None

    # Merge polygons
    merged = unary_union(non_contained)

    # Convert to GeoJSON
    return shapely.to_geojson(merged)

def combine_polygons(list_of_regions_polygons):
    # Flatten all Polygons and MultiPolygons into one list of Polygons
    all_polygons = []
    for geom in list_of_regions_polygons:
        if isinstance(geom, Polygon):
            all_polygons.append(geom)
        elif isinstance(geom, MultiPolygon):
            all_polygons.extend(list(geom.geoms))

    # Merge them into a single geometry
    merged = unary_union(all_polygons)

    # Convert to GeoJSON
    return merged

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
    merged =  combine_polygons(list_of_regions_polygons)
    return shapely.to_geojson(merged)



