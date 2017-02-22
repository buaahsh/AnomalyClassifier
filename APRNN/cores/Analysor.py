from sklearn.neighbors.kde import KernelDensity
import pandas as pd
import numpy as np
import json
import random
from cores.ResultItem import Result, Item


class Analysor():
    def __init__(self, bandwidth=1):
        self.bandwidth = bandwidth

    def analysis(self, X, x, kernel='gaussian'):
        # min_x = min(X)
        # X = [i - min_x for i in X]
        bandwidth = sum(X) / len(X)
        if bandwidth <= 0:
            bandwidth = 1
        X = [[i] for i in X]
        kde = KernelDensity(kernel=kernel, bandwidth=bandwidth ).fit(X)
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
                if dataset['Score'][i] == 0:
                    continue
                items = []
                for c in dataset.columns:
                    if c == 'Time' or c == 'Label' or c == 'Score':
                        continue
                    X = dataset[c][i-5: i]
                    x = dataset[c][i]
                    res = self.analysis(X, x)
                    item = Item(c, res, ','.join([str(it) for it in X]), x)
                    items.append(item)

                max_res = max([item.score for item in items ]) + random.random()

                items = sorted(items, key=lambda item:item.score, reverse=True)
                #refine
                final_items = []
                for item in items:
                    item.score /= max_res
                    final_items.append(json.dumps(item.__dict__))
                # refine
                # print('{0}\t{1}'.format(dataset['Time'][i], json.dumps(final_items)), file=f_out)
                label = dataset['Label'][i]
                score = dataset['Score'][i]
                result = Result(label, score, final_items)
                print >>f_out, '{0}\t{1}'.format(dataset['Time'][i], json.dumps(result.__dict__))


if __name__ == '__main__':
    # X = [82, 72, 88, 94, 67]
    # x = [52] #  5.37
    # X = np.array([18, 28, 12, 6, 33])
    # x = [48] #115.028
    # bandwidth = sum(X) / 5
    a = Analysor()


    # print(a.analysis(X, x))
    # x = [34, 4]
    # print(a.analysis(X, x))
    file_path = '../data/rubis/rubis.txt.out.re'
    a.pipeline(file_path)
