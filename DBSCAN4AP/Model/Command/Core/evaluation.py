def pr(y1, y2, windows_width=0, anomaly_label=1):
    """
    # TODO : add roc and others
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