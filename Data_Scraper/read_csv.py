import pandas as pd
from datetime import date


file_name = 'data/' + str(date.today()) + "-data"

#ouverture du fichier pour traitement
data = pd.read_csv(file_name + ".csv", sep=";")
data = data[["Nom_etablissement", "Nom_installation", "No_permis_installation", "Nombre_de_civieres_fonctionnelles",
               "Nombre_de_civieres_occupees", "Nombre_de_patients_sur_civiere_plus_de_24_heures",
               "Nombre_de_patients_sur_civiere_plus_de_48_heures", "Heure_de_l'extraction_(image)", "Mise_a_jour",
               "heure_meteo", "temperature", "climat", "vent", "humidex", "humidite_relative"]]

print(data.head())
print("ok")