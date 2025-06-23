import json
import matplotlib.pyplot as plt
import shapely
from shapely import unary_union
from shapely.geometry import Polygon
import io
from PIL import Image
from .search import *
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

def create_polygon_from_JSON(file:str):

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
    return polygon

def merge_polygon(poly1,poly2):
    mergedPolys = unary_union([poly1,poly2])
    print(mergedPolys)
    return mergedPolys

def merge_polygon_list(pols):
    mergedPolys = unary_union(pols)
    print(mergedPolys)
    return mergedPolys

# shapely.to_geojson(merge_polygon_list([p1,p2]))
import glob
import os
#code of regions ex [10,12,14,16]
def get_union_coordinates(regions):
    list_of_regions_polygons = []    
    for code in regions:
        root = "data/"

        if len(str(code)) == 2:
            root += "province_coordinates/"
        elif len(str(code)) == 4:
            root += "district_coordinates/"
        elif len(str(code)) == 6:
            root += "subdistrict_coordinates/"
        else:
            print(f"wrong province code! {code}")
            continue
        
        try:
            province = Province.objects.get(code=code)
        except:
            raise ValueError(f"province not found {code}")

        pattern = os.path.join(root, f"{province.code}*")
        matches = glob.glob(pattern)

        if not matches:
            raise FileNotFoundError(f"No file found for pattern: {pattern}")
        
        filename = matches[0]  # take the first match
        polygon = create_polygon_from_JSON(filename)
        list_of_regions_polygons.append(polygon)

    merged = merge_polygon_list(list_of_regions_polygons)
    return shapely.to_geojson(merged)