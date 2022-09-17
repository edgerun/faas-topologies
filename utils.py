import csv
import math
import os

import geopy.distance
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# filter dataset utils

def calc_distance(lon1, lat1, lon2, lat2):
    coords_1 = (lon1, lat1)
    coords_2 = (lon2, lat2)
    return geopy.distance.distance(coords_1, coords_2).km

def get_max_bounds(df):
    max_lat = df["lat"].max()
    min_lat = df["lat"].min()
    max_lon = df["lon"].max()
    min_lon = df["lon"].min()
    return [max_lat, min_lat, max_lon, min_lon]

def get_rectangle_bounds(coordinates, width, length):
    start = geopy.Point(latitude=coordinates[0], longitude=coordinates[1])
    hypotenuse = math.hypot(width, length)

    northeast_angle = 0 - math.degrees(math.atan(width / length))
    southwest_angle = 180 - math.degrees(math.atan(width / length))

    d = geopy.distance.distance(kilometers=hypotenuse / 2)
    northeast = d.destination(point=start, bearing=northeast_angle)
    southwest = d.destination(point=start, bearing=southwest_angle)
    bounds = []
    for point in [northeast, southwest]:
        coords = (point.latitude, point.longitude)
        bounds.append(coords)

    return bounds

def radius(B):
    B=math.radians(B)
    a = 6378.137  # Radius at sea level at equator
    b = 6356.752  # Radius at poles
    c = (a**2*math.cos(B))**2
    d = (b**2*math.sin(B))**2
    e = (a*math.cos(B))**2
    f = (b*math.sin(B))**2
    R = math.sqrt((c+d)/(e+f))
    return R

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def addKmToLat(lat, dy):
    new_latitude = lat + (dy / (radius(lat))) * (180 / math.pi)
    return new_latitude

def addKmToLon(lon, lat, dx):
    new_longitude = lon + (dx / radius(lat)) * (180 / math.pi) / math.cos(lat * math.pi / 180)
    return new_longitude

def saveCells(p, df, name, area):
    path = 'topologies/' + p + '/' + name + "_" + str(round(area, 2)) + 'km2'
    with open(path + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(df.head())
        writer.writerows(df.values)


# generate topology utils

def load_Topology(path):
    col_list = ['radio', 'cell', 'lon', 'lat']
    print("load cell dataset...")
    df = pd.read_csv(path,
                     skipinitialspace=True, usecols=col_list)
    return df

def associateWithCloudlets(dataframe, area):
    w = math.sqrt(area)
    # [max_lat, min_lat, max_lon, min_lon]
    max_bounds = get_max_bounds(dataframe)
    max_lat = max_bounds[0]
    min_lat = max_bounds[1]
    max_lon = max_bounds[2]
    min_lon = max_bounds[3]
    dataframe["cloudlet"] = 0
    new_lon = min_lon
    old_lon = new_lon
    new_lat = min_lat
    i = 0
    while new_lon <= max_lon:
        new_lat = min_lat
        old_lon = new_lon
        new_lon = addKmToLon(old_lon, new_lat, w)
        while new_lat <= max_lat:
            old_lat = new_lat
            new_lat = addKmToLat(new_lat, w)
            dataframe.loc[(dataframe['lon'].between(old_lon, new_lon, inclusive="both")) & (dataframe['lat'].between(old_lat, new_lat, inclusive="both")), "cloudlet"] = i
            i = i + 1
    return dataframe


def setDensity(dataframe, density):
    nodes = {}
    for n in dataframe.values:
        nodes[n[1]] = float(n[4])
    sorted_nodes = dict(sorted(nodes.items(), key=lambda x: x[1]))
    i = 1
    num_items = len(sorted_nodes.keys()) * density
    x = math.ceil(len(sorted_nodes.keys()) / num_items)

    # drop rows ordered by "distances" regarding the density (e.g. density=0.2 -> Drop 80% of the cells)
    # sort first to have a uniformed drop distribution
    for k in sorted_nodes.keys():
        if i % x != 0:
            dataframe.drop(dataframe[dataframe['cell'] == k].index, inplace=True)
        i = i + 1
    return dataframe

def segmentation_cmap():
    vals = np.linspace(0, 1, 256)
    np.random.shuffle(vals)
    return plt.cm.colors.ListedColormap(plt.cm.CMRmap(vals))

def savePlot(df, path, name):
    plt.scatter(df['lon'], df['lat'], c=df['cloudlet'],s=2, cmap=segmentation_cmap())
    plt.title("Cells in " + name)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path + "/" + name + ".png")
    df.to_csv(path + "/" + name + ".csv")
    plt.close()