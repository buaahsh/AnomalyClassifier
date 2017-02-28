__author__ = 'hsh'

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import plot,savefig
import os


def pot_file(file_path):
    x = []
    y = []
    with open(file_path, 'r') as f_in:
        for line in f_in:
            to = line.strip().split(',')
            x.append(float(to[0]))
            y.append(float(to[1]))
            if len(x) > 3000:
                break
    fig = plt.scatter(x,y,s=25,alpha=0.4,marker='o')
    plt.savefig(file_path + '.png')
    plt.close()

    # fig.savefig(file_path + '.png', dpi=100)
    # plt.show()

if __name__ == '__main__':
    path = '/Users/hsh/Documents/2015/AnomalyClassifier/y_out/t'
    listfile = os.listdir(path)
    for item in listfile:
        if item.endswith('.out'):
            print(item)
            pot_file(path + '/' + item)
    # pot_file('/Users/hsh/Documents/2015/AnomalyClassifier/y_out/t/1.txt.out')