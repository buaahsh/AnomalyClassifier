from sklearn.neighbors.kde import KernelDensity
import numpy as np
import random


class Analysor():
    def __init__(self, bandwidth):
        self.bandwidth = bandwidth

    def analysis(self, X, x, kernel='gaussian'):
        # X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
        kde = KernelDensity(kernel=kernel, bandwidth=self.bandwidth ).fit(X)
        result = kde.score([x])
        return -result

    def refine(self, X):
        x = max(X) + random.random()
        X = X / x
        return X

if __name__ == '__main__':
    bandwidth = 1
    a = Analysor(bandwidth)
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    x = [324, 434]
    print(a.analysis(X, x))
    x = [34, 4]
    print(a.analysis(X, x))