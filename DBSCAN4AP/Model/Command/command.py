# -*- coding: utf-8 -*-
"""
command.py

"""

# Author: Shaohan Huang <buaahsh@gmail.com>
# Date: 2016-8-18
# License: BSD 3 clause

import argparse

def train(args):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='',
                        help='data directory containing input.txt')
    parser.add_argument('--output', type=str, default='save',
                        help='output file position')
    parser.add_argument('--p', type=float, default=0.2,
                        help='percent for training')
    parser.add_argument('--width', type=int, default=3,
                        help='width of widow sampling')
    parser.add_argument('--ratio', type=int, default=0,
                        help='ratio of anomaly')
    parser.add_argument('--eps', type=int, default=0,
                        help='eps for model')
    parser.add_argument('--minpts', type=int, default=3,
                        help='mipts for model')
    parser.add_argument('--r', type=int, default=3,
                        help='redundancy for pruning')
    parser.add_argument('--a', type=bool, default=True,
                        help='analysis for prediction results')
    args = parser.parse_args()
    train(args)


