import math
import geopy.distance

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
