__author__ = 'hsh'
import pandas as pd

from Model import LowDimProcessor


def test(file_name):
    dataset = pd.read_csv(file_name)
    # print dataset['value']
    windows_width = 5
    ldp = LowDimProcessor(windows_width=windows_width)
    # print dataset['is_anomaly'].value_counts()[1]
    labels = ldp.train(dataset['value'], op=True, estimationPer=dataset['is_anomaly'].value_counts()[1])
    labels = ldp.predict(dataset['value'])
    print ldp.evaluate(dataset['is_anomaly'], labels)


    # scaler = StandardScaler().fit(dataset['value'])
    #
    #     # using preprocessing, standardization the X
    # standard_X = scaler.transform(dataset['value'])
    # ldp.parameterOptimization(standard_X, 16)

if __name__ == "__main__":
    file_name = "../Data/real_2.csv"
    test(file_name)