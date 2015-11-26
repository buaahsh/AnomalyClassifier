class FeatureItem(object):

    """docstring for FeatureItem"""

    def __init__(self, line):
        super(FeatureItem, self).__init__()
        self.arg = line


def TrainInstance(model, grid, train, cv, refit=True, n_jobs=5):
    from joblib import Parallel, delayed
    from sklearn.grid_search import ParameterGrid
    from numpy import zeros
    from sklearn.metrics import accuracy_score
    pred = zeros((train.shape[0], train.cuisine.unique().shape[0]))
    best_score = 0
    for g in ParameterGrid(grid):
        model.set_params(**g)
        results = Parallel(n_jobs=n_jobs)(
            delayed(fitIngredients)(train, list(cv), i, model) for i in range(cv.n_folds))
        for i in results:
            pred[i['index'], :] = i['pred']
        score = accuracy_score(train.cuisine, pred.argmax(1))
        if score > best_score:
            best_score = score
            best_pred = pred.copy()
            best_grid = g
    print "Best Score: %0.5f" % best_score
    print "Best Grid", best_grid
    if refit:
        X2 = splitIngredients(train)
        model.set_params(**best_grid)
        model.fit(X2.ingredient, X2.cuisine)
    return best_pred, IngredientModel(model)


def fitSklearn(X, y, cv, i, model, multi=False):
    """
    Train a sklearn pipeline or model -- wrapper to enable parallel CV.
    """
    tr = cv[i][0]
    vl = cv[i][1]
    model.fit(X.iloc[tr], y.iloc[tr])
    if multi:
        return {"pred": model.predict_proba(X.iloc[vl]), "index": vl}
    else:
        return {"pred": model.predict_proba(X.iloc[vl])[:, 1], "index": vl}


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
    """
    Read in JSON to create test set.
    """
    import json
    from pandas import DataFrame
    return DataFrame([ExtractRecipe(x).get_predict() for x in json.load(open(dir, 'rb'))])
