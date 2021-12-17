import itertools

from sklearn.preprocessing import minmax_scale

from methode_non_param.data import Data
import matplotlib as plt
import numpy as np
from variance_fct import *

list_param = ['HEURE', 'JOUR', 'TEMP', 'WEATHER_DESCRIPTION', 'HUMIDITY', 'WEATHER']

def test_combination_corr():
    combinations_list = list(itertools.combinations(list_param, 2))
    for comb in combinations_list:
        if len(comb) > 0:
            tmp = np.asarray(comb)

            data = Data(p_list= tmp)
            X, y = data()
            X = minmax_scale(X, feature_range=(0, 1), axis=0, copy=True)

            a = [tple[0] for tple in X]
            b = [tple[1] for tple in X]
            cor_func = correlation(a, b)
            cov_func = covariance(a, b)
            print(str(tmp) + ", Corr :" + str(cor_func) + ", Cov :" + str(cov_func))



def main():
    test_combination_corr()


if __name__ == "__main__":
    main()