import argparse
import os.path
import sys

from utils import savePlot, isfloat, load_Topology, associateWithCloudlets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Topology")
    parser.add_argument('--path', help='path to topology csv')
    parser.add_argument('--name', help='naming of the topology output files')
    parser.add_argument(
        '--cloudletarea',
        help='cloudlet area in km2')
    args = parser.parse_args()
    if args.cloudletarea is None:
        print("Please set --cloudletarea!")
        sys.exit()
    if not isfloat(args.cloudletarea):
        print("cloudletarea must be type: float!")
        sys.exit()
    if not 0.1 <= float(args.cloudletarea) <= 1:
        print("cloudlet area must be between 0.1 and 1 km2!")
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
            # savePlot(df, "output/cloudletarea/" + str(args.cloudletarea), args.name)
            df = associateWithCloudlets(df, float(args.cloudletarea))
            savePlot(df, "output/cloudletarea/" + str(args.cloudletarea), args.name)
    else:
        print("File does not exist!")
        sys.exit()
