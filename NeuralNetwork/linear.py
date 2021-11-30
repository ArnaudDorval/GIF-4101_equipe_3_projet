from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.linear_model import Perceptron, SGDClassifier
from sklearn.model_selection import train_test_split

def linear_models(data):
    X, y = data()
    loss = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']
    penalty = range(1, 6)
    max_it = range(1, 6)
    tmp_score = 0
    new_score = 0
    best_penalty = 0
    best_max_iter = 0
    best_clf = SGDClassifier()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    for i in range(len(loss)):
        tmp_score = 0
        for j in penalty:
            for k in max_it:
                clf = SGDClassifier(loss=loss[i])
                clf.fit(X_train, y_train)
                new_score = clf.score(X_test, y_test)
                if new_score > tmp_score:
                    tmp_score = new_score
                    best_clf = clf
                    best_penalty = j
                    best_max_iter = k

        print("Stochastic gradient descent classifier :,Score = {0}, loss function used = {1}, penalty = {2},"
              "max_iter = {3}, Comment = {4}"
              .format( best_clf.score(X_test, y_test), loss[i], best_penalty, best_max_iter, ""))

