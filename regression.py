
# Appeler requetes SQL pour sortir les infos necessaires a l'analyse
import pyodbc # pip install pyodbc
import pandas as pd
from datetime import datetime

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

sql0 = "select * from MAIN"
r0 = pd.read_sql(sql0, cnxn)
print(r0)

# Appeler script de formattage des donnees

# Appeler LinearRegression() pour chaque combinaison de variables, et comparer les scores/erreurs de chacun
