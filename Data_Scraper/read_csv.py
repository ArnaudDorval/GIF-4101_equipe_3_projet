import pandas as pd
from datetime import date
import matplotlib.pyplot as plt


file_name = 'data/' + str(date.today()) + "-data"

#ouverture du fichier pour traitement
#data = pd.read_csv(file_name + ".csv", sep=";")
data = pd.read_csv("data/2021-10-15-data.csv", sep=";")
data = data[["Nom_etablissement", "Nom_installation", "No_permis_installation", "Nombre_de_civieres_fonctionnelles",
               "Nombre_de_civieres_occupees", "Nombre_de_patients_sur_civiere_plus_de_24_heures",
               "Nombre_de_patients_sur_civiere_plus_de_48_heures", "Heure_de_l'extraction_(image)", "Mise_a_jour",
               "heure_meteo", "temperature", "climat", "vent", "humidex", "humidite_relative"]]

print(data.head())

liste_hopital = ["Le Centre hospitalier de l'Universit Laval", "Hpital Saint-Franois-d'Assise",
                 "L'Htel-Dieu de Qubec", "Hpital de l'Enfant-Jsus", "Hpital du Saint-Sacrement",
                 "Institut universitaire de cardiologie et de pneumologie de Qubec"]

#_mask = data['Nom_installation'] == "B"

hopital_laval = data[data['Nom_installation'] == "Le Centre hospitalier de l'Universit Laval"]
hopital_francois = data[data['Nom_installation'] == "Hpital Saint-Franois-d'Assise"]
hopital_dieu = data[data['Nom_installation'] == "L'Htel-Dieu de Qubec"]
hopital_jesus = data[data['Nom_installation'] == "Hpital de l'Enfant-Jsus"]
hopital_sacrament = data[data['Nom_installation'] == "Hpital du Saint-Sacrement"]
hopital_cardiologie = data[data['Nom_installation'] == "Institut universitaire de cardiologie et de pneumologie de Qubec"]

data.plot(kind='scatter',x='heure_meteo',y='temperature',color='red')
plt.show()

y_data = "Nombre_de_civieres_occupees"
x_data = "heure_meteo"

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
#plt.legend(("Le Centre hospitalier de l'Universit Laval", "Hpital Saint-Franois-d'Assise",
                # "L'Htel-Dieu de Qubec", "Hpital de l'Enfant-Jsus", "Hpital du Saint-Sacrement",
                # "Institut universitaire de cardiologie et de pneumologie de Qubec"), loc='best')
plt.grid(True)
plt.show()
print("ok")

