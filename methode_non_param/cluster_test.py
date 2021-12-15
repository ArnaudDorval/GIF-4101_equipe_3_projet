import time

from datetime import datetime
import numpy
import warnings
import pandas
from sklearn.preprocessing import minmax_scale

from data import Data

# Nous ne voulons pas avoir ce type d'avertissement, qui
# n'est pas utile dans le cadre de ce devoir
# We do not want to have this type of warning, which
# is not useful in the context of this assignment
warnings.filterwarnings("ignore", category=FutureWarning)

from matplotlib import pyplot

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, v_measure_score
from sklearn.datasets import load_breast_cancer
from sklearn.mixture import GaussianMixture


def evalKmeans(X, y, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)

    clst = kmeans.predict(X)

    pred = numpy.zeros(len(clst))

    for km in set(clst):
        data = []
        for j, b in enumerate(clst):
            if b == km:
                data.append(j)
        label = []
        for i in data:
            label.append(y[i])

        _target = numpy.argmax([label.count(0), label.count(1)])
        pred[data] = _target

    adjusted_score = adjusted_rand_score(y, pred)
    adjusted_info = adjusted_mutual_info_score(y, pred)
    v_measure = v_measure_score(y, pred)
    return adjusted_score, adjusted_info, v_measure


pyplot.figure()

def cluster_kmeans(data, p_list):

    X, y = data()

    X = minmax_scale(X[p_list], feature_range=(0, 1), axis=0, copy=True)


    clst_size = list(range(20, 50, 2))
    score_arr = []
    mutual_arr = []
    measure_arr = []

    for k in clst_size:
        score, mutual, measure = evalKmeans(X, y, k)
        score_arr.append(score)
        mutual_arr.append(mutual)
        measure_arr.append(measure)

    pyplot.xlabel('k')
    pyplot.ylabel('Score')
    pyplot.title(str(p_list))
    pyplot.plot(clst_size, score_arr, label="adjusted rand score")
    pyplot.plot(clst_size, mutual_arr, label="mutual info", alpha=1)
    pyplot.plot(clst_size, measure_arr, label="v measure", alpha=0.5)
    pyplot.legend()

    min_y = min(score_arr)
    if min_y > min(mutual_arr):
        min_y = min(mutual_arr)

    if min_y > min(measure_arr):
        min_y = min(measure_arr)

    max_y = max(score_arr)
    if max_y < max(mutual_arr):
        max_y = max(mutual_arr)

    if max_y < max(measure_arr):
        max_y = max(measure_arr)

    pyplot.ylim([min_y, max_y])

    file_name = "cluster_graph_1/" + str(datetime.now())
    #pyplot.savefig(file_name)
    pyplot.show()