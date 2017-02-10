import numpy as np


def pr(y1, y2, windows_width=0, anomaly_label=1):
    """
    Evaluate the accuracy
    :param y1: true label
    :param y2: prediction label
    :param anomaly_label: true label uses 1 as anomaly
    """
    y1 = y1[windows_width:]
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


def auc(x, y, reorder=False):
    if x.shape[0] < 2:
        raise ValueError('At least 2 points are needed to compute'
                         ' area under curve, but x.shape = %s' % x.shape)

    direction = 1
    if reorder:
        order = np.lexsort((y, x))
        x, y = x[order], y[order]
    else:
        dx = np.diff(x)
        if np.any(dx < 0):
            if np.all(dx <= 0):
                direction = -1
            else:
                raise ValueError("Reordering is not turned on, and "
                                 "the x array is not increasing: %s" % x)

    area = direction * np.trapz(y, x)
    if isinstance(area, np.memmap):
        area = area.dtype.type(area)
    return area