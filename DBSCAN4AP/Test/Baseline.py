import os

import numpy as np
import pandas as pd
from sklearn import svm


def handle_one_file(file_name, f_out, windows_width):
    from Model.Core import LowDimProcessor

    rng = np.random.RandomState(42)
    dataset = pd.read_csv(file_name)

    # clf = IsolationForest(max_samples=100, random_state=rng)
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    data = [[x] for x,y in zip(dataset['value'], dataset['is_anomaly']) if y != 1]
    clf.fit(data)
    anomaly_num = dataset['is_anomaly'].value_counts()[1]

    labels = clf.predict([[x] for x in dataset['value']])

    ldp = LowDimProcessor(windows_width=windows_width)
    precision, recall = ldp.evaluate(dataset['is_anomaly'], labels)
    s = "%s\t%f\t%f\t%d" % (file_name, precision, recall, anomaly_num)
    print >> f_out, s

def pipeline():
    # with open("iso-pipeline.txt", 'w') as f_out:
    with open("svm-pipeline.txt", 'w') as f_out:
        root = "/Users/hsh/Downloads/anomaly_data/Yahoo/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark"
        for i in os.listdir(root):
            file_name = os.path.join(root,i)
            if file_name.endswith("csv"):
                # handle_one_file(file_name, f_out, 0)
                # handle_one_file(file_name, f_out, 0)
                try:
                    handle_one_file(file_name, f_out, 0)
                    # handle_one_file(file_name, f_out, 3)
                    # handle_one_file(file_name, f_out, 5)
                except:
                    print file_name, "Error!!!!!!!"


if __name__ == '__main__':
    pipeline()