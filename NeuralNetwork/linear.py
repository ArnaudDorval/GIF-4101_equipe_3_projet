from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.linear_model import Perceptron, SGDClassifier
from sklearn.model_selection import train_test_split

def linear_models(data):
    X, y = data()
    loss = ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    for i in range(len(loss)):
        clf = SGDClassifier(loss=loss[i])
        clf.fit(X_train, y_train)
        a = clf.score(X_test, y_test)
        print("Stochastic gradient descent classifier :,Score = {0}, loss function used = {1}, Comment = {2}"
              .format( clf.score(X_test, y_test), loss[i],
                      "Data are too clustered due to the features having small range and thus data is not linearly "
                      "independant we need to project to higher dimensions"))

