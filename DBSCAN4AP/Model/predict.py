# -*- coding: utf-8 -*-
"""
test/predict the anomalies prediction model by command
"""

# Author: Shaohan Huang <buaahsh@gmail.com>
# Date: 2016-8-18
# License: BSD 3 clause

import pickle
import pandas as pd
import argparse

# from Model.Core.LowDimProcessor import LowDimProcessor


def predict(args):
    input_file = args.input
    output_file = args.output
    model_file = args.model

    dataset = pd.read_csv(input_file)

    with open(model_file, 'rb') as handle:
        ldp = pickle.load(handle)
        windows_width = ldp.windows_width

        if args.a:
            labels = ldp.predict_with_analysis(dataset['value'])
            dataset['label'] = 0
            dataset['label'][windows_width - 1:] = labels
        else:
            labels = ldp.predict(dataset['value'])
            dataset['label'] = 0
            dataset['label'][windows_width - 1:] = labels
        dataset.to_csv(output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='',
                        help='data directory containing input.txt')
    parser.add_argument('--output', type=str, default='',
                        help='output file position')
    parser.add_argument('--model', type=str, default='',
                        help='anomaly prediction model')
    parser.add_argument('--a', type=bool, default=True,
                        help='analysis for prediction results')
    args = parser.parse_args()
    predict(args)

if __name__ == '__main__':
    main()

