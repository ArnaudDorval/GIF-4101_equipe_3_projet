# Ca prend ODBC Driver 17 : https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
import pyodbc # pip install pyodbc
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

dict_achalandage = {0.25:'Pas achalande',
                    0.5:'Peu achalende',
                    0.75:'achalande',
                    1.0:'tres achalande',
                    1.25:'tres tres achalande',
                    1.50:'extremement achalande',
                    1.75:'absurdement achalande'}

class get_db_data:

    def __init__(self):
        pass

    def get_all(self):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE='
            + database + ';UID=' + username + ';PWD=' + password)
        sql = "select * from MAIN";
        data = pd.read_sql(sql, cnxn)

        return data

    def check_civ_available(self, p_df):
        # todo : verifier si le nb civiere est dispo
        pass

    def make_weather_desc_list(self, p_df):
        #a = p_df["WEATHER_DESCRIPTION"]
        weather_list = p_df['WEATHER_DESCRIPTION'].str.split(';\s*', expand=True).stack().unique()

        #l'index de a c'est la valeur par la quel on remplace le string weather description
        f = list(range(0, len(weather_list)))
        p_dict = dict(zip(weather_list, f))
        self.weather_list = p_dict
        return p_dict

    def weather_desc_to_int(self, p_df):
        p_df["WEATHER_DESCRIPTION"].replace(self.weather_list, inplace=True)
        return p_df

    def normaliser_valeur_de_civ(self, p_df):

        tmp_list = []
        for ind in p_df.index:
            nb_disp = p_df['NB_CIV_FONC'][ind]
            nb_occupe = p_df['NB_CIV_OCC'][ind]
            tmp_list.append(nb_occupe/nb_disp)

        p_df['CIV_NORMALISE'] = tmp_list
        #print(p_df.head())
        print("valeur d'achalandage maximal : " + str(max(tmp_list)))
        return p_df

    def val_norm_to_class(self, p_df_row):
        t = p_df_row["CIV_NORMALISE"]
        for key in dict_achalandage:
            if t < key:
                #print(dict_achalandage.get(key))
                #print(dict_achalandage[key])
                return dict_achalandage.get(key)
                break

    def convert_civ_norm_closest_class(self, p_df):
        tmp_list = []
        for ind in p_df.index:
            val_norm = p_df['CIV_NORMALISE'][ind]
            for key in dict_achalandage:
                if val_norm < key:
                    #print(key)
                    tmp_list.append(key)
                    break

        p_df['CIV_NORMALISE_CLASS'] = tmp_list
        return p_df

    def plot_tempurature(self, p_df):
        p_df.plot(kind='scatter', x='LOCAL_TIME', y="TEMP", color='red')
        plt.show()

    def plot_data_for_all(self, p_tag, p_df):
        hopital_laval = p_df[p_df['NOM_HOSPITAL'] == "Le Centre hospitalier de l'Universit Laval"]
        hopital_francois = p_df[p_df['NOM_HOSPITAL'] == "Hpital Saint-Franois-d'Assise"]
        hopital_dieu = p_df[p_df['NOM_HOSPITAL'] == "L'Htel-Dieu de Qubec"]
        hopital_jesus = p_df[p_df['NOM_HOSPITAL'] == "Hpital de l'Enfant-Jsus"]
        hopital_sacrament = p_df[p_df['NOM_HOSPITAL'] == "Hpital du Saint-Sacrement"]
        hopital_cardiologie = p_df[
            p_df['NOM_HOSPITAL'] == "Institut universitaire de cardiologie et de pneumologie de Qubec"]

        y_data = p_tag
        x_data = "LOCAL_TIME"

        plt.figure(1)
        plt.scatter(hopital_laval[x_data], hopital_laval[y_data])
        plt.scatter(hopital_francois[x_data], hopital_francois[y_data])
        plt.scatter(hopital_dieu[x_data], hopital_dieu[y_data])
        plt.scatter(hopital_jesus[x_data], hopital_jesus[y_data])
        plt.scatter(hopital_sacrament[x_data], hopital_sacrament[y_data])
        plt.scatter(hopital_cardiologie[x_data], hopital_cardiologie[y_data])
        plt.xlabel(x_data)
        plt.ylabel(y_data)
        plt.title('Raw Data')
        plt.legend(("Universit Laval", "St-Franois",
                    "L'Htel-Dieu", "Enfant-Jsus", "St-Sacrement",
                    "IUCPQ"), loc='upper center',
                   bbox_to_anchor=(0.5, -0.05),
                   fancybox=True, shadow=True, ncol=6)

        plt.grid(True)
        plt.show()