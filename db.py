# Ca prend ODBC Driver 17 : https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
import pyodbc # pip install pyodbc
import pandas as pd
from datetime import datetime

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

# Le server est disponible de 9:30 AM jusqu'à 1:30 AM chaque jour

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

# La main view s'apelle MAIN avec les colonnes suivantes:
# LOCAL_TIME           -> date    (Temps local. Voir les fonctions de temps)
# NOM_HOSPITAL         -> string  (Les noms des hôpitaux sans charactères français comme ç, é, è, etc.
#                                  S'il y a apostrophes dans le nom ('), on en met deux (''), car sql
#                                  utilise uniquement les single quotes pour comparer les strings.
#                                  Voir les exemples sql2, sql3)
# NB_CIV_FONC          -> int     (Nombre de civières fonctionnelles)
# NB_CIV_OCC           -> int     (Nombre de civières occupées)
# NB_PATIENT_CIV_24_H  -> int     (Nombre de patients sur civières depuis plus de 24h)
# NB_PATIENT_CIV_48_H  -> int     (Nombre de patients sur civières depuis plus de 48h)
# TEMP                 -> float   (Température en degré celsius. Peut être comparé avec int. Voir sql5)
# HUMIDITY             -> int     (Indices d'humidité)
# PRESSURE             -> int     (Pression en kPa)
# VISIBILITY           -> int     (Visibilité. Plus haut -> plus de visibilité)
# WIND_SPEED           -> float   (Ne semble pas être en km/h :(, devrait être OK avec une valeur numérique
#                                  mais je vais regarder pour la convertire)
# WEATHER              -> string  (Description de la température en mot. La query sql7
#                                  listes les différentes weather qu'on a eux jusqu'à maintenant)
# WEATHER_DESCRIPTION  -> string  (Description plus détaillée. Voir sql8)

# Fonction de temps:
# dbo.HOUR_OF(LOCAL_TIME)  -> retourne int                      (Voir sql2)
# dbo.DAY_OF(LOCAL_TIME)   -> retourne int
# dbo.MONTH_OF(LOCAL_TIME) -> retourne int
# dbo.YEAR_OF(LOCAL_TIME)  -> retourne int
# dbo.DATE_OF(LOCAL_TIME)  -> retourne une string 'DD-MM-YYYY'  (Voir sql1, sql3)

# Nom des hôpitaux:
# Hpital de l'Enfant-Jsus
# Le Centre hospitalier de l'Universit Laval
# Hpital Saint-Franois-d'Assise
# Hpital du Saint-Sacrement
# Institut universitaire de cardiologie et de pneumologie de Qubec
# L'Htel-Dieu de Qubec

today = datetime.today().strftime("%d-%m-%Y")

sql0 = "select * from MAIN"

sql1 = "select * from MAIN where dbo.DATE_OF(LOCAL_TIME) = '%s'" %today

sql2 = """
       select  NOM_HOSPITAL, NB_CIV_OCC, NB_CIV_FONC, TEMP from MAIN
       where   dbo.HOUR_OF(LOCAL_TIME) > 6
       and     dbo.HOUR_OF(LOCAL_TIME) <= 18
       and     NOM_HOSPITAL = 'Le Centre hospitalier de l''Universit Laval'
       """

sql3 = """
       select  LOCAL_TIME, NOM_HOSPITAL, NB_CIV_FONC, NB_CIV_OCC, TEMP, PRESSURE, WEATHER_DESCRIPTION from MAIN
       where   dbo.DATE_OF(LOCAL_TIME) = '04-11-2021'
       and     NOM_HOSPITAL = 'L''Htel-Dieu de Qubec'
       """

sql4 = """
       select * from MAIN
       where dbo.DATE_OF(LOCAL_TIME) = '04-10-2021'
       """

sql5 = """
       select LOCAL_TIME, NOM_HOSPITAL, TEMP, WEATHER, WEATHER_DESCRIPTION
       from MAIN
       where TEMP < 0 and NOM_HOSPITAL = 'L''Htel-Dieu de Qubec'
       """

sql6 = "select WIND_SPEED from MAIN where NOM_HOSPITAL = 'L''Htel-Dieu de Qubec' order by WIND_SPEED desc"

sql7 = "select WEATHER from MAIN group by WEATHER"

sql8 = "select WEATHER_DESCRIPTION from MAIN group by WEATHER_DESCRIPTION"

sql9 = """
       select    NOM_HOSPITAL, avg(NB_CIV_FONC) as AVG_NB_CIV_FONC, avg(NB_CIV_OCC) as AVG_NOM_CIV_OCC
       from      MAIN
       group by  NOM_HOSPITAL
       order by  AVG_NB_CIV_FONC desc
       """


#r0 = pd.read_sql(sql0, cnxn)
r1 = pd.read_sql(sql1, cnxn)
#r2 = pd.read_sql(sql2, cnxn)
#r3 = pd.read_sql(sql3, cnxn)
#r4 = pd.read_sql(sql4, cnxn)
#r5 = pd.read_sql(sql5, cnxn)
#r6 = pd.read_sql(sql6, cnxn)
#r7 = pd.read_sql(sql7, cnxn)
#r8 = pd.read_sql(sql8, cnxn)
r9 = pd.read_sql(sql9, cnxn)


#pd.set_option("display.max_colwidth", None) # Utile pour print des longues strings sans que pandas les truncate
pd.set_option("display.max_colwidth", None) # Utile pour print des longues strings sans que pandas les truncate

#print(r0)
print(r1)
#print(r2)
#print(r3)
#print(r4)
#print(r5)
#print(r6)
#print(r7)
#print(r8)
print(r9)
