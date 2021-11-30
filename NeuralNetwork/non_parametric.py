import numpy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from data import Data, dict_achalandage
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def non_parametric_models(data, transform = 'norm'):
    X, y = data()
    n = range(1, 100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    #normalisation/standardization
    if (transform == 'standardization'):
        pass
    else:
        norm = MinMaxScaler().fit(X_train)
        # transform training data
        X_train= norm.transform(X_train)
        # transform testing dataabs
        X_test = norm.transform(X_test)

    metrics = ["euclidean", "manhattan", "chebyshev", "minkowski"]
    tmp_score = 0
    new_score = 0
    best_k = 0
    best_clf = KNeighborsClassifier(1, metric=metrics[0])

    for i in range(len(metrics)):
        tmp_score = 0
        for j in n:
            clf = KNeighborsClassifier(j, metric=metrics[i])
            clf.fit(X_train, y_train)
            new_score = clf.score(X_test, y_test)
            if new_score > tmp_score:
                tmp_score = new_score
                best_clf = clf
                best_k = j

        print("KNearestNeightbors : K = {0}, Score = {1}, metric = {2}, Comment = {3}"
              .format(best_k, best_clf.score(X_test, y_test), metrics[i], ""))

    """ --- 3d representation of the data ---
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    scatter = ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=data.explicit_y[y])
    
    ax.legend(*scatter.legend_elements(fmt="Classe {x:g}"))
    """

    """ --- multiple plots of 2d classifiers --- 
    fig, sub_figs = plt.subplots(2, 2, tight_layout=True)
    colors = numpy.array([x for x in "bgrcmyk"])
    pairs = [(0, 1), (0, 2), (1, 2)]
    
    for (f1, f2), sub_fig in zip(pairs, sub_figs.reshape(-1)):
        clf = KNeighborsClassifier(43)
        clf.fit(X_train[:, [f1,f2]], y_train)
        x_min, x_max = X[:, f1].min() - 1, X[:, f1].max() + 1
        y_min, y_max = X[:, f2].min() - 1, X[:, f2].max() + 1
    
        xx, yy = numpy.meshgrid(numpy.arange(x_min, x_max, 0.02),
                             numpy.arange(y_min, y_max, 0.02))
    
        Z = clf.predict(numpy.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
    
        sub_fig.contourf(xx, yy, Z, alpha=0.3)
    
        for t in range(len(numpy.unique(y))):
            sub_fig.scatter(X[y == t, f1], X[y == t, f2], color=colors[t].tolist(),
                            label=dict_achalandage[t], s=10)
        sub_fig.set_xlabel(data.feature_names[f1])
        sub_fig.set_ylabel(data.feature_names[f2])
        #sub_fig.legend()


    ---  Possibility to rename the axis for better understanding of numerical values ---
    ax.xaxis.set_ticks(numpy.arange(min(X[:, 0]), max(X[:, 0]) + 1, 1.0))
    labels = [item.get_text() for item in ax.get_xticklabels()]
    
    # Adjusting the margins to fit the text
    plt.gcf().subplots_adjust(left=0.2/plt.gcf().get_size_inches()[0], right=1.- 0.2/plt.gcf().get_size_inches()[0])

    #for i in range(len(numpy.unique(X[:, 0]))):
        #labels[i] = data.explicit_weather[i]
    
    #ax.set_xticklabels(labels)
    
    plt.show()"""
