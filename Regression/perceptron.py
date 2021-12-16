from data import Data
from sklearn import neural_network
from sklearn.model_selection import train_test_split
import pandas as pd
from matplotlib import pyplot
import numpy

def run_perceptron(x,y, plot=False):

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

    excel_writer = pd.ExcelWriter('perceptron.xlsx')

    resultats = numpy.asarray(resultats)
    meill_coeff_idx = numpy.argmax(resultats[:, 3].astype(float))
    meilleurs_res = resultats[meill_coeff_idx, :]

    if plot:
        pmc_regr = neural_network.MLPRegressor(hidden_layer_sizes=resultats[meill_coeff_idx,0].astype(int),
                                               activation=resultats[meill_coeff_idx,1],
                                               momentum=resultats[meill_coeff_idx,2].astype(float), max_iter=1300)
        pmc_regr.fit(x, numpy.ravel(y))
        pred = pmc_regr.predict(x)

        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        ax.scatter(x=y, y=pred, color='indianred')
        ax.plot(numpy.array([0,2]), numpy.array([0,2]), color='black', label="x=y line")
        ax.set_xlabel('Valeurs reelles')
        ax.set_ylabel('Valeurs predites')
        ax.set_xlim([0, y.max()])
        ax.set_ylim([pred.min() - 0.05, pred.max()])
        ax.legend(loc='upper left')
        fig.set_size_inches(25, 10)
        ax.set_title('Meilleur modele, perceptron', fontsize=20)
        pyplot.savefig(fname="predictions_perceptron.png")

    resultats_pd = pd.DataFrame(resultats)
    resultats_pd.to_excel(excel_writer, sheet_name='Results',
                          header=['Hidden_layers_size', 'Activation fct', 'Momentum', 'Coeff de determination'])
    meilleurs_res_pd = pd.DataFrame(meilleurs_res)
    meilleurs_res_pd.to_excel(excel_writer, sheet_name='Best R^2')
    excel_writer.save()
