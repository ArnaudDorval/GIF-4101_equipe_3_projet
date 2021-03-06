import numpy
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import cdist
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, minmax_scale
from sklearn.svm import SVC

def svm(data, list):
    X, y = data()

    kernel = ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']
    X_train, X_test, y_train, y_test = train_test_split(X[list], y, test_size=0.50)


    d = cdist(X_train, X_train)
    s = numpy.min(d[numpy.nonzero(d)])

    range_sigma = [s, 2*s, 4*s, 8*s, 16*s]
    range_lambda = [10**-3, 10**-2, 10**-1, 10**0, 10**1, 10**2]

    err = 0
    s = l = k = 0
    for sigma in range_sigma:
        for _lambda in range_lambda:
            clf = SVC(C=_lambda, gamma=1/sigma, kernel="rbf")
            clf.fit(X_train, y_train)
            temp = clf.score(X_test, y_test)
            if err < temp:
                err = temp
                s = sigma
                l = _lambda


    clf = SVC(C=l, gamma=1 / s, kernel='rbf')
    clf.fit(X_train, y_train)

    print("SVM :Score = {0}, _lambda = {1},"
              "sigma = {2}, kernel = {3} Comment = {4}"
              .format(clf.score(X_test, y_test), l, s, 'rbf', ""))

