import itertools
from data import Data
from non_parametric import non_parametric_models
from linear import linear_models
from SVM import svm
import numpy as np
from estimation_densite import kernel_density_model
import matplotlib.pyplot as plt

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

def test_all_kernel():
    for r in list_param:
        n = [r]
        data2 = Data(p_list=n, type_y="normalised_variation")
        kernel_density_model(data2)

def main():

    data = Data()
    #data = Data(type_y="variation")
    plt.hist(data.y)  # density=False would make counts
    plt.ylabel('Probability')
    plt.xlabel('Data')

    plt.show()

    #decision_random_tree_models(data)
    #test_all_combination_knn()

    #non_parametric_models(data)

    #linear_models(data)
    #svm(data)
    #kernel_density_model(data)
    test_all_kernel()

    #test_all_combination_tree()
    #test_all_combination_random_tree()




if __name__ == "__main__":
    main()
