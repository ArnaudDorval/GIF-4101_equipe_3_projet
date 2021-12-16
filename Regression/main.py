import fonctions_reg as fr
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from matplotlib import pyplot
import math
from perceptron import run_perceptron
import pyodbc
import data_merged as dm
import descriptive_stats as ds

donnees = dm.Data(classification='hourly_variation')
pd.set_option("display.max_columns", None) # Permet de voir toutes les colonnes du DF
X, y = donnees.get_x_y()
print(X)

#run_perceptron(x,y)

# Donnees non normalisees
writer = pd.ExcelWriter('reg_ridge_par_heure.xlsx')
d = fr.meilleur_modele(data=X, target=y, normalisees=False, vars_categorielles=['NOM_HOSPITAL', 'WEATHER', 'WEATHER_DESCRIPTION'],
                       excel_writer=writer, sheet_name='Modeles', plot=False)
d = pd.DataFrame(d, index=['model', 'alpha', 'R^2'], columns=['Donnees_non_normalisees'])
d.to_excel(writer, sheet_name='Meilleur_modele')
writer.save()

# Donnees transformees
donnees.boxcox_transformation(X=X, plot=False)
writer = pd.ExcelWriter('reg_lin_par_heure.xlsx')
d = fr.meilleur_modele(data=X, target=y, normalisees=True, vars_categorielles=['NOM_HOSPITAL', 'WEATHER', 'WEATHER_DESCRIPTION'],
                       excel_writer=writer, sheet_name='Modeles', plot=False)
d = pd.DataFrame(d, index=['model', 'alpha', 'R^2'], columns=['Donnees_normalisees'])
d.to_excel(writer, sheet_name='Meilleur_modele')
writer.save()

"""
# Perceptron avec variables les plus correlees avec y
#X_percept = x[liste_vars_correlees]
#run_perceptron(x=X_percept, y=y)

# Perceptron avec les variables composant le meilleur modele lineaire
#meilleures_vars = d[0]
#X_percept = x[meilleures_vars]
#run_perceptron(X_percept, y)
"""
