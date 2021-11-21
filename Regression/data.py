#Ce fichier permet de récupérer les données de la base de données et de les formater

import pyodbc # pip install pyodbc
import pandas as pd
import pyodbc
import numpy as np

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

class Data:
    def __init__(self):
        #Connexion à la base de données
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='+ database + ';UID=' + username + ';PWD=' + password)

        #Construction dataframe
        y = pd.read_sql("SELECT round(cast (NB_CIV_OCC as float)/cast(NB_CIV_FONC as float),2) as TAUX_OCC from MAIN ", cnxn, columns = ['TAUX_OCC'])
        x = pd.read_sql("SELECT"
                               " LOCAL_TIME, NOM_HOSPITAL, NB_PATIENT_CIV_24_H,"
                               "NB_PATIENT_CIV_48_H, TEMP, HUMIDITY, PRESSURE, VISIBILITY, WIND_SPEED,WEATHER, WEATHER_DESCRIPTION FROM MAIN", cnxn, columns=['LOCAL_TIME', 'NOM_HOSPITAL','NB_PATIENT_CIV_24_H',
                                             'NB_PATIENT_CIV_48_H', 'TEMP', 'HUMIDITY', 'PRESSURE', 'VISIBILITY',
                                             'WIND_SPEED', 'WEATHER', 'WEATHER_DESCRIPTION'])
        #Conversion des données discrètes
        conv_weather_desc, self.dict_weather_desc = pd.factorize(x['WEATHER_DESCRIPTION'])
        conv_nom_hop, self.dict_nom_hop = pd.factorize(x['NOM_HOSPITAL'])
        conv_weather, self.dict_weather = pd.factorize(x['WEATHER'])

        x['WEATHER_DESCRIPTION'] = conv_weather_desc
        x['NOM_HOSPITAL'] = conv_nom_hop
        x['WEATHER'] = conv_weather

        #normalisation du vecteur y
        y_norm = y.values/y.values.max(axis=0)
        y['TAUX_OCC'] = y_norm

        #Extraire donnees du Timestamp
        x['MOIS'] = x['LOCAL_TIME'].dt.month
        x['HEURE'] = x['LOCAL_TIME'].dt.hour
        x['JOUR'] = x['LOCAL_TIME'].dt.dayofweek
        x.drop('LOCAL_TIME', axis=1, inplace=True)

        self.x=x
        self.y=y

    def get_x_y(self):
        return self.x, self.y

if __name__ == '__main__':
    data = Data()
    X,Y=data.get_x_y()
    print(X,Y)
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


