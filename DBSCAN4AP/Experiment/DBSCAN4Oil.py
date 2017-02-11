__author__ = 'hsh'

import numpy as np
import csv
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from datetime import datetime


def read_file(file_path):
    times = []
    values = []
    timesDict = {}
    with open(file_path, 'r') as f_in:
        for line in f_in:
            tokens = line.split(',')
            try:
                float(tokens[0])
                # times.append(tokens[3])
                datetime_object = datetime.strptime(tokens[1].strip(), '%Y/%m/%d %H:%M:%S')
                convert_datetime = datetime(datetime_object.year, datetime_object.month, datetime_object.day,
                                            datetime_object.hour, datetime_object.minute)
                convert_datetime  = convert_datetime.strftime('%Y/%m/%d %H:%M:%S')

                if convert_datetime not in timesDict:
                    timesDict[convert_datetime] = []
                timesDict[convert_datetime].append(float(tokens[0]))
            except(ValueError):
                # print(ValueError)
                continue
               # print("its no a float\n")
            # if tokens[0].isalnum():
    print(len(timesDict))
    for i in timesDict:
        times.append(i)
        values.append([sum(timesDict[i]) / len(timesDict[i])])
    return times, values

def run(file_path):
    times, X = read_file(file_path)
    X_s = StandardScaler().fit_transform(X)
    for i in range(0, len(X_s), 3000):
        print(i)

        j = min(i + 3000, len(X_s))
        new_x = X_s[i:j]

        db = DBSCAN(eps=0.1, min_samples=10).fit(new_x)
        labels = list(db.labels_)
        s = set(labels)
        maxLabel = -1
        maxNum = 0
        for la in s:
            if labels.count(la) > maxNum:
                maxNum = labels.count(la)
                maxLabel = la

        with open(file_path + '.avg.out', 'a') as f_out:
            for l in range(i, j):
                time = times[l]
                x = X[l]
                label = labels[l % 3000]

                dummy_label = 0 if label == maxLabel else -1
                # print >>f_out, '{0},{1},{2},{3}'.format(time, x[0], dummy_label, label)


if __name__ == '__main__':
    file_path = '/Users/hsh/Downloads/shiyou/2015/1.csv'
    run(file_path)
