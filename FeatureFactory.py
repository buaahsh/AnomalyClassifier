# -*- coding:utf-8 -*-


import argparse


class FlowV5():

    def __init__(self, tokens):
        self.srcAdd = tokens[0]
        self.srcPort = int(tokens[1])
        self.dstAdd = tokens[2]
        self.dstPort = int(tokens[3])
        self.tcpFlag = int(tokens[4])
        self.prot = int(tokens[5])
        self.pkts = int(tokens[6])
        self.octs = int(tokens[7])
        self.isSyn = self.tcpFlag & 2
        self.isIcmp = 0
        if self.prot == 1:
            self.isIcmp = 1


def loadLabelFile(isSourceKey, labelFile):
    _dict = {}
    print "Loading label file..."
    with open(labelFile, 'r') as fIn:
        i = 0
        for line in fIn:
            i += 1
            if i == 1:
                continue
            tokens = line.strip().split(",")
            if len(tokens) != 9:
                continue
            key = tokens[1]
            if not isSourceKey:
                key = tokens[3]
            if not key:
                continue
            tax = tokens[5]
            c = tokens[-1]
            _dict[key] = [tax, c]
    print "# of labeled data is", len(_dict)
    return _dict


def outputFeaure(outputFile, _dict, isSourceKey, mode, labelFile):
    """
    Convert into features, the format of feature is:
    key,isSourceKey,
    nSrcAdds,nSrcPorts,nDstAdds,nDstPorts
    nFlows,nPkts,avgFlowsSize,avgPktSize,nICMP/nFlows,nICMP/nPkts,nSYN/nFlows
    """
    def convert2feaure(flows):

        nSrcAdds = {}
        nSrcPorts = {}
        nDstAdds = {}
        nDstPorts = {}
        nFlows = 0
        nPkts = 0
        avgFlowsSize = 0
        avgPktSize = 0
        nICMPFlow = 0
        nICMPPkt = 0
        nSYN = 0
        for f in flows:
            if f.srcAdd not in nSrcAdds:
                nSrcAdds[f.srcAdd] = 1
            if f.dstAdd not in nDstAdds:
                nDstAdds[f.dstAdd] = 1
            if f.srcAdd + "," + str(f.srcPort) not in nSrcPorts:
                nSrcPorts[f.srcAdd + "," + str(f.srcPort)] = 1
            if f.dstAdd + "," + str(f.dstPort) not in nDstPorts:
                nDstPorts[f.dstAdd + "," + str(f.dstPort)] = 1
            nFlows += 1
            nPkts += f.pkts
            nICMPFlow += f.isIcmp
            nICMPPkt += f.isIcmp * f.pkts
            nSYN += f.isSyn
            avgFlowsSize += (f.octs - avgFlowsSize) * 1.0 / (nFlows + 1)
            avgPktSize += (f.octs - avgPktSize) * 1.0 / (nPkts + 1)

        return [len(nSrcAdds), len(nSrcPorts), len(nDstAdds), len(nDstPorts),
                nFlows, nPkts, avgFlowsSize, avgPktSize,
                nICMPFlow * 1.0 / nFlows,
                nICMPPkt * 1.0 / nPkts,
                nSYN * 1.0 / nFlows]

    if mode == "f":
        print >>outputFile, "key,isSourceKey,nSrcAdds,nSrcPorts,nDstAdds,nDstPortsnFlows,nPkts,avgFlowsSize,avgPktSize,nICMP_nFlows,nICMP_nPkts,nSYN_nFlows"
        for k in _dict:
            flows = _dict[k]
            features = convert2feaure(flows)
            features = [str(f) for f in features]
            print >>outputFile,  "%s,%s" % (k, ",".join(features))
    elif mode == "l":
        labelDict = loadLabelFile(isSourceKey, labelFile)
        inNum = 0
        print >>outputFile, "key,isSourceKey,nSrcAdds,nSrcPorts,nDstAdds,nDstPortsnFlows,nPkts,avgFlowsSize,avgPktSize,nICMP_nFlows,nICMP_nPkts,nSYN_nFlows,label"
        for k in _dict:
            flows = _dict[k]
            features = convert2feaure(flows)
            features = [str(f) for f in features]
            tax = ""
            if k in labelDict:
                tax = labelDict[k][0]
                inNum += 1
            print >>outputFile,  "%s,%s,%s" % (k, ",".join(features), tax)
        print >>outputFile, "#%d,%d" % (len(labelDict), len(labelDict) - inNum)


def buildFearueFile(inputFile, outputFile, isSourceKey, mode, labelFile):
    _dict = {}
    num = 0
    with open(outputFile, 'w') as fOut:
        with open(inputFile, 'r') as fIn:
            for line in fIn:
                num += 1
                if num % 100000 == 0:
                    print num, " lines..."
                tokens = line.strip().split(",")
                if len(tokens) != 8:
                    continue
                flow = FlowV5(tokens)
                if flow.pkts < 10:
                    continue
                key = flow.srcAdd
                if not isSourceKey:
                    key = flow.dstAdd
                if key in _dict:
                    _dict[key].append(flow)
                else:
                    _dict[key] = [flow]
        outputFeaure(fOut, _dict, isSourceKey, mode, labelFile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode",
                        help="mode, f: build features file; l:with label data",
                        default="f")
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-l", "--label", help="labeled file")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-k", "--key", help="aggregation key", default="src")

    args = parser.parse_args()
    print "Args :", args
    mode = args.mode
    inputFile = args.input
    labelFile = args.label
    outputFile = args.output
    isSourceKey = True
    if args.key != "src":
        isSourceKey = False

    buildFearueFile(inputFile, outputFile, isSourceKey, mode, labelFile)
