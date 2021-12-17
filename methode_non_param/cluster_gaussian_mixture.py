import time
import numpy
import warnings
import pandas
from sklearn.preprocessing import minmax_scale
from datetime import datetime

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

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, v_measure_score
from sklearn.datasets import load_breast_cancer
from sklearn.mixture import GaussianMixture

def evalEM(X, y, k, init):

    GM = GaussianMixture(n_components=k, init_params=init, max_iter=250)
    GM.fit(X)
    xt = GM.predict_proba(X)

    Gj0_num = numpy.sum((y == 0).reshape(-1, 1) * xt, axis=0)
    Gj0_denom = numpy.sum((y == 0).reshape(-1, 1) * xt)

    Gj1_num = numpy.sum((y == 1).reshape(-1, 1) * xt, axis=0)
    Gj1_denom = numpy.sum((y == 1).reshape(-1, 1) * xt)

    Gj0 = Gj0_num / Gj0_denom
    Gj1 = Gj1_num / Gj1_denom

    total_denom = (numpy.sum(Gj0 * xt, axis=1) + numpy.sum(Gj1 * xt, axis=1))
    xt_0_num = numpy.sum(Gj0 * xt, axis=1)
    xt_1_num = numpy.sum(Gj1 * xt, axis=1)

    xt_0 = xt_0_num / total_denom
    xt_1 = xt_1_num / total_denom

    Ci = numpy.vstack((xt_0, xt_1))

    pred = numpy.argmax(Ci, axis=0)

    adjusted_score = adjusted_rand_score(y, pred)
    adjusted_info = adjusted_mutual_info_score(y, pred)
    v_measure = v_measure_score(y, pred)
    return adjusted_score, adjusted_info, v_measure

pyplot.figure()

def cluster_gaussian_mixture(data, p_list):

    X, y = data()

    X = minmax_scale(X, feature_range=(0, 1), axis=0, copy=True)

    clst_size = list(range(2, 50, 2))
    score_arr = []
    mutual_arr = []
    measure_arr = []

    for k in clst_size:
        score, mutual, measure = evalEM(X, y, k, 'kmeans')
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
    t = datetime.now()
    dt = str(str(t.hour) + '_' + str(t.minute) + '_' + str(t.second))
    file_name = "cluster_graph_2/" + dt + ".png"
    pyplot.savefig(file_name)
    pyplot.show()