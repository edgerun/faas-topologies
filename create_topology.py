import argparse
import time

import math
import numpy as np
import pandas as pd
import sys
import csv
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans

from utils import isfloat, calc_distance, get_max_bounds, get_rectangle_bounds
from geopy.geocoders import Nominatim
from sklearn.neighbors import BallTree

def saveCells(p, df, name, area):
    path = 'topologies/' + p + '/' + name + "_" + str(round(area, 2)) + 'km2'
    with open(path + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(df.head())
        writer.writerows(df.values)

def setDensity(df, density):
    # TODO: remove entries by the entered <density> (uniform distributed by the locations)
    print("set density...")
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create topology from center point")
    parser.add_argument(
        '--n',
        help='name for topology')
    parser.add_argument(
        '--c',
        help='name of city')
    parser.add_argument(
        '--lat',
        help='latitude')
    parser.add_argument(
        '--lon',
        help='longitude')
    parser.add_argument(
        '--w',
        help='width of area (default 2.0 km)')
    parser.add_argument(
        '--h',
        help='height of area (default 2.0 km)')
    parser.add_argument(
        '--d',
        help='density of network nodes: 0.0 - 1.0 (0.0 = only one network node, 1.0 = every cell is a network node [default])')
    args = parser.parse_args()

    start = time.time()
    lat = None
    lon = None
    density = 1.0

    if args.density is not None and isfloat(args.density) and 0.0 >= args.density <= 1.0:
        density = args.density

    if args.name is None:
        print("Please set --name of topology!")
        sys.exit()
    if args.city is not None:
        try:
            geolocator = Nominatim(user_agent="Topology")
            location = geolocator.geocode(args.city)
        except:
            location = None
        if location is None or not hasattr(location, "latitude") or not hasattr(location, "longitude"):
            print("No city found with this name! Please try again or use only --lat and --lon parameters.")
            sys.exit()
        else:
            lat = location.latitude
            lon = location.longitude
    else:
        if args.lon is None or args.lat is None:
            print("no --lat and --lon set, please try again")
            sys.exit()
        else:
            lat = args.lat
            lon = args.lon
    # default value for width and height (2km)
    w = 2.0
    h = 2.0
    if args.width is not None and isfloat(args.width) is True:
        w = float(args.width)
    if args.height is not None and isfloat(args.height) is True:
        h = float(args.height)

    print("Get bounds of area by center point...")
    coords = get_rectangle_bounds([lat, lon], w, h)
    # set bounds
    lon_min = coords[0][1]
    lon_max = coords[1][1]
    lat_min = coords[1][0]
    lat_max = coords[0][0]

    col_list = ['radio', 'cell', 'lon', 'lat']

    print("Loading cell dataset...")
    df_towers = pd.read_csv('data/cells_data/cell_towers_filtered.csv',
                            skipinitialspace=True, usecols=col_list)
    print("Filter cells in area...")
    df_towers = df_towers[df_towers['lon'].between(lon_min, lon_max, inclusive="both")]
    df_towers = df_towers[df_towers['lat'].between(lat_min, lat_max, inclusive="both")]
    df_towers = setDensity(df_towers, density)

    # get max bounds of df --> [max_lat, min_lat, max_lon, min_lon]
    number_cells = len(df_towers)
    if number_cells > 0:
        max_bounds = get_max_bounds(df_towers)
        h_new = calc_distance(max_bounds[2], max_bounds[0], max_bounds[2], max_bounds[1])
        w_new = calc_distance(max_bounds[2], max_bounds[0], max_bounds[3], max_bounds[0])
        # calc average_cells_per_km2 for categorizing topology
        area = w_new * h_new

        tree = BallTree(np.deg2rad(df_towers[['lat', 'lon']].values), metric='haversine')

        query_lats = df_towers['lat']
        query_lons = df_towers['lon']
        print(number_cells)
        k = 3
        if number_cells < 3:
            k = 1
        distances, indices = tree.query(np.deg2rad(np.c_[query_lats, query_lons]), k=k)
        r_km = 6371
        di = []
        for d in distances:
            # remove all zero values
            d = d[d != 0.]
            if len(d) > 0:
                di.append(d.mean() * r_km)
        mean_distance = np.mean(di)

        # if mean distance > 0.5km => sparsely
        if mean_distance > 0.5:
            print("sparsely")
            saveCells("sparsely", df_towers, args.name, area)
        # if mean distance >= 0.1 and <= 0.5km => normal
        elif 0.1 < mean_distance <= 0.5:
            print("normal")
            saveCells("normal", df_towers, args.name, area)
        # if mean distance <= 0.1km => dense
        else:
            print("dense")
            saveCells("dense", df_towers, args.name, area)

    else:
        print("no cells found in this area")