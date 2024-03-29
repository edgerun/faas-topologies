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
    B = math.radians(B)
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

def saveCells(df, name):
    path = 'topologies/' + name
    with open(path + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(df.columns)
        writer.writerows(df.values)


# generate topology utils

def load_Topology(path):
    col_list = ['radio', 'cell', 'lon', 'lat']
    print("load cell dataset...")
    df = pd.read_csv(path,
                     skipinitialspace=True, usecols=col_list)
    return df

def load_Cloudlet_Topology(path):
    col_list = ['radio', 'cell', 'lon', 'lat', 'cloudlet']
    print("load cell dataset...")
    df = pd.read_csv(path,
                     skipinitialspace=True, usecols=col_list)
    return df

def associateWithCloudlets(dataframe, w, h):
    # [max_lat, min_lat, max_lon, min_lon]
    max_bounds = get_max_bounds(dataframe)
    max_lat = max_bounds[0]
    min_lat = max_bounds[1]
    max_lon = max_bounds[2]
    min_lon = max_bounds[3]
    dataframe["cloudlet"] = 0
    new_lon = min_lon
    new_lat = min_lat
    i = 0
    while new_lon <= max_lon:
        old_lon = new_lon
        new_lat = min_lat
        new_lon = addKmToLon(old_lon, new_lat, h + 0.001)
        while new_lat <= max_lat:
            old_lat = new_lat
            new_lat = addKmToLat(new_lat, w + 0.001)
            dataframe.loc[(dataframe['lon'].between(old_lon, new_lon, inclusive="both")) & (dataframe['lat'].between(old_lat, new_lat, inclusive="both")), "cloudlet"] = i
            i = i + 1

    return dataframe

def segmentation_cmap():
    vals = np.linspace(0, 1, 256)
    np.random.shuffle(vals)
    return plt.cm.colors.ListedColormap(plt.cm.CMRmap(vals))
def createColorMapping(df):
    print(df)
    color = {}
    for k, e in enumerate(df):
        if e == 0:
            df[k] = "#000000"
        if e == 1:
            df[k] = "#FF0000"
        if e == 2:
            df[k] = "#0000FF"
        if e == 3:
            df[k] = "#008000"
    return df
def savePlot(df, path, name):
    df = df.loc[df['cloudlet'] == 1, 'cloudlet'] = "#FF0000"
    df = df.loc[df['cloudlet'] == 2, 'cloudlet'] = "#0000FF"
    df = df.loc[df['cloudlet'] == 3, 'cloudlet'] = "#008000"
    plt.scatter(df['lon'], df['lat'], c=createColorMapping(df['cloudlet']),s=2, cmap=segmentation_cmap())
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path + "/" + name + ".pdf")
    df.to_csv(path + "/" + name + ".csv")
    plt.close()