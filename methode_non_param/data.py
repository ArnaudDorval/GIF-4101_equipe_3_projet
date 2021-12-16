import numpy
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
import pyodbc
import pandas as pd
from sklearn.model_selection import train_test_split

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
    _classification = ["hourly_variation", "step_variation", "regression"]
    _normalization = ["min-max", "mean", "none"]
    def __init__(self, _step=0.25, _max=1.75, classification = _classification[0], normalization = _normalization[0]):
        # Connect to the database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='
            + database + ';UID=' + username + ';PWD=' + password)
        # Load data from the database
        df = pd.read_sql("select * from MAIN", cnxn)

        self.y = pd.DataFrame()
        if classification == "hourly_variation":
            # Hourly variation (-1 iq)
            temp = df[['LOCAL_TIME', 'NB_CIV_OCC', 'NOM_HOSPITAL']].groupby("NOM_HOSPITAL", as_index=False)\
                .apply(
                lambda x: (x.NB_CIV_OCC - x.NB_CIV_OCC.shift())
                    .where((x.LOCAL_TIME - x.LOCAL_TIME.shift()).dt.total_seconds()/60 < 120))\
                .reset_index(level=0).sort_index()['NB_CIV_OCC']
            # Drop the rows of every NA values
            df = df.mask(temp.isnull(), pd.NA).dropna().reset_index(level=0, drop=True)

            df["variation"] = temp.dropna().reset_index(level=0, drop=True)
            column_values = df[['variation']].values
            print(numpy.unique(column_values))
            lim_low = 0
            lim_high = 8
            df_high = df.drop(df[df['variation'] < lim_low].index)
            df_high = df_high.drop(df_high[df_high['variation'] > lim_high].index)
            df_low = df.drop(df[df['variation'] > -1].index)
            df_low = df_low.drop(df_low[df_low['variation'] < -lim_high].index)

            df = pd.concat([df_low, df_high])
            column_values = df[['variation']].values
            print(numpy.unique(column_values))
            df.reset_index(inplace=True)
            self.y, _ = pd.factorize(df['variation'])
            #self.y, _ = pd.factorize(temp.dropna().reset_index(level=0, drop=True))

        elif classification == "step_variation":
            norm = numpy.zeros(round(_max / _step))
            for i in range(len(norm)):
                norm[i] = (i + 1) * _step
            reformat = numpy.vectorize(lambda x: min(norm, key=lambda y: abs(x - y)))
            self.y, _ = pd.factorize(reformat((df['NB_CIV_OCC'] / df['NB_CIV_FONC']).array))

        self.X = pd.DataFrame()

        # Third column correspond to the hour of the day (0-23)
        self.X['HEURE'] = df['LOCAL_TIME'].dt.hour
        # Second column correspond to the day of the week (0-6)
        self.X['JOUR'] = df['LOCAL_TIME'].dt.dayofweek
        self.X['WEATHER_DESCRIPTION'], _ = pd.factorize(df['WEATHER_DESCRIPTION'])
        self.X['TEMP'], _ = pd.factorize(df['TEMP'])
        self.X['HUMIDITY'], _ = pd.factorize(df['HUMIDITY'])
        self.X['WEATHER'], _ = pd.factorize(df['WEATHER'])

        if normalization == "min-max":
            self.X = (self.X - self.X.min())/(self.X.max() - self.X.min())
        elif normalization == "mean":
            self.X = (self.X - self.X.mean())/self.X.std()

        self.X, X_test, self.y, y_test = train_test_split(self.X, self.y, test_size=0.75)
        self.final_df = X_test
        self.final_df['target'] = y_test
        """
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
            civ_occ = df['NB_CIV_OCC'].mask(temp.isnull(), pd.NA).dropna()
            civ_disp = df['NB_CIV_FONC'].mask(temp.isnull(), pd.NA).dropna()
            u = civ_disp/civ_occ
            self.y, self.explicit_y = pd.factorize(reformat(u.array))

        self.X = df
        """

    def __call__(self):
        return self.X, self.y

    def group_data(self):
        #permet de grouper les datas ex par bloc de 6h
        pass

    def final_data(self):
        return self.final_df