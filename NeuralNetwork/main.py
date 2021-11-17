import itertools
from data import Data
from non_parametric import non_parametric_models
from linear import linear_models
from SVM import svm
import numpy as np

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
def main():

    data = Data()
    test_all_combination_knn()


    #linear_models(data)
    #svm(data)


if __name__ == "__main__":
    main()
