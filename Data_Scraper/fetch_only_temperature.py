from temperature_fetch import *
from hospital_fetch import *
import time
from datetime import datetime, date
import os
import logging
from git import Repo


#PATH_OF_GIT_REPO = r'C:\Users\arnau\OneDrive\Documents\Universite\Automne 2021\AI\projet\GIF-4101_equipe_3_projet\.git'
COMMIT_MESSAGE = 'Push data files for the day'
PATH_OF_GIT_REPO = r'/home/pi/GIF-4101_equipe_3_projet/.git'

def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    repo.remotes.origin.pull()
    repo.git.add(all=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()



logging.basicConfig(filename='data/error_temp.log', level=logging.DEBUG)

data = "Nom_etablissement;Nom_installation;No_permis_installation;Nombre_de_civieres_fonctionnelles;" \
       "Nombre_de_civieres_occupees;Nombre_de_patients_sur_civiere_plus_de_24_heures;" \
       "Nombre_de_patients_sur_civiere_plus_de_48_heures;Heure_de_l'extraction_(image);Mise_a_jour;heure_meteo;" \
       "temperature;climat;vent;humidex;humidite_relative\n"

dataSet = [data]
file_name = 'data/' + str(date.today()) + "-data-temp.csv"

temperature_obj = Temperature()
while (1):
    temperature_obj.fetch() #il y a un bug dans la fct donc je le fetch  chaque fois
    #comme ca si ca bug sur un temperature bah il tombe en exception pis ca update
    # pas la date de prev update et le programme continu a rouler

    donnees_quebec_list = fetch_Donnees_Quebec_Data_Frame()
    buf_name = 'data/' + str(date.today()) + "-data-temp.csv"

    if(not os.path.isfile(buf_name)):
        #git_push()
        f = open(buf_name, "x")
        f.close()
        file_name = buf_name

    buff = temperature_obj.format_csv() + "\n"

    f = open(file_name, "a")
    f.write(buff)
    print(buff)
    f.close()

    buff_heure = str(datetime.datetime.now())
    print(buff_heure)
    logging.debug(buff_heure)
    time.sleep(10) # sleep 15min
