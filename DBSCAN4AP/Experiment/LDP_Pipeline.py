__author__ = 'hsh'
import os

import pandas as pd

from Model.Core.LowDimProcessor import LowDimProcessor


def handle_one_file(file_name, f_out, windows_width):
    dataset = pd.read_csv(file_name)

    # print dataset['value']
    # windows_width = 0
    ldp = LowDimProcessor(windows_width=windows_width)
    anomaly_num = dataset['is_anomaly'].value_counts()[1]
    # print len(dataset['value'][:1000])
    # print len(dataset['value'])
    # labels = ldp.train(dataset['value'][:1200], op=True, estimationPer=anomaly_num)
    labels = ldp.train(dataset['value'][:1000], eps=0.3, min_samples=5)

    # labels = ldp.predict(dataset['value'])
    labels = ldp.predict_with_analysis(dataset['value'])
    # precision, recall = ldp.evaluate(dataset['is_anomaly'], labels)
    # s = "%s\t%f\t%f\t%d" % (file_name, precision, recall, anomaly_num)
    # print >> f_out, s
    root = "/Users/hsh/Downloads/anomaly_data/Yahoo/ydata-labeled-time-series-anomalies-v1_0/y_out/"
    with open(root + file_name.split('/')[-1] + '.out', 'w') as f_out:
        i = 1
        for v, l in zip(dataset['value'][windows_width-1:], labels):
            # print f_out, '{0},{1},{2}'.format(i, v, l)
            i += 1


def pipeline():
    with open("svm-pipeline.txt", 'w') as f_out:
        root = "/Users/hsh/Downloads/anomaly_data/Yahoo/ydata-labeled-time-series-anomalies-v1_0/y"
        for i in os.listdir(root):
            file_name = os.path.join(root,i)
            if file_name.endswith("csv"):
                handle_one_file(file_name, f_out, 2)
                # try:
                #     handle_one_file(file_name, f_out, 0)
                #     # handle_one_file(file_name, f_out, 3)
                #     # handle_one_file(file_name, f_out, 5)
                # except:
                #     print file_name, "Error!!!!!!!"


def para_pipeline():
    root = "/Users/hsh/Downloads/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark/real_2.csv"
    with open("para_pipeline.txt", 'w') as f_out:
        file_name = root
        if file_name.endswith("csv"):
            # handle_one_file(file_name, f_out, 0)
            try:
                for i in range(0, 15):
                    handle_one_file(file_name, f_out, i)
            except:
                print(file_name, "Error!!!!!!!")

if __name__ == "__main__":
    pipeline()
    # para_pipeline()