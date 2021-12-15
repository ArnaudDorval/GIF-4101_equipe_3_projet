import itertools

from scipy import stats

import seaborn as sns

from data import Data
from k_pp import non_parametric_models
from linear import linear_models
from SVM import svm
import numpy as np
from estimation_densite import kernel_density_model
import matplotlib.pyplot as plt
from cluster_test import *
from cluster_gaussian_mixture import *

from decision_tree import decision_tree_models
from random_tree import decision_random_tree_models

list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY', 'WEATHER']

def test_all_combination_knn():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                non_parametric_models(data)

def test_all_combination_linear():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                linear_models(data)

def test_all_combination_tree():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                decision_tree_models(data)


def test_all_combination_random_tree():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                decision_random_tree_models(data)


def test_cluster_kmeans():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                cluster_kmeans(data, tmp)


def test_cluster_gaussian_mixture():
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                data = Data(p_list= tmp)
                cluster_gaussian_mixture(data, tmp)

def test_all_kernel():
    for r in list_param:
        n = [r]
        data2 = Data(p_list=n, type_y="normalised_variation")
        kernel_density_model(data2)

def main():

    data = Data(p_list=list_param)
    #data = Data(type_y="variation")
    x, y = data()
    """plt.hist(data.y)  # density=False would make counts
    plt.ylabel('Probability')
    plt.xlabel('Data')

    plt.show()"""

    #y = minmax_scale(y, feature_range=(1, 2), axis=0, copy=True)
    n = y > 0
    w = y[n].reshape(-1,1)
    norm = stats.boxcox(w)

    fig, ax = plt.subplots(1, 2)
    sns.distplot(y, ax=ax[0])
    ax[0].set_title("Original Data")
    sns.distplot(norm, ax=ax[1])
    ax[1].set_title("Normalized data")
    plt.show()

    #decision_random_tree_models(data)
    #test_all_combination_knn()

    #non_parametric_models(data)

    #linear_models(data)
    #svm(data)
    #kernel_density_model(data)
    #test_all_kernel()

    #test_all_combination_tree()
    #test_all_combination_random_tree()

    #test_cluster_kmeans()
    #test_cluster_gaussian_mixture()



if __name__ == "__main__":
    main()
