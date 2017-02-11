# -*- coding: utf-8 -*-
"""
PredictExecutor has two prediction stretaties.

Add Prediction method, it can use the old model to predict new data and update the model
"""

# Author: Shaohan Huang <buaahsh@gmail.com>
#
# License: BSD 3 clause

from sklearn.neighbors import DistanceMetric


class PredictExecutor():
    def __init__(self, n, eps):
        self.n = n
        self.n_edge_num = 0
        self.eps = eps
        self.tempaltes = []

    def reset(self):
        self.n_edge_num = 0

    def predict(self, x, is_edge):
        """
        Predict the x is anomaly based on two stretagies, as n_edge and template
        """
        return self.n_edge(x, is_edge) and self.tempaltes

    def add_template(self, tem):
        self.tempaltes.append(tem)

    def template(self, x):
        if not self.tempaltes:
            return False

        dist = DistanceMetric.get_metric('euclidean')
        # print self.components_
        dists = dist.pairwise([x], self.tempaltes)

        for d in dists:
            num_neighbors = len(list(filter(lambda t: t <= self.eps, d)))
            if num_neighbors == 0:
                return False
            return True


    def n_edge(self, x, is_edge=True):
        """
        N edge stretage is based no n edge points to judge the x is anomaly
        :return:
        """
        if not is_edge:
            self.reset()

        self.n_edge_num += 1
        if self.n_edge_num > self.n:
            return True
        return False

