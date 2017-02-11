# -*- coding: utf-8 -*-
"""
preprocess the tencent dataset

"""

# Author: Shaohan Huang <buaahsh@gmail.com>
#
# License: BSD 3 clause


def reduce_file(file_path):
    output_file = file_path + '.out'
    with open(output_file, 'w') as f_out:
        l = []
        with open(file_path, 'r') as f_in:
            for line in f_in:
                l.append(float(line))
        for i, num in enumerate(l[2:len(l):2]):
            print >>f_out, '{0},{1}'.format(i, num)


def fix_time_file(file_path):
    output_file = file_path + '.out'
    with open(output_file, 'w') as f_out:
        l = []
        with open(file_path, 'r') as f_in:
            for line in f_in:
                l.append(float(line.split(',')[1]))
        for i, num in enumerate(l):
            print >>f_out, '{0},{1}'.format(i, num)


if __name__ == '__main__':
    file_path = '../../../y_out/t/real_53.csv'
    fix_time_file(file_path)