import fonctions_reg as fr
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from matplotlib import pyplot
import math

donnees = fr.Data()
x,y = donnees.get_x_y()

pd.set_option("display.max_columns", None) # Permet de voir toutes les colonnes du DF

# Analyses preliminaires
#print(x.corr())
# NOTES: Correlation assez elevee entre certaines variables explicatives, probablement mieux d'utiliser regression Ridge
taille = x.shape[1]
nb_cols = round(math.sqrt(taille))
vars_x = x.columns
fig, subfigs = pyplot.subplots(nb_cols, nb_cols, tight_layout=True)

label_y = y.columns[0]
for variable, subfig in zip(vars_x, subfigs.reshape(-1)):
    print(variable)
    label_x = variable
    subfig.scatter(x[variable], y)
    subfig.set_ylabel(label_y)
    subfig.set_xlabel(label_x)

writer = pd.ExcelWriter('save_test.xlsx')
corr = x.corrwith(y.squeeze())
corr = pd.DataFrame(corr)
corr['SELECT'] = 0
vars_corr = abs(corr[0]) > 0.1
corr.loc[vars_corr, 'SELECT'] = 1
liste_vars_correlees = corr.index[vars_corr]

corr.to_excel(writer, sheet_name='Correlations', header=['Corr w/ TAUX_OCC', 'SELECT'])

# Sans normalisation
d = fr.meilleur_modele(data=x[liste_vars_correlees], target=y, vars_categorielles=donnees.vars_cat, excel_writer=writer, sheet_name='Resultats non-norm')
d = pd.DataFrame(d, index=['model', 'err'], columns=['Sans normalisation'])
d.to_excel(writer, sheet_name='Sans_norm')

# Normalisation de toutes les variables numeriques
x.loc[:, ~x.columns.isin([donnees.vars_cat, 'MOIS', 'HEURE', 'JOUR'])] = minmax_scale(x.loc[:, ~x.columns.isin([donnees.vars_cat, 'MOIS', 'HEURE', 'JOUR'])])
d2 = fr.meilleur_modele(data=x[liste_vars_correlees], target=y, vars_categorielles=donnees.vars_cat, excel_writer=writer, sheet_name = 'Resultats norm')
d2 = pd.DataFrame(d2, index=['model', 'err'], columns=['Donnees normalisees'])
d2.to_excel(writer, sheet_name='Normalisees')

writer.save()
fig.set_size_inches(12, 7)
pyplot.savefig(fname='relations.png')
pyplot.show()