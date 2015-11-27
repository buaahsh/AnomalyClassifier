from sklearn.cross_validation import KFold
from sklearn.cross_validation import KFold
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from Helper import *
from sklearn.feature_selection import chi2, SelectPercentile, f_classif, SelectKBest

from sklearn.svm import SVC

pipe = Pipeline([
    # ('feat', SelectPercentile(chi2)),
    ('model', SVC())
])

grid = {
    # 'tfidf__ngram_range':[(2,6)],
    # 'feat__percentile':[95,90,85],
    # 'model__C':[5]
}


def main():
    # load data
    #train, encoder = loadTrainSet()
    train = [[0], [1], [2], [3]]
    target = [0, 1, 2, 3]
    cv = KFold(4, n_folds=2, shuffle=True)
    print list(cv)[0]

    # pred, model = trainSklearn(pipe,grid,train,target,cv,n_jobs=2)

if __name__ == "__main__":
    main()
