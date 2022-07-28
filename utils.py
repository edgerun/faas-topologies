import csv
import math
import os

import geopy.distance
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

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def saveCells(p, df, name, area):
    path = 'topologies/' + p + '/' + name + "_" + str(round(area, 2)) + 'km2'
    with open(path + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(df.head())
        writer.writerows(df.values)


# generate topology utils

def load_Topology(path):
    col_list = ['radio', 'cell', 'lon', 'lat', 'distances']
    print("load cell dataset...")
    df = pd.read_csv(path,
                     skipinitialspace=True, usecols=col_list)
    return df

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

def savePlot(df, path, name):
    plt.scatter(df['lat'], df['lon'])
    plt.title("Cells in " + name)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    if not os.path.isdir(path):
        os.makedirs(path)
    plt.savefig(path + "/" + name + ".png")
    df.to_csv(path + "/" + name + ".csv")
    plt.close()