import argparse

from utils import load_Cloudlet_Topology

if __name__ == '__main__':
    csvs = ['new_york_1x1_1x1.csv', 'new_york_1x1_05x05.csv',
             'new_york_2x2_1x1.csv','new_york_2x2_2x1.csv']

    for c in csvs:
        df = load_Cloudlet_Topology("output/" + c)
        cloudletDfs = dict(tuple(df.groupby('cloudlet')))
        print(c + ":")
        for i, df in cloudletDfs.items():
            if len(df) > 1:
                print(str(i) + ": " + str(len(df)))