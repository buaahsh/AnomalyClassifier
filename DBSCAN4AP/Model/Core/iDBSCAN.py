# -*- coding: utf-8 -*-
"""
iDBSCAN: improved DBSCAN
DBSCAN: Density-Based Spatial Clustering of Applications with Noise

Add Prediction method, it can use the old model to predict new data and update the model
"""

# Author: Shaohan Huang <buaahsh@gmail.com>
#
# License: BSD 3 clause

import numpy as np
import random

from sklearn.cluster import DBSCAN
from sklearn.utils import check_array
from sklearn.neighbors import DistanceMetric


class iDBSCAN(DBSCAN):
    def __init__(self, eps=0.5, min_samples=5, metric='euclidean',
                 algorithm='auto', leaf_size=30, p=None):
        DBSCAN.__init__(self, eps=eps, min_samples=min_samples, metric=metric,
                 algorithm=algorithm, leaf_size=leaf_size, p=p)
        self.new_components_ = None
        self.cache_components_ = None
        self.x_components_ = 5
        self.num_components_ = 0
        self.num_cache_ = 0

    def fit_predict(self, X, y=None, sample_weight=None):
        labels = DBSCAN.fit_predict(self, X, y, sample_weight)
        if not self.new_components_:
            self.update_components()
        return labels

    def fit(self, X, y=None, sample_weight=None):
        m = DBSCAN.fit(self, X, y, sample_weight)
        if self.new_components_ == None or not self.new_components_.any():
            self.update_components()
        return m

    def update_components(self):
        """
        Init new components and cache components
        new components: Core points
        Cache components: Edge points
        """
        self.new_components_ = np.zeros((self.components_.shape[0] * self.x_components_,
                                         self.components_.shape[1]))
        self.cache_components_ = np.zeros((self.components_.shape[0], self.components_.shape[1]))

        self.new_components_[:self.components_.shape[0]] = self.components_
        self.num_components_ = self.components_.shape[0]

    def detect(self, X):
        """
        it can use the old model to predict new data and update the model
        :param X:
        :return labels
        """
        if not self.new_components_.any():
            self.update_components()
        X = check_array(X, accept_sparse='csr')
        labels = self.radius_neighbors(X)
        return np.array(labels)

    def radius_neighbors(self, X, r=4):
        labels = []
        dist = DistanceMetric.get_metric('euclidean')
        # print self.components_
        dists = dist.pairwise(X, self.new_components_[:self.num_components_])
        # print dists
        for d, x in zip(dists, X):
            f = list(filter(lambda t: t <= self.eps, d))
            num_neighbors = len(f)
            if num_neighbors:
                labels.append(0)
                if self.min_samples <= num_neighbors <= r * self.min_samples and self.num_components_ < self.new_components_.shape[0]:
                    self.new_components_[self.num_components_] = x
                    self.num_components_ += 1
                elif 0 < num_neighbors < self.min_samples:
                    idx = min(self.num_cache_, self.cache_components_.shape[0])
                    num_cache = 0
                    if idx:
                        cache_dists = dist.pairwise([x], self.cache_components_[:])
                        num_cache = len(list(filter(lambda t: t <= self.eps, cache_dists[0])))
                    if self.min_samples <= num_neighbors + num_cache <= r * self.min_samples and self.num_components_ < self.new_components_.shape[0]:
                        self.new_components_[self.num_components_] = x
                        self.num_components_ += 1
                    else:
                        self.cache_components_[self.num_cache_ % self.cache_components_.shape[0]] = x
                        self.num_cache_ += 1
            else:
                labels.append(-1)

        return labels

    def detect_with_analysis(self, X):
        """
        0: normal
        0-1: abnormal
        :param X:
        :return: labels
        """
        if not self.new_components_.any():
            self.update_components()
        X = check_array(X, accept_sparse='csr')
        labels = self.__radius_neighbors_k_means(X)
        return np.array(labels)

    def __radius_neighbors_k_means(self, X, r=4):
        labels = []
        dist = DistanceMetric.get_metric('euclidean')
        # print self.components_
        dists = dist.pairwise(X, self.new_components_[:self.num_components_])
        # print dists
        for d, x in zip(dists, X):
            num_neighbors = len(filter(lambda t: t <= self.eps, d))
            if num_neighbors:
                labels.append(0)
                if self.min_samples <= num_neighbors <= r * self.min_samples and self.num_components_ < self.new_components_.shape[0]:
                    self.new_components_[self.num_components_] = x
                    self.num_components_ += 1
                elif 0 < num_neighbors < self.min_samples:
                    idx = min(self.num_cache_, self.cache_components_.shape[0])
                    num_cache = 0
                    if idx:
                        cache_dists = dist.pairwise([x], self.cache_components_[:])
                        num_cache = len(filter(lambda t: t <= self.eps, cache_dists[0]))
                    if self.min_samples <= num_neighbors + num_cache <= r * self.min_samples and self.num_components_ < self.new_components_.shape[0]:
                        self.new_components_[self.num_components_] = x
                        self.num_components_ += 1
                    else:
                        self.cache_components_[self.num_cache_ % self.cache_components_.shape[0]] = x
                        self.num_cache_ += 1
            else:
                cache_dists = dist.pairwise([x], self.cache_components_[:])[0]
                label = self.__analysis(d, cache_dists)
                labels.append(label)

        return labels

    def __analysis(self, dists, cache_dists):
        """
        Analysis the anomaly using the k-means methods
        :param dists:
        :param cache_dists:
        :return:
        """
        rank = self.min_samples
        dists_sort = sorted(dists)
        cache_dists_sort = sorted(cache_dists)
        i, j = 0, 0
        while i + j < rank:
            if dists_sort[i] < cache_dists_sort[j]:
                i += 1
            else:
                j += 1
        degree = j * 1.0 / rank + random.random() / 10
        if j == 0 or i == 0:
            return degree
        d_edge = sum(cache_dists_sort[:j]) / j
        d_core = sum(dists_sort[:i]) / i
        if d_core < d_edge:
            return degree + (d_core / d_edge)
        return degree


if __name__ == "__main__":
    Y = [[3, 4, 3], [3, 4, 2]]
    ad = iDBSCAN()
    # ad.min_samples = 2
    # ad.eps = 4
    # ad.components_ = np.array(Y)
    # X = [[0, 1, 2], [0, 1, 3], [0, 3, 2]]
    #
    # print ad.predict(X)
    # print ad.new_components_
    # print ad.num_components_