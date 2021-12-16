from data import Data
from sklearn import neural_network
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy

def run_perceptron(x,y):

    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=100)

    n_features = len(x.columns)
    layers_size = range(1, n_features)

    activation = ['identity', 'logistic', 'tanh', 'relu']

    momentum_range = [0.5, 0.6, 0.7, 0.8, 0.9,1]

    resultats = []
    for l_size in layers_size:
        for fct_activ in activation:
            for moment in momentum_range:
                pmc_regr = neural_network.MLPRegressor(hidden_layer_sizes=l_size, activation=fct_activ,
                                                       momentum=moment, max_iter=1300)
                pmc_regr.fit(X_train, numpy.ravel(y_train))
                score = pmc_regr.score(X_test, numpy.ravel(y_test))
                resultats.append([l_size, fct_activ, moment, score])

    excel_writer = pd.ExcelWriter('perceptron_par_h_1300_iter.xlsx')

    resultats = numpy.asarray(resultats)
    meill_coeff_idx = numpy.argmax(resultats[:, 3].astype(float))
    meilleurs_res = resultats[meill_coeff_idx, :]

    resultats_pd = pd.DataFrame(resultats)
    resultats_pd.to_excel(excel_writer, sheet_name='Results',
                          header=['Hidden_layers_size', 'Activation fct', 'Momentum', 'Coeff de determination'])
    meilleurs_res_pd = pd.DataFrame(meilleurs_res)
    meilleurs_res_pd.to_excel(excel_writer, sheet_name='Best R^2')
    excel_writer.save()
