import csv
import requests

CSV_URL = 'http://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Releve_horaire_urgences_7jours.csv'

lieux = ["CHU", "Institut universitaire de cardiologie et de pneumologie de Qubec"]

def fetchDonneesQuebec():
    resp = requests.get(CSV_URL)
    content = resp.content.decode('utf-8', errors='ignore')
    cr = csv.reader(content.splitlines(), delimiter=',')
    data = list(cr)
    updateTime = (data[2][8])
    f_ = open('./prevUpdate.txt', 'r')
    prevUpdateTime = f_.read()
    f_.close()
    if updateTime != prevUpdateTime:
        f__ = open('./prevUpdate.txt', 'w')
        f__.write(updateTime)
        f__.close()
        f = open('./Data.txt', 'a')
        for l in data:
            if l[0] in lieux:
                for l_ in l:
                    f.write(l_)
                    f.write(',')
                f.write('\n')
        f.close()


fetchDonneesQuebec()
