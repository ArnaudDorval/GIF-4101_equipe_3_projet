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

    def __init__(self, _step=0.25, _max=1.75, p_list = ['HEURE', 'TEMP']):
        # Connect to the database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='
            + database + ';UID=' + username + ';PWD=' + password)
        # Load data from the database
        df = pd.read_sql("select * from MAIN", cnxn)
        self.size = len(df.index)

        # X has 3 dimension : weather, day of the week, hour of the day
        # y correspond to ratio of used stretchers rounded to _step bounded between 0 and _max
        self.X = numpy.zeros((self.size, len(p_list)))
        self.y = numpy.zeros(self.size)
        self.feature_names = numpy.array(p_list)

        for index, val in enumerate(p_list):
            temp_data = []

            if val == 'HEURE':
                # Third column correspond to the hour of the day (0-23)
                temp_data = df['LOCAL_TIME'].dt.hour
            elif val == "JOUR":
                # Second column correspond to the day of the week (0-6)
                temp_data = df['LOCAL_TIME'].dt.dayofweek
            elif val == 'WEATHER_DESCRIPTION':
                # First column correspond to the normalized weather data, we're also saving the types of weather
                # identifying the numerical value
                temp_data, self.explicite_weather_desc = pd.factorize(df['WEATHER_DESCRIPTION'])
            elif val == 'TEMP':
                temp_data, self.explicit_temp = pd.factorize(df['TEMP'])
            elif val == 'HUMIDITY':
                temp_data, self.explicit_humidity = pd.factorize(df['HUMIDITY'])
            elif val == 'WEATHER':
                temp_data, self.explicite_weather = pd.factorize(df['WEATHER'])

            self.X[:, index] = temp_data


            for j in liste_hopital:
                hopital = df[df['NOM_HOSPITAL'] == j]
                tmp_y = hopital['NB_CIV_OCC']
                new_y = []
                old_value = 0
                for b in tmp_y:
                    if old_value > 0:
                       new_y.append(tmp_y.index(b) - old_value)

                    old_value = b
                    print("ok")

    def __call__(self):
        return self.X, self.y

    def normalize_civ(self, _max, _step, df):
        # Initializing a temp array of all the steps for the stretchers classes
        norm = numpy.zeros(round(_max / _step))
        for i in range(len(norm)):
            norm[i] = (i + 1) * _step

        # Reformatting the data to get the class index from the number of used stretchers divided by the number of
        # available stretchers rounded to closest step
        reformat = numpy.vectorize(lambda x: min(norm, key=lambda y: abs(x - y)))
        self.y, self.explicit_y = pd.factorize(reformat((df['NB_CIV_OCC'] / df['NB_CIV_FONC']).array))
