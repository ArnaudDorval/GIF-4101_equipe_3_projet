import itertools
import seaborn as sns
from data import Data
from k_pp import non_parametric_models
from SVM import svm
import numpy as np
from cluster_test import *
from cluster_gaussian_mixture import *

list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY', 'WEATHER']

def test_all_combination_knn(data):
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                non_parametric_models(data, tmp)


def test_all_combination_svm(data):
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                svm(data, tmp)

def test_cluster_kmeans(data):
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                cluster_kmeans(data, tmp)


def test_cluster_gaussian_mixture(data):
    for r in range(len(list_param) + 1):
        combinations_object = itertools.combinations(list_param, r)
        combinations_list = list(combinations_object)
        for comb in combinations_list:
            if len(comb) > 0:
                tmp = np.asarray(comb)
                print(tmp)
                cluster_gaussian_mixture(data, tmp)


#uncomment function to run grid search for all parameters of each model
def main():

    #data = Data(classification="step_variation")
    data = Data(classification="hourly_variation",normalization="min-max")
    x, y = data()

    test_all_combination_svm(data)

    #test_all_combination_knn(data)

    #non_parametric_models(data)

    #test_cluster_kmeans(data)
    #test_cluster_gaussian_mixture(data)


if __name__ == "__main__":
    main()
