import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn import datasets
from matplotlib import pyplot
from math import sqrt, ceil
from load_dataset import Data



def appliquer_regression(data, target, k, fit_intercept=True, shuffle=True):
    mod = LinearRegression(fit_intercept=fit_intercept)

    # Separation des donnees en k-plis
    kf = KFold(n_splits=k, shuffle=shuffle, random_state=134)
    liste_erreurs = []
    for train_idx, test_idx in kf.split(data):
        X_train, X_test = data[train_idx,:], data[test_idx,:]
        y_train, y_test = target[train_idx], target[test_idx]

        mod.fit(X_train, y_train)
        score = mod.score(X_test, y_test)
        liste_erreurs.append(1 - score)

    return (sum(liste_erreurs)/len(liste_erreurs))

def meilleur_modele(data, target):
    nb_vars = data.shape[1]

    resultats = []
    for idx_1 in range(nb_vars):
        for idx_2 in range(idx_1 + 1, nb_vars + 1):
            jd = data[:,idx_1:idx_2]
            err = appliquer_regression(jd, target, k=3)
            resultats.append([idx_1, idx_2, err])
#    return resultats
    resultats = np.array(resultats)
    meill_err_idx = np.argmax(resultats[:,2])
    return resultats[meill_err_idx,:]


def main():
    x,y = Data().get_x_y()
    appliquer_regression(x.values, y.values, 2)
    #diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)
    #nb_vars = diabetes_X.shape[1]
    #carre = int(sqrt(nb_vars))
    #long = ceil(nb_vars/carre)
    #fig, subfigs = pyplot.subplots(carre, long, tight_layout=True)
    #for i, subfig in zip(range(nb_vars), subfigs.reshape(-1)):
        #scatter = subfig.scatter(diabetes_X[:, i], diabetes_y)

    #pyplot.show()


    #r = meilleur_modele(diabetes_X, diabetes_y)
    #print(r)
    return 0

if __name__ == '__main__':
    main()
