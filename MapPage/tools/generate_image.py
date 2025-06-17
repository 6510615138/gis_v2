import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import io
from PIL import Image

def generate_mask_from_file(file:str):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)


    center_lat = float(data['center']['lat'])
    center_lng = float(data['center']['lng'])

    coordinates = data['coordinates']

    plot_coordinate = [] #A list of tuple
    for blob in coordinates:
        for point in blob:
            point_tuple = (point['lat'], point['lng'])
            #print(point_tuple)  #debug
            plot_coordinate.append(point_tuple)

    # polygon
    polygon = Polygon(plot_coordinate)
    # plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.grid(False)

    x, y = polygon.exterior.xy
    ax.plot(y, x, color='blue', linewidth=2,)
    ax.fill(y,x)
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

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    plt.axis("equal")

    #create a buffer, savefig to that buffer then read from that buffer and return PIL image
    buf = io.BytesIO()
    ax.savefig(buf,transparent=True)
    buf.seek(0)
    img = Image.open(buf)
    return img
