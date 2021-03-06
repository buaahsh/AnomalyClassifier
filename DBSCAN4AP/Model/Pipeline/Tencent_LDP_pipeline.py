__author__ = 'hsh'
import os

import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pandas as pd


def get_data(file_name, label):
    dataset = pd.read_csv(file_name)
    # print dataset['value']
    # windows_width = 5
    # data = []
    return dataset[label]
    # with open(file_name, 'r') as f_in:
    #     for line in f_in:
    #         line = line.strip().strip(',')
    #         v = float(line)
    #         data.append(v)
    # return data

def handle_one_file(file_name, f_out, windows_width, label):
    dataset = get_data(file_name, label)
    dataset = [[i] for i in dataset]

    X = StandardScaler().fit_transform(dataset)

    db = DBSCAN(eps=0.3, min_samples=100).fit(X)
    labels = db.labels_

    # labels = ldp.predict(dataset, 10)
    plot(dataset, labels, file_name + label)
    save_anomaly(file_name + label, labels)
    # precision, recall = ldp.evaluate(dataset['is_anomaly'], labels)
    # s = "%s\t%f\t%f\t%d" % (file_name, precision, recall, anomaly_num)
    # print >> f_out,

def save_anomaly(file_name, labels):
    with open(file_name + '.label', 'w') as f_out:
        for i, l in enumerate(labels):
            if l  == -1:
                print >>f_out, i + 1

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
    plt.close()

def pipeline():
    root = "/Users/hsh/Documents/2015/AnomalyClassifier/y_out/te"
    file_name = os.path.join(root, 'temp.data')
    a = ['CPU_CAP','CPU_USAGE','MEM_CAP','MEM_USAGE','CPU_AVAI','MEM_AVAI','NET_IN','NET_OUT']
    for i in a:
        handle_one_file(file_name, '', 0, i)
    # with open("tencent-pipeline.txt", 'w') as f_out:
    #     root = "/Users/hsh/Documents/2015/AnomalyClassifier/y_out/te"
    #     for i in os.listdir(root):
    #         file_name = os.path.join(root,i)
    #         if file_name.endswith("csv"):
    #             handle_one_file(file_name, f_out, 0)

                # try:
                #     print(file_name)
                #     handle_one_file(file_name, f_out, 0)
                #     # handle_one_file(file_name, f_out, 3)
                #     # handle_one_file(file_name, f_out, 5)
                # except:
                #     print file_name, "Error!!!!!!!"


if __name__ == "__main__":
    pipeline()
    # para_pipeline()