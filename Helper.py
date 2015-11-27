class FeatureItem(object):

    """docstring for FeatureItem"""

    def __init__(self, line):
        super(FeatureItem, self).__init__()
        self.arg = line


def fitSklearn(X,y,cv,i,model,multi=False):
    """
    Train a sklearn pipeline or model -- wrapper to enable parallel CV.
    """
    tr = cv[i][0]
    vl = cv[i][1]
    # model.fit(X.iloc[tr],y.iloc[tr])
    # if multi:
    #     return  {"pred": model.predict_proba(X.iloc[vl]), "index":vl}
    # else:
    #     return  {"pred": model.predict_proba(X.iloc[vl])[:,1], "index":vl}
    model.fit(X[tr], y[tr])
    if multi:
        return  {"pred": model.predict_proba(X[vl]), "index":vl}
    else:
        return  {"pred": model.predict_proba(X)[vl][:,1], "index":vl}

def trainSklearn(model,grid,train,target,cv,refit=True,n_jobs=5,multi=False):
    """
    Train a sklearn pipeline or model using textual data as input.
    """
    from joblib import Parallel, delayed   
    from sklearn.grid_search import ParameterGrid
    from numpy import zeros
    if multi:
        pred = zeros((train.shape[0],target.unique().shape[0]))
        from sklearn.metrics import accuracy_score
        score_func = accuracy_score
    else:
        from sklearn.metrics import roc_auc_score
        score_func = roc_auc_score
        # pred = zeros(train.shape[0])
        pred = zeros(4)
    best_score = 0
    for g in ParameterGrid(grid):
        model.set_params(**g)
        if len([True for x in g.keys() if x.find('nthread') != -1 ]) > 0:
            results = [fitSklearn(train,target,list(cv),i,model,multi) for i in range(cv.n_folds)]
        else:
            results = Parallel(n_jobs=n_jobs)(delayed(fitSklearn)(train,target,list(cv),i,model,multi) for i in range(cv.n_folds))
        if multi:
            for i in results:
                pred[i['index'],:] = i['pred']
            score = score_func(target,pred.argmax(1))
        else:
            for i in results:
                pred[i['index']] = i['pred']
            score = score_func(target,pred)
        if score > best_score:
            best_score = score
            best_pred = pred.copy()
            best_grid = g
    print "Best Score: %0.5f" % best_score 
    print "Best Grid", best_grid
    if refit:
        model.set_params(**best_grid)
        model.fit(train,target)
    return best_pred, model


def loadTrainSet(dir='../data/train.json'):
    """
    Read in JSON to create training set.
    """
    import json
    from pandas import DataFrame, Series
    from sklearn.preprocessing import LabelEncoder
    X = DataFrame([ExtractRecipe(x).get_train()
                   for x in json.load(open(dir, 'rb'))])
    encoder = LabelEncoder()
    X['cuisine'] = encoder.fit_transform(X['cuisine'])
    return X, encoder


def loadTestSet(dir='../data/test.json'):
    pass
