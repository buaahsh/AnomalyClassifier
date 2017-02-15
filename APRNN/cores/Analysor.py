from sklearn.neighbors.kde import KernelDensity
import pandas as pd
import numpy as np
import json
import random
from cores.ResultItem import Result, Item

class Analysor():
    def __init__(self, bandwidth):
        self.bandwidth = bandwidth

    def analysis(self, X, x, kernel='gaussian'):
        # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
        X = [[i] for i in X]
        kde = KernelDensity(kernel=kernel, bandwidth=self.bandwidth ).fit(X)
        result = kde.score([x])
        return -result

    def refine(self, X):
        x = max(X) + random.random()
        X = X / x
        return X

    def pipeline(self, file_path, width=5, threshold=0.5):
        """
        Output file format:
        Time,Info
        :param file_path:
        :return:
        """
        dataset = pd.read_csv(file_path)

        with open(file_path + '.ana', 'w') as f_out:
            print('Time,Info')
            for i in range(width, len(dataset['Time'])):
                if dataset['Label'][i] < threshold:
                    continue
                items = []
                for c in dataset.columns:
                    if c == 'Time' or c == 'Label':
                        continue
                    X = dataset[c][i-5: i]
                    x = dataset[c][i]
                    res = self.analysis(X, x)
                    item = Item(c, res, ','.join([str(it) for it in X]))
                    items.append(json.dumps(item.__dict__))
                # refine
                print('{0},{1}'.format(dataset['Time'][i], json.dumps(items)), file=f_out)


if __name__ == '__main__':
    bandwidth = 1
    a = Analysor(bandwidth)
    # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    # x = [324, 434]
    # print(a.analysis(X, x))
    # x = [34, 4]
    # print(a.analysis(X, x))
    file_path = '../data/rubis/rubis.txt.out'
    a.pipeline(file_path)
