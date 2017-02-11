__author__ = 'hsh'

print(__doc__)

import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

from Model.Core import iDBSCAN

##############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)

##############################################################################
# Compute DBSCAN
db = iDBSCAN(eps=0.3, min_samples=5).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

import matplotlib.pyplot as plt

plt.figure(dpi=98)
# p1 = plt.subplot(221)
# p2 = plt.subplot(222)
# p3 = plt.subplot(223)
# p4 = plt.subplot(224)
# p1 = plt.subplot(211)
p2 = plt.subplot(111)

# Black removed and is used for noise instead.
unique_labels = set(labels)

colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    p2.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

    xy = X[class_member_mask & ~core_samples_mask]
    p2.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)
    # p1.title("Raw training dataset")

print db.num_components_

labels = db.detect(X)

unique_labels = set(labels)

colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask]
    p2.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

    # p2.title('Experiment using training data set')

centers = [[1, 1], [-1, -1], [1, -1]]

X, t = make_blobs(n_samples=750, centers=centers, cluster_std=0.3,random_state=1)
#
print db.num_components_


labels = db.detect(X)

unique_labels = set(labels)

# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
colors = ['g', 'k']
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask]
    p2.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

    # p3.title('New random data using old center')

import time

centers = [[0.8, 0.8], [-1.2, -1.2], [1.1, -0.9]]

X, t = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,random_state=0)

start = time.clock()
for _ in xrange(20):
    db.fit(X)
end = time.clock()
print "read: %f s" % (end - start) * 750

start = time.clock()
for _ in xrange(20):
    db.detect(X)
end = time.clock()
print "read: %f s" % (end - start)
