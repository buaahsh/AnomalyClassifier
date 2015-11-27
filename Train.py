from sklearn.cross_validation import KFold
from sklearn.cross_validation import KFold
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from Helper import *
from sklearn.feature_selection import chi2, SelectPercentile, f_classif, SelectKBest

from sklearn.svm import SVC

pipe = Pipeline([
    # ('feat', SelectPercentile(chi2)),
    ('model', SVC(probability=True))
])

grid = {
    # 'tfidf__ngram_range':[(2,6)],
    # 'feat__percentile':[95,90,85],
    # 'model__C':[5]
}


def main():
    # load data
    #train, encoder = loadTrainSet()
    train, target, encoder = loadTrainSet()
    print train.shape[0]
    # cv = KFold(train.shape[0], n_folds=1, shuffle=True)
    # # print list(cv)[0]
    # cv = list(cv)
    # tr = cv[0][0]
    # vl = cv[0][1]
    model = SVC(probability=True).fit(train,target)
    z = {"pred": model.predict_proba(train), "index":0}
    from numpy import zeros
    print target[0].unique().shape[0]
    pred = zeros((train.shape[0], target[0].unique().shape[0]))
    print z['pred'].shape
    print pred[z['index'],:].shape
    pred[z['index'],:] = z['pred']
    score = score_func(target,pred.argmax(1))
    # pred, model = trainSklearn(pipe,grid,train,target,cv,n_jobs=2,multi=True)

if __name__ == "__main__":
    main()
