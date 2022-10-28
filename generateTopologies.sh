# 0.5 km * 0.5 km "New York City"
python filter_dataset.py --name new_york_05x05km --city "New York City" --width 0.5 --height 0.5
python generate_topology.py --path topologies/new_york_05x05km.csv --name new_york_05x05km_05km2 --cloudletarea 0.5
python generate_topology.py --path topologies/new_york_05x05km.csv --name new_york_05x05km_025km2 --cloudletarea 0.25
# 2km * 2km "New York City"
python filter_dataset.py --name new_york_2x2km --city "New York City" --width 2 --height 2
python generate_topology.py --path topologies/new_york_2x2km.csv --name new_york_2x2km_1km2 --cloudletarea 1
python generate_topology.py --path topologies/new_york_2x2km.csv --name new_york_2x2km_05km2 --cloudletarea 0.5
