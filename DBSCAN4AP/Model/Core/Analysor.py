# -*- coding: utf-8 -*-
"""
Analysor can analysis the anomaly degree based on multi method.
"""

# Author: Shaohan Huang <buaahsh@gmail.com>
#
# License: BSD 3 clause


import random


class Analysor():
    def __init__(self, minpts, eps):
        self.min_samples = minpts
        self.eps = eps

    def analysis(self, dists, cache_dists, method='kdis'):
        if method == 'kmean':
            return self.__analysis_based_k_mean(dists, cache_dists)
        if method == 'kdis':
            return self.__analysis_based_k_dis(dists)


    def __analysis_based_k_dis(self, dists):
        dists_sort = sorted(dists)
        k_dis = dists_sort[:self.min_samples]
        ave = sum(k_dis) / len(k_dis)
        return ave / (self.eps * 2)


    def __analysis_based_k_mean(self, dists, cache_dists):
        rank = self.min_samples * 2
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