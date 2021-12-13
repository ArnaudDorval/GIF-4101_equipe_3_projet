import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn import datasets
from matplotlib import pyplot
from math import sqrt, ceil
import pandas as pd
from data import Data


# Prend en entree un array de variables et un array de reponse, et applique une regression lineaire multiple
# Si necessaire, transforme les variables categorielles en dummies pour qu'elles soient utilisables dans la reg
def appliquer_regression(data, target, k,  alpha, fit_intercept=True, shuffle=True, vars_categorielles=None):
    # Copie de data et target pour pouvoir les manipuler librement
    X, y = data, target
#    mod = LinearRegression(fit_intercept=fit_intercept)
    mod = Ridge(fit_intercept=fit_intercept, alpha=alpha)

    if vars_categorielles is not None:
        X = set_dummies(dataframe=X, variables=vars_categorielles)

    X = X.to_numpy()
    y = y.to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)
    mod.fit(X_train, y_train)
    score = mod.score(X_test, y_test)
    return score


# Prend en entree un jeu de donnees Pandas,
# Retourne une liste contenant les index des variables utilisees par le meilleur modele et l'erreur de ce modele
def meilleur_modele(data, target, vars_categorielles=None, excel_writer=None, sheet_name='Sheet 1', plot=True):
    X,y = data, target
    resultats = []
    nb_vars = data.shape[1]
    nb_obs = data.shape[0]
    # Si on veut creer un jeu de donnees d'entrainement contenant 80% des obs (choix arbitraire), il faut avoir k = 5
    k = 5
    alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    for idx_1 in range(nb_vars):
        for idx_2 in range(idx_1 + 1, nb_vars + 1):
            for a in alphas:
                # Extraction des variables qui seront utilisees dans cette instance de regression
                jd = X.iloc[:, idx_1:idx_2]

                # Extraction des noms des variables utilisees dans cette instance
                noms_variables = X.columns[idx_1:idx_2]

                # Extraction des variables categorielles contenues dans le jd actuel
                vars_categorielles_actuelles = []
                for var in vars_categorielles:
                    if var in jd.columns:
                        vars_categorielles_actuelles.append(var)

                if len(vars_categorielles_actuelles) == 0:
                    vars_categorielles_actuelles = None

                coeff_det = appliquer_regression(data=jd, target=y, k=k, vars_categorielles=vars_categorielles_actuelles, alpha=a)
    #            vars = [i for i in range(idx_1, idx_2+1)]
                resultats.append([noms_variables, a, coeff_det])

    resultats = np.array(resultats)
    resultats_pd = pd.DataFrame(resultats)
    if excel_writer is not None:
        resultats_pd.to_excel(excel_writer, sheet_name=sheet_name, header=['Variables', 'Alpha','Coeff de determination'])
    meill_coeff_idx = np.argmax(resultats[:,2])
    if plot:
        clf = Ridge(alpha=resultats[meill_coeff_idx, 1])
        clf.fit(X[resultats[meill_coeff_idx,0]], y)
        pred = clf.predict(X[resultats[meill_coeff_idx, 0]])
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Meilleur modele, alpha = {:.1f}'.format(resultats[meill_coeff_idx,1]))
        ax.scatter(x=y, y=pred)
        ax.set_xlabel('Valeurs reelles')
        ax.set_ylabel('Valeurs predites')
        pyplot.show()

    return resultats[meill_coeff_idx,:]

def set_dummies(dataframe, variables):
    for var in variables:

        # Permet d'ajouter facilement les colonnes au np.array
        dataframe = pd.get_dummies(dataframe, columns=[var], drop_first=True)
    return dataframe
