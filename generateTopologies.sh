# 1 km * 1 km "New York City"
python filter_dataset.py --name new_york_1x1 --lat 40.754380 --lon -73.984986 --width 1 --height 1
python generate_topology.py --path topologies/new_york_1x1.csv --name new_york_1x1_1x1 --width 1 --height 1
python generate_topology.py --path topologies/new_york_1x1.csv --name new_york_1x1_05x05 --width 0.5 --height 0.5
# 2km * 2km "New York City"
python filter_dataset.py --name new_york_2x2 --lat 40.754380 --lon -73.984986 --width 2 --height 2
python generate_topology.py --path topologies/new_york_2x2.csv --name new_york_2x2_2x1 --width 2 --height 1
python generate_topology.py --path topologies/new_york_2x2.csv --name new_york_2x2_1x1 --width 1 --height 1
