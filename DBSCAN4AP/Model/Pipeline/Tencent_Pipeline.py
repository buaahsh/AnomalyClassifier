__author__ = 'hsh'
import os

import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

from Model.Core.LDP import LDP
import pandas as pd


def get_data(file_name):
    dataset = pd.read_csv(file_name)
    # print dataset['value']
    # windows_width = 5
    # data = []
    return dataset['value']
    # with open(file_name, 'r') as f_in:
    #     for line in f_in:
    #         line = line.strip().strip(',')
    #         v = float(line)
    #         data.append(v)
    # return data

def handle_one_file(file_name, f_out, windows_width):
    dataset = get_data(file_name)

    ldp = LDP(windows_width=windows_width)

    index = min(1000, len(dataset))
    labels = ldp.train(dataset[:index], eps=0.3, min_samples=5)

    # labels = ldp.predict(dataset, 10)
    plot(dataset, labels, file_name)
    # precision, recall = ldp.evaluate(dataset['is_anomaly'], labels)
    # s = "%s\t%f\t%f\t%d" % (file_name, precision, recall, anomaly_num)
    # print >> f_out, s

def plot(dataset, labels, file_name):
    type1_x = []
    type1_y = []
    type2_x = []
    type2_y = []
    for (idx, v), l in zip(enumerate(dataset), labels):
        if l == -1:
            type1_x.append(idx)
            type1_y.append(v)
        else:
            type2_x.append(idx)
            type2_y.append(v)
    plt.figure(figsize=(8, 5), dpi=80)
    axes = plt.subplot(111)
    type1 = axes.scatter(type1_x, type1_y,s=40, c='red' )
    type2 = axes.scatter(type2_x, type2_y, s=40, c='green')
    # plt.show()

    savefig(file_name + '.jpg')

def pipeline():
    with open("tencent-pipeline.txt", 'w') as f_out:
        root = "/Users/hsh/Downloads/anomaly_data/Yahoo/ydata-labeled-time-series-anomalies-v1_0/a1"
        for i in os.listdir(root):
            file_name = os.path.join(root,i)
            if file_name.endswith("csv"):
                handle_one_file(file_name, f_out, 0)

                # try:
                #     print(file_name)
                #     handle_one_file(file_name, f_out, 0)
                #     # handle_one_file(file_name, f_out, 3)
                #     # handle_one_file(file_name, f_out, 5)
                # except:
                #     print file_name, "Error!!!!!!!"


if __name__ == "__main__":
    pipeline()
    # para_pipeline()__author__ = 'hsh'
