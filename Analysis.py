# analysis the distribution
# -*- coding:utf-8 -*-

from FeatureFactory import FlowV5
from FeatureFactory import loadLabelFile

def extractOne(lines, isSourceKey, _label):
    _dict = {}
    for line in lines:
        tokens = line.strip().split(",")
        if len(tokens) != 8:
            continue
        flow = FlowV5(tokens)
        key = flow.srcAdd
        if not isSourceKey:
            key = flow.dstAdd
        if _label:
            if key not in _label:
                continue
        if key in _dict:
            _dict[key][0] += 1
            _dict[key][1] += flow.pkts
        else:
            _dict[key] = [1, flow.pkts]
    return _dict


def buildFearueFile(inputFile, outputFile, isSourceKey, labelFile=None):
    _dict = {}
    _label = {}
    if labelFile:
        _label = loadLabelFile()
    num = 0
    n_jobs = 10
    batch_size = 100000
    from joblib import Parallel, delayed
    with open(outputFile, 'w') as fOut:
        with open(inputFile, 'r') as fIn:
            lines = []
            for line in fIn:
                num += 1
                lines.append(line)
                if num % 1000000 == 0:
                    print num, " lines..."
                    results = Parallel(n_jobs=n_jobs)(delayed(extractOne)(
                        lines[i:i+batch_size], isSourceKey, _label) for i in range(0, len(lines), batch_size))
                    lines = []
                    for r in results:
                        for k in r:
                            if k in _dict:
                                _dict[k][0] += r[k][0]
                                _dict[k][1] += r[k][1]
                            else:
                                _dict[k] = [r[k][0], r[k][1]]
                    if num % 2000000 == 0:
                        break
            if lines:
                results += Parallel(n_jobs=n_jobs)(delayed(extractOne)(
                            lines[i:batch_size], isSourceKey, _label) for i in range(0, len(lines), batch_size))
                for r in results:
                        for k in r:
                            if k in _dict:
                                _dict[k][0] += r[k][0]
                                _dict[k][1] += r[k][1]
                            else:
                                _dict[k] = [r[k][0], r[k][1]]
        for k in _dict:
            print >>fOut, "%s,%d,%d" % (k, _dict[k][0], _dict[k][1])


if __name__ == "__main__":
    inputFile = "../ad/data/csv.file"
    outputFile = "../f.file"
    labelFile = "20150104_anomalous_suspicious.csv"
    isSourceKey = True
    buildFearueFile(inputFile, outputFile, isSourceKey, labelFile)
