from sklearn.neighbors.kde import KernelDensity
import numpy as np


class Analysor():
    def __init__(self):
        pass

    def analysis(self):
        X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        result = kde.score_samples([343124,43])
        print(result)

if __name__ == '__main__':
    a = Analysor()
    a.analysis()