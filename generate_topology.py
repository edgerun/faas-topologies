import argparse
import os.path
import sys

from utils import savePlot, isfloat, load_Topology, createGraph

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Ether Topology")
    parser.add_argument('--path', help='path to topology csv')
    parser.add_argument('--name', help='naming of the topology output files')
    parser.add_argument(
        '--density',
        help='prune the available nodes by the density (0-1 in percent)',
        default=1)
    args = parser.parse_args()
    if not isfloat(args.density):
        print("density must be type: float!")
        sys.exit()
    if not 0 < float(args.density) <= 1:
        print("density must be between 0 and 1!")
        sys.exit()
    if args.path is None:
        print("Please set --path!")
        sys.exit()
    if args.name is None:
        print("Please set --name!")
        sys.exit()
    if os.path.isfile(args.path):
        if not args.path.endswith('.csv'):
            print("File must has a csv extension!")
        else:
            df = load_Topology(args.path)
            savePlot(df, "output/no_density/" + str(args.density), args.name)
            df = createGraph(df, float(args.density))
            savePlot(df, "output/density/" + str(args.density), args.name)
    else:
        print("File does not exist!")
        sys.exit()
