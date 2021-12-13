import fonctions_reg as fr
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from matplotlib import pyplot
import math
from perceptron import run_perceptron
pd.set_option("display.max_columns", None) # Permet de voir toutes les colonnes du DF
donnees = fr.Data()
donnees.fetch_data(format='by_hour')
x,y = donnees.get_x_y()
print(x)

donnees.fetch_data(format='by_day')
x,y = donnees.get_x_y()
print(x)
#donnees.normalize(X=x,liste_vars=x.columns, plot=False)

#run_perceptron(x,y)

# Analyses preliminaires
#print(x.corr())
#writer = pd.ExcelWriter('correlations.xlsx')
#corr = x.corr(method='spearman')
#corr = pd.DataFrame(corr)
#corr.to_excel(writer)
#writer.save()
# NOTES: Correlation assez elevee entre certaines variables explicatives, probablement mieux d'utiliser regression Ridge
"""
taille = x.shape[1]
nb_cols = round(math.sqrt(taille))
vars_x = x.columns
fig, subfigs = pyplot.subplots(nb_cols, nb_cols, tight_layout=True)

label_y = y.columns[0]
for variable, subfig in zip(vars_x, subfigs.reshape(-1)):
    label_x = variable
    subfig.scatter(x[variable], y, s=1)
    subfig.set_ylabel(label_y)
    subfig.set_xlabel(label_x)

writer = pd.ExcelWriter('reg_alpha_variable.xlsx')
#corr = x.corrwith(y.squeeze(), method='spearman')
#corr = pd.DataFrame(corr)
#corr['SELECT'] = 0
#vars_corr = abs(corr[0]) > 0.1
#corr.loc[vars_corr, 'SELECT'] = 1
#liste_vars_correlees = corr.index[vars_corr]
#corr.to_excel(writer, sheet_name='Correlations', header=['Corr w/ TAUX_OCC', 'SELECT'])
"""
# Perceptron avec variables les plus correlees avec y
#X_percept = x[liste_vars_correlees]
#run_perceptron(x=X_percept, y=y)

#d = fr.meilleur_modele(data=x, target=y, vars_categorielles=donnees.vars_cat, excel_writer=writer, sheet_name='Modeles')

# Perceptron avec les variables composant le meilleur modele lineaire
#meilleures_vars = d[0]
#X_percept = x[meilleures_vars]
#run_perceptron(X_percept, y)

#d = pd.DataFrame(d, index=['model', 'alpha', 'err'], columns=['Sans normalisation'])
#d.to_excel(writer, sheet_name='Meilleur_modele')

#writer.save()
#fig.set_size_inches(25, 10)
#pyplot.savefig(fname='relations.png')
#pyplot.show()
