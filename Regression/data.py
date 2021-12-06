#Ce fichier permet de récupérer les données de la base de données et de les formater

import pyodbc # pip install pyodbc
import pandas as pd
import pyodbc
import numpy as np
import datetime

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'


class Data:
    def __init__(self):
        #Connexion à la base de données
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='+ database + ';UID=' + username + ';PWD=' + password)

        #Construction dataframe
#        y = pd.read_sql("SELECT round(cast (NB_CIV_OCC as float)/cast(NB_CIV_FONC as float),2) as TAUX_OCC from MAIN ", cnxn, columns = ['TAUX_OCC'])
        y = pd.read_sql("SELECT round(sum(cast (NB_CIV_OCC as float)) / sum(cast(NB_CIV_FONC as float)),3) as TAUX_OCC_MOY from MAIN group by dbo.DATE_OF(LOCAL_TIME), NOM_HOSPITAL", cnxn, columns = ['TAUX_OCC_MOY'])
#        x = pd.read_sql("SELECT"
#                               " dbo.DATE_OF(LOCAL_TIME) as LOCAL_TIME, NOM_HOSPITAL, NB_PATIENT_CIV_24_H,"
#                               "NB_PATIENT_CIV_48_H, TEMP, HUMIDITY, PRESSURE, VISIBILITY, WIND_SPEED,WEATHER, WEATHER_DESCRIPTION FROM MAIN", cnxn, columns=['LOCAL_TIME', 'NOM_HOSPITAL','NB_PATIENT_CIV_24_H',
#                                             'NB_PATIENT_CIV_48_H', 'TEMP', 'HUMIDITY', 'PRESSURE', 'VISIBILITY',
#                                             'WIND_SPEED', 'WEATHER', 'WEATHER_DESCRIPTION'])
        x = pd.read_sql("SELECT"
                               " dbo.DATE_OF(LOCAL_TIME) as LOCAL_TIME, NOM_HOSPITAL, avg(NB_PATIENT_CIV_24_H) as NB_PATIENT_CIV_24_H_AVG,"
                               "avg(NB_PATIENT_CIV_48_H) as NB_PATIENT_CIV_48_H_AVG, avg(TEMP) as TEMP_AVG, avg(HUMIDITY) as HUMIDITY_AVG, avg(PRESSURE) as PRESSURE_AVG, avg(VISIBILITY) as VISIBILITY_AVG, avg(WIND_SPEED) as WIND_SPEED_AVG,WEATHER, WEATHER_DESCRIPTION from MAIN group by NOM_HOSPITAL, dbo.DATE_OF(LOCAL_TIME), WEATHER, WEATHER_DESCRIPTION", cnxn, columns=['LOCAL_TIME', 'NOM_HOSPITAL','NB_PATIENT_CIV_24_H',
                                             'NB_PATIENT_CIV_48_H', 'TEMP', 'HUMIDITY', 'PRESSURE', 'VISIBILITY',
                                             'WIND_SPEED', 'WEATHER', 'WEATHER_DESCRIPTION'])
        #Conversion des donnees categorielles
        conv_weather_desc, self.dict_weather_desc = pd.factorize(x['WEATHER_DESCRIPTION'])
        conv_nom_hop, self.dict_nom_hop = pd.factorize(x['NOM_HOSPITAL'])
        conv_weather, self.dict_weather = pd.factorize(x['WEATHER'])

        self.vars_cat = ['WEATHER_DESCRIPTION','NOM_HOSPITAL', 'WEATHER']

        x['WEATHER_DESCRIPTION'] = conv_weather_desc
        x['NOM_HOSPITAL'] = conv_nom_hop
        x['WEATHER'] = conv_weather

        # Conversion des variables categorielles pour avoir une categorie par hopital, par jour
        unique_times = pd.unique(x['LOCAL_TIME'])
        nb_hopitaux = len(self.dict_nom_hop)
        for t in unique_times:
            for hosp in range(nb_hopitaux):
                weather = (x[(x['NOM_HOSPITAL'] == hosp) & (x['LOCAL_TIME'] == t)])['WEATHER'].to_numpy()
                weather_descriptions = (x[(x['NOM_HOSPITAL'] == hosp) & (x['LOCAL_TIME'] == t)])['WEATHER_DESCRIPTION'].to_numpy()

                weather_types, weather_counts = np.unique(weather, return_counts=True)
                weather_desc_types, weather_desc_counts = np.unique(weather_descriptions, return_counts=True)

                # Extrait la position de la valeur la plus frequente
                wt_idx_mode = np.argmax(weather_counts)
                wt_desc_idx_mode = np.argmax(weather_desc_counts)
                x['WEATHER'].where(~((x.NOM_HOSPITAL == hosp) & (x.LOCAL_TIME == t)), other=weather_types[wt_idx_mode],inplace=True)
                x['WEATHER_DESCRIPTION'].where(~((x.NOM_HOSPITAL == hosp) & (x.LOCAL_TIME == t)), other=weather_desc_types[wt_desc_idx_mode],inplace=True)

        # Regroupement des observations pour avoir une ligne par hopital, par jour
        x = x.groupby(['LOCAL_TIME', 'NOM_HOSPITAL']).mean().reset_index()
        x = x.round(decimals=3)

        #normalisation du vecteur y
        y_norm = y.values/y.values.max(axis=0)
        y['TAUX_OCC_MOY'] = y_norm
#        y['TAUX_OCC'] = y_norm

        #Extraire donnees du Timestamp
        x['LOCAL_TIME'] = pd.to_datetime(x['LOCAL_TIME'], dayfirst=True)
        x['MOIS'] = x['LOCAL_TIME'].dt.month
#        x['HEURE'] = x['LOCAL_TIME'].dt.hour
        x['JOUR'] = x['LOCAL_TIME'].dt.dayofweek
        x.drop('LOCAL_TIME', axis=1, inplace=True)

        self.x=x
        self.y=y

    def get_x_y(self):
        return self.x, self.y

if __name__ == '__main__':
    data = Data()
    X,Y=data.get_x_y()
    pd.set_option("display.max_columns", None)  # Permet de voir toutes les colonnes du DF
    print(X.head())
#    print(X.shape)
#    print(d)
    #print(X.values[0])
    #print(X.values[0].size)
    #print(X.columns)
    #print(Y.columns)

#df.values -> donne toutes les lignes avec type numpy array
#df.columns -> donne toutes les variables

#Dictionnaires de conversion pour variables discrètes
#weather_description = {'Clear': 0, 'Clouds': 1, 'Drizzle': 2, 'Fog': 3, 'Mist': 4, 'Rain': 5, 'Snow': 6}

#weather = {'broken clouds': 0, 'clear sky': 1, 'few clouds': 2, 'fog': 3, 'heavy intensity rain': 4, 'light intensity drizzle': 5, 'light intensity drizzle rain': 6, 'light intensity shower rain': 7, 'light rain': 8, 'light shower snow': 9, 'light snow': 10, 'mist': 11, 'moderate rain': 12, 'overcast clouds': 13, 'scattered clouds': 14, 'shower rain': 15, 'snow': 16}

#nom_hopital = {"Hpital de l'Enfant-Jsus": 0, "Le Centre hospitalier de l'Universit Laval": 1, "Hpital Saint-Franois-d'Assise": 2, "Hpital du Saint-Sacrement": 3,"Institut universitaire de cardiologie et de pneumologie de Qubec": 4, "L'Htel-Dieu de Qubec": 5}


