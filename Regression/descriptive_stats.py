import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from matplotlib import pyplot
import math

# Get the variances of all elements of X and y and store them in the Excel file writer_name
def covariances(X, y, writer_name='covariances.xlsx'):
    writer = pd.ExcelWriter(writer_name)
    var_X = X.var()
    var_y = y.var()
    var_y = pd.Series(var_y)
    variances = pd.concat([var_X, var_y])
    variances.to_excel(writer)
    writer.save()


# If only x is defined, get the correlations between each column of x
# If x and y are defined, get the correlations between y and the individual columns of x
def correlations(x, y=None, writer_name='correlations.xlsx', method='spearman'):
    writer = pd.ExcelWriter(writer_name)
    if y is not None:
        corr = x.corrwith(y.squeeze(), method='spearman')
        corr = pd.DataFrame(corr)
        corr['SELECT'] = 0
        vars_corr = abs(corr[0]) > 0.1
        corr.loc[vars_corr, 'SELECT'] = 1
        corr.to_excel(writer, sheet_name='Correlations', header=['Corr w/ TAUX_OCC', 'SELECT'])
        writer.save()
    else:
        corr = x.corr(method=method)
        corr = pd.DataFrame(corr)
        corr.to_excel(writer, sheet_name='Correlations de X')
        writer.save()


# Get the scatterplot between y and every column of X
def graphs(X, y, graph_name='relations_par_heure.png'):
    taille = X.shape[1]
    nb_cols = round(math.sqrt(taille))
    vars_x = X.columns
    fig, subfigs = pyplot.subplots(nb_cols, nb_cols, tight_layout=True)

    label_y = y.name
    for variable, subfig in zip(vars_x, subfigs.reshape(-1)):
        label_x = variable
        subfig.scatter(X[variable], y, s=1)
        subfig.set_ylabel(label_y)
        subfig.set_xlabel(label_x)

    fig.set_size_inches(25, 10)
    pyplot.savefig(fname=graph_name)
    pyplot.show()
