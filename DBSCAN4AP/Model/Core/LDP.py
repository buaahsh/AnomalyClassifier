# -*- coding: utf-8 -*-
"""
LowDimProcessor: Process low dimension datasets including: ParameterOptimization, Feature Extractor, Train, Predict ,Evaluation

DBSCAN: Density-Based Spatial Clustering of Applications with Noise

"""

# Author: Shaohan Huang <buaahsh@gmail.com>
# Date: 2016-5-18
# License: BSD 3 clause


from sklearn.grid_search import ParameterGrid
from sklearn.preprocessing import StandardScaler

from .iDBSCAN import iDBSCAN


class LDP(object):

    def __init__(self, windows_width=5):
        self.model = None
        self.scaler = None
        self.windows_width = windows_width

    def parameter_optimization(self, X, estimation_per):
        """
        MinPts must be chosen at least 3. However,
        larger values are usually better for data sets with noise and will yield more significant clusters.
        The larger the data set, the larger the value of minPts should be chosen.

        :param X:
        :param estimation_per:
        :return:
        """

        def score_(estimation_per, X_len, label):
            anomaly_num = label.tolist().count(-1)
            if estimation_per < 1:
                return abs(estimation_per - anomaly_num * 1.0 / X_len)
            else:
                return abs(estimation_per - anomaly_num)

        # tuned_parameters = [{'eps': [0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5], 'min_samples': [3, 4, 5, 6, 7]}]
        tuned_parameters = [{'eps': [0.1, 0.2, 0.3, 0.4, 0.5], 'min_samples': [3, 4, 5, 6, 7]}]
        parameters = ParameterGrid(tuned_parameters)
        best_parameter = None
        best_err_score = None

        for parameter in parameters:
            m = iDBSCAN()
            m.set_params(**parameter)
            m.fit(X)
            labels = m.labels_
            err_score = score_(estimation_per, len(X), labels)
            if not best_parameter:
                best_parameter = parameter
                best_err_score = err_score
            elif best_err_score > err_score:
                best_parameter = parameter
                best_err_score = err_score

        # print best_err_score
        # print best_parameter
        return best_parameter

    def feature_extract(self, X):

        """
        Extract features, based on windows width
        :param X:
        :return:
        """
        if self.windows_width == 0:
            return [[i] for i in X]
        def item_feature(item):
            mean = item.mean()
            amplitude = item.max() - item.min()
            return [item[-1], abs(item[-1] - item[-2])]
            # return [item[-1], mean]
            # return [item[-1], mean, amplitude]
            # return [item[-1], mean, amplitude, amplitude / mean]
        # print type(X[0: 5])
        X = [item_feature(X[i-self.windows_width + 1: i+1]) for i in range(self.windows_width - 1, len(X))]
        return X

    def train(self, X, eps=None, min_samples=None, op=False, estimationPer=None):
        self.scaler = StandardScaler().fit(X)

        # using preprocessing, standardization the X
        standard_X = self.scaler.transform(X)

        if op:
            parameters = self.parameter_optimization(standard_X, estimationPer)
            self.model = iDBSCAN()
            self.model.set_params(**parameters)
        else:
            assert(eps and min_samples)
            self.model = iDBSCAN(eps, min_samples)

        # extract the features from standard X
        standard_X = self.feature_extract(standard_X)

        # Train the ad_dbscan model
        self.model.fit(standard_X)

        labels = self.model.labels_
        return labels

    def predict(self, X, r):
        standard_X = self.scaler.transform(X)
        # extract the features from standard X
        standard_X = self.feature_extract(standard_X)
        labels = self.model.detect(standard_X, r)
        return labels

    def predict_with_analysis(self, X, r):
        standard_X = self.scaler.transform(X)
        # extract the features from standard X
        standard_X = self.feature_extract(standard_X)
        # labels = self.model.detect(standard_X)
        labels = self.model.detect_with_analysis(standard_X, r)
        return labels

    def count_core_points(self, X, r):
        standard_X = self.scaler.transform(X)
        # extract the features from standard X
        standard_X = self.feature_extract(standard_X)
        labels = self.model.count_core_points(standard_X, r)
        return labels

    def evaluate(self, y1, y2, anomaly_label=1):
        """
        # TODO : add roc and others
        Evaluate the accuracy
        :param y1: true label
        :param y2: prediction label
        :param anomaly_label: true label uses 1 as anomaly
        """
        y1 = y1[self.windows_width:]
        tp = 0.0
        fp = 0.0
        fn = 0.0
        for i, j in zip(y1, y2):
            if i == anomaly_label and j == -1:
                tp += 1
            elif i == anomaly_label:
                fn += 1
            elif j == -1:
                fp += 1
        if tp == 0:
            return 0, 0
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        return precision, recall