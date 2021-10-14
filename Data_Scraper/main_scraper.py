from temperature_fetch import *
from hospital_fetch import *
import time
from datetime import date
import os

data = "Nom_etablissement;Nom_installation;No_permis_installation;Nombre_de_civieres_fonctionnelles;" \
       "Nombre_de_civieres_occupees;Nombre_de_patients_sur_civiere_plus_de_24_heures;" \
       "Nombre_de_patients_sur_civiere_plus_de_48_heures;Heure_de_l'extraction_(image);Mise_a_jour;heure_meteo;" \
       "temperature;climat;vent;humidex;humidite_relative\n"

dataSet = [data]
file_name = 'data/' + str(date.today()) + "-data.csv"

temperature_obj = Temperature()
while (1):

    donnees_quebec_list = fetch_Donnees_Quebec_Data_Frame()
    buf_name = 'data/' + str(date.today()) + "-data.csv"

    if(not os.path.isfile(buf_name)):
        f = open(buf_name, "x")
        f.write(data)
        f.close()
        file_name = buf_name

    if(donnees_quebec_list):
        temperature_obj.fetch()
        temp_list = []
        for i in donnees_quebec_list:
            temp_list.append(i + temperature_obj.format_csv() + "\n")

        f = open(file_name, "a")
        for t in temp_list:
            f.write(t)
            print(t)
        f.close()

    time.sleep(60*15)
    print(str(datetime.now()))
