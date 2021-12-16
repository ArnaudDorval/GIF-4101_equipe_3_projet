# Ce fichier permet de recuperer les donnees de la base de donnees et de les formatter

import pyodbc # pip install pyodbc
import pandas as pd
import pyodbc
import numpy as np
import datetime
import math
from scipy import stats
from matplotlib import pyplot

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

dict_achalandage = np.array(['Pas achalande', 'Peu achalende', 'achalande', 'tres achalande', 'tres tres achalande',
                                'extremement achalande', 'absurdement achalande'])

liste_hopital = ["Le Centre hospitalier de l'Universit Laval", "Hpital Saint-Franois-d'Assise",
                 "L'Htel-Dieu de Qubec", "Hpital de l'Enfant-Jsus", "Hpital du Saint-Sacrement",
                 "Institut universitaire de cardiologie et de pneumologie de Qubec"]

class Data:
    _classification = ["hourly_variation", "step_variation", "regression"]
    _normalization = ["min-max", "mean", "none"]

    def __init__(self, _step = 0.25, _max = 1.75, classification = _classification[0], type_y = 'hourly',
                 categorical = ['WEATHER', 'WEATHER_DESCRIPTION', 'NOM_HOSPITAL'], normalization = _normalization[0]):
        # Connection to the database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='
            + database + ';UID=' + username + ';PWD=' + password)

        # Load all data from the DB
        df = pd.read_sql("select * from MAIN", cnxn)
        self.categorical_vars = categorical
        self.numerical_vars = df.columns.drop(categorical)

        self.y = pd.DataFrame()

        # Formats the dataset to have y be a categorical variable based on the value of type_y
        if classification == 'hourly_variation':
            # Hourly variation (-1 iq)
            temp = df[['LOCAL_TIME', 'NB_CIV_OCC', 'NOM_HOSPITAL']].groupby("NOM_HOSPITAL", as_index=False)\
                .apply(
                lambda x: (x.NB_CIV_OCC - x.NB_CIV_OCC.shift())
                    .where((x.LOCAL_TIME - x.LOCAL_TIME.shift()).dt.total_seconds()/60 < 120))\
                .reset_index(level=0).sort_index()['NB_CIV_OCC']
            # Drop the rows of every NA values
            df = df.mask(temp.isnull(), pd.NA).dropna().reset_index(level=0, drop=True)
            self.y, _ = pd.factorize(temp.dropna().reset_index(level=0, drop=True))

            self.X = pd.DataFrame()

            # Third column corresponds to the hour of the day (0-23)
            self.X['HEURE'] = df['LOCAL_TIME'].dt.hour
            # Second column corresponds to the day of the week (0-6)
            self.X['JOUR'] = df['LOCAL_TIME'].dt.dayofweek
            self.X['WEATHER_DESCRIPTION'], _ = pd.factorize(df['WEATHER_DESCRIPTION'])
            self.X['TEMP'], _ = pd.factorize(df['TEMP'])
            self.X['HUMIDITY'], _ = pd.factorize(df['HUMIDITY'])
            self.X['WEATHER'], _ = pd.factorize(df['WEATHER'])

            if normalization == "min-max":
                self.X = (self.X - self.X.min())/(self.X.max() - self.X.min())
            elif normalization == "mean":
                self.X = (self.X - self.X.mean())/self.X.std()

        elif classification == 'step_variation':
            norm = np.zeros(round(_max / _step))
            for i in range(len(norm)):
                norm[i] = (i + 1) * _step
            reformat = np.vectorize(lambda x: min(norm, key=lambda y: abs(x - y)))
            self.y, _ = pd.factorize(reformat((df['NB_CIV_OCC'] / df['NB_CIV_FONC']).array))

            self.X = pd.DataFrame()

            # Third column corresponds to the hour of the day (0-23)
            self.X['HEURE'] = df['LOCAL_TIME'].dt.hour
            # Second column corresponds to the day of the week (0-6)
            self.X['JOUR'] = df['LOCAL_TIME'].dt.dayofweek
            self.X['WEATHER_DESCRIPTION'], _ = pd.factorize(df['WEATHER_DESCRIPTION'])
            self.X['TEMP'], _ = pd.factorize(df['TEMP'])
            self.X['HUMIDITY'], _ = pd.factorize(df['HUMIDITY'])
            self.X['WEATHER'], _ = pd.factorize(df['WEATHER'])

            if normalization == "min-max":
                self.X = (self.X - self.X.min())/(self.X.max() - self.X.min())
            elif normalization == "mean":
                self.X = (self.X - self.X.mean())/self.X.std()


        # Formats the dataset to have y be a continuous variable to use in regression functions

        elif classification == 'regression':
            # Creation du y qui sera utilise
            df['TAUX_OCC'] = df.NB_CIV_OCC / df.NB_CIV_FONC

            if (type_y == 'hourly'):
                # Conversion des variables categorielles
                #                self.categorical_conversion()

                # Extraction of the month, hour and day of the week
                df['MOIS'] = df['LOCAL_TIME'].dt.month
                df['HEURE'] = df['LOCAL_TIME'].dt.hour
                df['JOUR'] = df['LOCAL_TIME'].dt.dayofweek
                df.drop('LOCAL_TIME', axis=1, inplace=True)

                self.y = df['TAUX_OCC']
                self.X = df.drop(labels=['TAUX_OCC', 'NB_CIV_OCC', 'NB_CIV_FONC'], axis=1)

            elif (type_y == 'by_day'):
                # Extraction of the "date" portion of the TimeStamp
                df['DATE'] = df.LOCAL_TIME.dt.date

                # Grouping by date and by hospital
                temp = df.groupby(['NOM_HOSPITAL', 'DATE'])
                new_df = temp[self.numerical_vars].mean()
                new_df['TAUX_OCC_MOYEN'] = temp['TAUX_OCC'].mean()

                for v in self.categorical_vars:
                    uniques = temp[v].apply(lambda x: np.unique(x, return_counts=True))
                    mod = uniques.apply(lambda x: x[0][np.argmax(x[1])])
                    new_df[v] = mod

                # Extraction of the month and day of the week

                #                df['MOIS'] = df['DATE'].dt.month
                #                df['JOUR'] = df['DATE'].dt.dayofweek
                #                df.drop('DATE', axis=1, inplace=True)

                self.y = new_df['TAUX_OCC_MOYEN']
                self.X = new_df.drop(labels=['TAUX_OCC_MOYEN', 'NB_CIV_OCC', 'NB_CIV_FONC'], axis=1)


    def categorical_conversion(self, df):
        conv_weather_desc, self.dict_weather_desc = pd.factorize(df['WEATHER_DESCRIPTION'])
        conv_nom_hop, self.dict_nom_hop = pd.factorize(df['NOM_HOSPITAL'])
        conv_weather, self.dict_weather = pd.factorize(df['WEATHER'])

        df['WEATHER_DESCRIPTION'] = conv_weather_desc
        df['NOM_HOSPITAL'] = conv_nom_hop
        df['WEATHER'] = conv_weather


    def get_x_y(self):
        return self.X, self.y


    # Normalisation de variables
    # Par defaut, normalise toutes les var. numeriques
    def boxcox_transformation(self, X, liste_vars=['NB_PATIENT_CIV_24_H',
                               'NB_PATIENT_CIV_48_H', 'TEMP', 'HUMIDITY', 'PRESSURE', 'VISIBILITY', 'WIND_SPEED'], plot=True):
        # Iteration sur toutes les variables a normaliser
        if plot:
            lim_inf = -20
            lim_sup = 20

            # Nombre de graphiques a imprimer
            taille = len(liste_vars)
            nb_cols = round(math.sqrt(taille))
            fig, subfigs = pyplot.subplots(nb_cols, nb_cols, tight_layout=True)
            for var, subfig in zip(liste_vars, subfigs.reshape(-1)):
                if (X[var] <= 0).any():
                    val_min = X[var].min()
                    X[var] = X[var] + abs(val_min) + 1

                norm_data, lmda = stats.boxcox(X[var])
                stats.boxcox_normplot(X[var], lim_inf, lim_sup, plot=subfig)
                subfig.set_title(var)
                subfig.axvline(lmda, color='red')
                subfig.set_xticks([lmda])
                X[var] = norm_data
            pyplot.show()

            fig2, subfigs2 = pyplot.subplots(nb_cols, nb_cols, tight_layout=True)
            for var, subfig in zip(liste_vars, subfigs2.reshape(-1)):
                norm_data, lmda = stats.boxcox(X[var])
                stats.boxcox_normplot(X[var], lim_inf, lim_sup, plot=subfig)
                subfig.hist(norm_data)
                subfig.set_title(var)
            pyplot.show()
        else:
            for var in liste_vars:
                if (X[var] <= 0).any():
                    val_min = X[var].min()
                    X[var] = X[var] + abs(val_min) + 1
                norm_data, lmda = stats.boxcox(X[var])
                X[var] = norm_data


