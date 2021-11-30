#todo : estimation noyau criss de score negatif batard

from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import train_test_split
import numpy as np

def kernel_density_model(data):
    X, y = data()
    kernel = ['gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine']
    metrics = ["euclidean", "manhattan", "chebyshev", "minkowski"]
    bandwidth = np.linspace(1, 10, 20)
    bandwidth = [0.01, 0.05, 0.1, 0.5, 1, 4]
    tmp_score = 0
    new_score = 0
    best_penalty = 0
    best_max_iter = 0
    best_bandwidth = 0
    best_clf = KernelDensity()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    for i in range(len(kernel)):
        tmp_score = 0
        for k in range(len(bandwidth)):
            clf = KernelDensity(kernel=kernel[i], bandwidth=bandwidth[k])
            clf.fit(X_train, y_train)
            new_score = clf.score(X_test, y_test)
            if  new_score > tmp_score:
                    tmp_score = new_score
                    best_clf = clf
                    best_bandwidth = k

        best_clf.fit(X_test, y_test)
        t = best_clf.score(X_test, y_test)
        print("Kernel density :Score = {0}, kernel = {1},"
              "bandwidth = {2}, Comment = {3}"
              .format(t, kernel[i], best_bandwidth, ""))