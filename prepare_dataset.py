import sys

import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare OpenCellID dataset")
    parser.add_argument(
        '--radio',
        help='radio type')
    args = parser.parse_args()
    if args.radio is None:
        print("Please set --radio type!")
        sys.exit()
    col_list = ['radio', 'mcc', 'net', 'area', 'cell',
                    'unit', 'lon', 'lat', 'range', 'samples', 'changeable',
                    'created', 'updated', 'averageSignal']
    print("load cell dataset...")
    df = pd.read_csv('data/cells_data/cell_towers.csv',
                            skipinitialspace=True, usecols=col_list)

    print("prepare filtered dataset...")
    df.drop(['mcc', 'net', 'area', 'unit', 'range', 'samples', 'changeable', 'created', 'updated', 'averageSignal'], axis=1, inplace=True)
    df = df[df["radio"].str.contains(args.radio) == True]
    df.to_csv('data/cells_data/cell_towers_prepared.csv')