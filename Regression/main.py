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

def run_linear_regression(donnees, X, y, transformed=False, plot=False):
    # Donnees transformees
    if transformed:
        donnees.boxcox_transformation(X=X, plot=plot)
        writer = pd.ExcelWriter('reg_lin_par_heure.xlsx')
        d = fr.meilleur_modele(data=X, target=y, normalisees=True, vars_categorielles=['NOM_HOSPITAL', 'WEATHER', 'WEATHER_DESCRIPTION'],
                               excel_writer=writer, sheet_name='Modeles', plot=plot)
        d = pd.DataFrame(d, index=['model', 'alpha', 'R^2'], columns=['Donnees_normalisees'])
        d.to_excel(writer, sheet_name='Meilleur_modele')
        writer.save()

    # Donnees non normalisees
    else:
        writer = pd.ExcelWriter('reg_ridge_par_heure.xlsx')
        d = fr.meilleur_modele(data=X, target=y, normalisees=False, vars_categorielles=['NOM_HOSPITAL', 'WEATHER', 'WEATHER_DESCRIPTION'],
                               excel_writer=writer, sheet_name='Modeles', plot=plot)
        d = pd.DataFrame(d, index=['model', 'alpha', 'R^2'], columns=['Donnees_non_normalisees'])
        d.to_excel(writer, sheet_name='Meilleur_modele')
        writer.save()


def main():
    donnees = dm.Data(classification='regression', type_y='hourly')
    pd.set_option("display.max_columns", None)  # Permet de voir toutes les colonnes du DF
    X, y = donnees.get_x_y()

#    run_linear_regression(donnees, X, y, transformed=False, plot=True)
#    run_linear_regression(donnees, X, y, transformed=True, plot=True)
    run_perceptron(X, y, plot=True)

if __name__ == "__main__":
    main()
