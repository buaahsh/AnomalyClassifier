# -*- coding: utf-8 -*-
"""
train the anomalies prediction model by command
"""

# Author: Shaohan Huang <buaahsh@gmail.com>
# Date: 2016-8-18
# License: BSD 3 clause

import pickle
import pandas as pd
import argparse

from Model.Core.LowDimProcessor import LowDimProcessor


def train(args):
    input_file = args.input
    output_file = args.output
    dataset = pd.read_csv(input_file)
    windows_width = args.width
    ldp = LowDimProcessor(windows_width=windows_width)
    train_per = args.per
    train_data = dataset['value'][:int(len(dataset['value']) * train_per)]
    if args.ratio > 0:
        ldp.train(train_data, op=False, estimationPer=args.ratio)
    else:
        ldp.train(train_data, min_samples=args.minpts, eps=args.eps)
    with open(output_file, 'wb') as handle:
        pickle.dump(ldp, handle, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='',
                        help='data directory containing input.txt')
    parser.add_argument('--output', type=str, default='',
                        help='output file position')
    parser.add_argument('--per', type=float, default=0.2,
                        help='percent for training')
    parser.add_argument('--width', type=int, default=3,
                        help='width of widow sampling')
    parser.add_argument('--ratio', type=int, default=0,
                        help='ratio of anomaly')
    parser.add_argument('--eps', type=int, default=0.2,
                        help='eps for model')
    parser.add_argument('--minpts', type=int, default=10,
                        help='mipts for model')
    parser.add_argument('--r', type=int, default=3,
                        help='redundancy for pruning')
    parser.add_argument('--a', type=bool, default=True,
                        help='analysis for prediction results')
    args = parser.parse_args()
    train(args)

if __name__ == '__main__':
    main()

