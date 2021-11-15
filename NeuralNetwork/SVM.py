import numpy
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import cdist
from sklearn.svm import SVC

def svm(data):
    X, y = data()


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)

    d = cdist(X_train, X_train)
    s = numpy.min(d[numpy.nonzero(d)])

    range_sigma = [s, 2*s, 4*s, 8*s, 16*s]
    range_lambda = [10**-3, 10**-2, 10**-1, 10**0, 10**1, 10**2]

    grid_X_train, grid_X_test, grid_y_train, grid_y_test = train_test_split(X_train.copy(), y_train.copy(),
                                                                            test_size=0.5)
    err = 0
    s = l = 0
    for sigma in range_sigma:
        for _lambda in range_lambda:

            clf = SVC(C=_lambda, gamma=1/sigma)
            clf.fit(grid_X_train, grid_y_train)
            temp = clf.score(grid_X_test, grid_y_test)
            if err < temp:
                err = temp
                s = sigma
                l = _lambda

    print(s)
    print(l)
    clf = SVC(C=l, gamma=1/s)
    clf.fit(X_train, y_train)
    print(clf.score(X_test, y_test))