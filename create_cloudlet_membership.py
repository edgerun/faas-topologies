import argparse
import os.path
import sys

from utils import savePlot, isfloat, load_Topology, associateWithCloudlets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Topology")
    parser.add_argument('--path', help='path to topology csv')
    parser.add_argument('--name', help='naming of the topology output files')
    parser.add_argument('--width', help='cloudlet width in km')
    parser.add_argument('--height', help='cloudlet height in km')
    args = parser.parse_args()
    if args.width is None:
        print("Please set --width!")
        sys.exit()
    if args.height is None:
        print("Please set --height!")
        sys.exit()
    if not isfloat(args.width):
        print("width must be type: float!")
        sys.exit()
    if not isfloat(args.height):
        print("height must be type: float!")
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
            # savePlot(df, "output",  args.name)
            df = associateWithCloudlets(df, float(args.width), float(args.height))
            savePlot(df, "output", args.name)
    else:
        print("File does not exist!")
        sys.exit()
