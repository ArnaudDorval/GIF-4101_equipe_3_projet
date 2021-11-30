import numpy
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
import pyodbc
import pandas as pd

server = r'24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

dict_achalandage = numpy.array(['Pas achalande', 'Peu achalende', 'achalande', 'tres achalande', 'tres tres achalande',
                                'extremement achalande', 'absurdement achalande'])

liste_hopital = ["Le Centre hospitalier de l'Universit Laval", "Hpital Saint-Franois-d'Assise",
                 "L'Htel-Dieu de Qubec", "Hpital de l'Enfant-Jsus", "Hpital du Saint-Sacrement",
                 "Institut universitaire de cardiologie et de pneumologie de Qubec"]

class Data:

    def __init__(self, _step=0.25, _max=1.75, p_list = ['HEURE', 'WEATHER'], type_y = "variation-1"):
        # Connect to the database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='
            + database + ';UID=' + username + ';PWD=' + password)
        # Load data from the database
        df = pd.read_sql("select * from MAIN", cnxn)
        self.size = len(df.index)

        temp = df[['LOCAL_TIME', 'NB_CIV_OCC', 'NOM_HOSPITAL']].groupby("NOM_HOSPITAL", as_index=False)\
            .apply(
            lambda x: (x.NB_CIV_OCC - x.NB_CIV_OCC.shift())
                .where((x.LOCAL_TIME - x.LOCAL_TIME.shift()).dt.total_seconds()/60 < 120))\
            .reset_index(level=0).sort_index()['NB_CIV_OCC']

        # X has 3 dimension : weather, day of the week, hour of the day
        # y correspond to ratio of used stretchers rounded to _step bounded between 0 and _max
        self.X = numpy.zeros((temp.dropna().size, len(p_list)))
        self.y = numpy.zeros(temp.dropna().size)
        self.feature_names = numpy.array(p_list)

        for index, val in enumerate(p_list):
            temp_data = []

            if val == 'HEURE':
                # Third column correspond to the hour of the day (0-23)
                temp_data = df['LOCAL_TIME'].dt.hour.mask(temp.isnull(), pd.NA).dropna().apply(lambda x: x - 1 % 24)
            elif val == "JOUR":
                # Second column correspond to the day of the week (0-6)
                temp_data = df['LOCAL_TIME'].dt.dayofweek.mask(temp.isnull(), pd.NA).dropna()
            elif val == 'WEATHER_DESCRIPTION':
                # First column correspond to the normalized weather data, we're also saving the types of weather
                # identifying the numerical value
                temp_data, self.explicite_weather_desc = pd.factorize(df['WEATHER_DESCRIPTION'].mask(temp.isnull(), pd.NA).dropna())
            elif val == 'TEMP':
                temp_data, self.explicit_temp = pd.factorize(df['TEMP'].mask(temp.isnull(), pd.NA).dropna())
            elif val == 'HUMIDITY':
                temp_data, self.explicit_humidity = pd.factorize(df['HUMIDITY'].mask(temp.isnull(), pd.NA).dropna())
            elif val == 'WEATHER':
                temp_data, self.explicite_weather = pd.factorize(df['WEATHER'].mask(temp.isnull(), pd.NA).dropna())

            self.X[:, index] = temp_data

        if(type_y == "variation-1"):
            # retourne des classes pour les differente variation heure par heure
            self.y, self.explicit_y = pd.factorize(temp.mask(temp.isnull(), pd.NA).dropna())
            self.X = self.X[:-1, :]
            self.explicit_y = numpy.delete(self.explicit_y, 0)
            self.y = numpy.delete(self.y, 0)

        elif(type_y == "normalised_variation"):
            # retourne la distribution entre [0,1] de la variation heure par heure
            n = []
            arr = numpy.asarray(temp.mask(temp.isnull(), pd.NA).dropna())
            for i in arr:
                n.append((i - min(arr)) / (max(arr) - min(arr)))
            print("ok")
            self.y = n
            self.explicit_y = arr

        elif (type_y == "civ_occ/civ_dispo"):
            # retourne un y avec des classe pour le taux doccupation selon le step par défaut 25%
            norm = numpy.zeros(round(_max / _step))
            for i in range(len(norm)):
                norm[i] = (i + 1) * _step

            # Reformatting the data to get the class index from the number of used stretchers divided by the number of
            # available stretchers rounded to closest step
            reformat = numpy.vectorize(lambda x: min(norm, key=lambda y: abs(x - y)))
            self.y, self.explicit_y = pd.factorize(reformat((df['NB_CIV_OCC'] / df['NB_CIV_FONC']).array))

    def __call__(self):
        return self.X, self.y
