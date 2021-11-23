import fonctions_reg as fr
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale

donnees = fr.Data()
x,y = donnees.get_x_y()

pd.set_option("display.max_columns", None) # Permet de voir toutes les colonnes du DF

# Analyses preliminaires
print(x.corr())
# NOTES: Correlation assez elevee entre certaines variables, probablement mieux d'utiliser regression Ridge

# Sans normalisation
writer= pd.ExcelWriter('save_test.xlsx')
d = fr.meilleur_modele(data=x, target=y, vars_categorielles=donnees.vars_cat)
d = pd.DataFrame(d, index=['model', 'err'], columns=['Sans normalisation'])
d.to_excel(writer, sheet_name='Sans_norm')

# Normalisation de toutes les variables numeriques
x.loc[:, ~x.columns.isin([donnees.vars_cat, 'MOIS', 'HEURE', 'JOUR'])] = minmax_scale(x.loc[:, ~x.columns.isin([donnees.vars_cat, 'MOIS', 'HEURE', 'JOUR'])])
d2 = fr.meilleur_modele(data=x, target=y, vars_categorielles=donnees.vars_cat)
d2 = pd.DataFrame(d2, index=['model', 'err'], columns=['Donnees normalisees'])
d2.to_excel(writer, sheet_name='Normalisees')


writer.save()
