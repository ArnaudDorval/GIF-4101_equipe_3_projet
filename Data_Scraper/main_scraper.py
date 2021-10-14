from temperature_fetch import *
from hospital_fetch import *
import time

data = "Nom_etablissement;Nom_installation; No_permis_installation;Nombre_de_civieres_fonctionnelles;" \
       "Nombre_de_civieres_occupees; Nombre_de_patients_sur_civiere_plus_de_24_heures;" \
       "Nombre_de_patients_sur_civiere_plus_de_48_heures;Heure_de_l'extraction_(image);Mise_a_jour;" \
       "heure_meteo;temperature;climat;vent;humidex;humidite_relative"

dataSet = [data]


temperature_obj = Temperature()
while (1):
    temperature_obj.fetch()
    print(temperature_obj.format_csv() + "\n")
    donnees_quebec_list = fetch_Donnees_Quebec_Data_Frame()

    temp_list = []
    for i in donnees_quebec_list:
        temp_list.append(i + temperature_obj.format_csv())

    for t in temp_list:
        print(t + "\n")

    time.sleep(5)
