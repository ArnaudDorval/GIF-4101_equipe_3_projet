import numpy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from data import Data, dict_achalandage
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def non_parametric_models(data, list, transform = 'norm'):
    X, y = data()
    n = range(50, 1)
    X_train, X_test, y_train, y_test = train_test_split(X[list], y, test_size=0.25)

    metrics = ["chebyshev"]#"euclidean", "manhattan", , "minkowski"
    tmp_score = 0
    new_score = 0
    best_k = 0
    best_clf = KNeighborsClassifier(1, metric=metrics[0])
    best_metric = ""
    score_list = []

    for i in range(len(metrics)):
        for j in n:
            clf = KNeighborsClassifier(j, metric=metrics[i])
            clf.fit(X_train, y_train)
            new_score = clf.score(X_test, y_test)
            score_list.append(new_score)
            if new_score > tmp_score:
                tmp_score = new_score
                best_clf = clf
                best_k = j
                best_metric = i

    print("KNearestNeightbors : K = {0}, Score = {1}, metric = {2}, Comment = {3}"
            .format(best_k, best_clf.score(X_test, y_test), metrics[best_metric], ""))

    t = best_clf.predict(X_test)
    print(t)

    cls, freq = np.unique(t, return_counts=True)
    plt.bar(cls, np.array(freq))
    plt.ylabel('Probability')
    plt.xlabel('Data')
    plt.title("Distribution des résultats de prédiction selon le metric " + str(metrics[best_metric]) + "et k=" + str(best_k))
    plt.show()

    plt.plot(score_list)
    plt.ylabel('Score')
    plt.xlabel('k')
    plt.title("Score en fonction du k-voisin avec \n"
              "['JOUR' 'TEMP' 'WEATHER_DESCRIPTION' 'HUMIDITY']")
    plt.show()


#data = Data(classification="step_variation",normalization="min-max")
#non_parametric_models(data, ['JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY'])