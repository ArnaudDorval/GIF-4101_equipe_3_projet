# Ca prend ODBC Driver 17 : https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
import pyodbc # pip install pyodbc
import pandas as pd

server = '24.122.207.31\MSSQLSERVER,1433'
database = 'AI_Hospital'
username = 'ai_user'
password = 'ai_password'



cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

# notre seul table dans la db SQL est "data", donc on request "from data" ou "from DATA", etc.."
sql1 = "select TIMESTAMP, NOM_HOSPITAL, NB_CIV_OCC, NB_CIV_FONC, TEMP, WEATHER from DATA order by NOM_HOSPITAL"
# Timestamp unix epoch-time dans notre database, on peut la convertir en readable local time comme ca
sql2 = "select dateadd(S, TIMESTAMP - 14400, '1970-01-01') as LOCALTIME, NOM_HOSPITAL, NB_CIV_OCC, NB_CIV_FONC, TEMP, WEATHER from data order by LOCALTIME"
# select everything
sql3 = "select * from DATA order by NOM_HOSPITAL"
# temp vs temps
sql4 = "select dateadd(S, TIMESTAMP - 14400, '1970-01-01') as LOCALTIME, TEMP from DATA order by LOCALTIME"
# nb_civieres vs temps
sql5 = "select dateadd(S, TIMESTAMP - 14400, '1970-01-01') as LOCALTIME, NB_CIV_FONC from DATA order by LOCALTIME"

r1 = pd.read_sql(sql1, cnxn)
r2 = pd.read_sql(sql2, cnxn)
r3 = pd.read_sql(sql3, cnxn)
r4 = pd.read_sql(sql4, cnxn)
r5 = pd.read_sql(sql5, cnxn)

print(r1, "\n")
print(r2, "\n")
print(r3, "\n")
print(r4, "\n")
print(r5, "\n")
