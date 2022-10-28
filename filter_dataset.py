import argparse
import time
import numpy as np
import pandas as pd
import sys

from utils import isfloat, calc_distance, get_max_bounds, get_rectangle_bounds, saveCells
from geopy.geocoders import Nominatim
from sklearn.neighbors import BallTree

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create topology from center point")
    parser.add_argument(
        '--name',
        help='name for topology')
    parser.add_argument(
        '--city',
        help='name of city')
    parser.add_argument(
        '--lat',
        help='latitude')
    parser.add_argument(
        '--lon',
        help='longitude')
    parser.add_argument(
        '--width',
        help='width of area (default 2.0 km)')
    parser.add_argument(
        '--height',
        help='height of area (default 2.0 km)')
    args = parser.parse_args()

    start = time.time()
    lat = None
    lon = None

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
    df_towers = pd.read_csv('data/cells_data/cell_towers_prepared.csv',
                            skipinitialspace=True, usecols=col_list)
    print("Filter cells in area...")
    df_towers = df_towers[df_towers['lon'].between(lon_min, lon_max, inclusive="both")]
    df_towers = df_towers[df_towers['lat'].between(lat_min, lat_max, inclusive="both")]

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

        k = 3
        if number_cells < 3:
            k = 1
        # get distances to k nearest neighbours
        distances, indices = tree.query(np.deg2rad(np.c_[query_lats, query_lons]), k=k)

        # sum up top k distances and add to dataframe
        # df_distances = []
        # for d in distances:
        #   df_distances.append(sum(d))
        # df_towers['distances'] = df_distances


        # calculate mean distance top k nearest neighbours per cell
        r_km = 6371
        di = []
        for d in distances:
            # remove all zero values
            d = d[d != 0.]
            if len(d) > 0:
                di.append(d.mean() * r_km)

        # overall mean distance per cell
        mean_distance = np.mean(di)

        # if mean distance > 0.5km => sparsely
        if mean_distance > 0.5:
            print("sparsely dataset created...")
            saveCells(df_towers, args.name)
        # if mean distance >= 0.1 and <= 0.5km => normal
        elif 0.1 < mean_distance <= 0.5:
            print("normal dataset created...")
            saveCells(df_towers, args.name)
        # if mean distance <= 0.1km => dense
        else:
            print("dense dataset created...")
            saveCells(df_towers, args.name)

    else:
        print("no cells found in this area")