# -*- coding: utf-8 -*-
"""
analysis the tencent and Yahoo dataset and import the result

"""

# Author: Shaohan Huang <buaahsh@gmail.com>
#
# License: BSD 3 clause


import random


def export(file_path):
    output_file = file_path + '.ana'
    with open(output_file, 'w') as f_out:
        l = []
        a_l = []
        with open(file_path, 'r') as f_in:
            for line in f_in:
                l.append(line.strip())
        for i in range(len(l)):
            line = l[i]
            tokens = line.split(',')
            f = float(tokens[2])
            if f > 0:
                a_l.append('\t'.join([l[i-2], l[i-1], l[i]]))
        print(len(a_l))
        for line in a_l:
            rand = random.randint(0, len(a_l) - 1)
            print >>f_out, line
            print >>f_out, a_l[rand]
            print >>f_out, ''



if __name__ == '__main__':
    file_path = '../../../y_out/y/real_67.csv.out.result'
    export(file_path)

