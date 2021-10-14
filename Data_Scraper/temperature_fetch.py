import urllib.request
from bs4 import BeautifulSoup
from datetime import *

url = "https://meteo.gc.ca/past_conditions/index_f.html?station=yqb"


class Temperature:
    heure = ""
    temperature_value = ""
    climat = ""
    vent = ""
    humidex = ""
    humidite_relative = ""

    def __init__(self):
        pass

    def fetch(self):
        print("fetch")
        fp = urllib.request.urlopen(url)
        html = fp.read()
        soup = BeautifulSoup(html)
        tags = soup('td')

        temp_list = []
        temp_str = ""

        ## heure
        temp_str = tags[0]
        temp_list = str(temp_str).split('>')
        self.heure = temp_list[1].split(' ')[1]
        ############################################
        # Climat
        temp_str = tags[1]
        temp_list = str(temp_str).split('>')
        self.climat = temp_list[10].split('<')[0]
        ############################################
        # temperature
        temp_str = tags[2]
        temp_list = str(temp_str).split('>')
        self.temperature_value = temp_list[1].split('\n')[0]
        ############################################
        # vent km/h
        temp_str = tags[4]
        temp_list = str(temp_str).split('>')
        self.vent = temp_list[2].split('<')[0] + temp_list[3].split('<')[0]
        ############################################
        # humidex
        temp_str = tags[6]
        temp_list = str(temp_str).split('>')
        self.humidex = temp_list[2].split("<")[0]
        ############################################
        # humidite relative %
        temp_str = tags[8]
        temp_list = str(temp_str).split('>')
        self.humidite_relative = temp_list[1].split("<")[0]
        return True

    def format_csv(self):
        temp_str = self.heure + ";" + self.temperature_value + ";" \
                   + self.climat + ";" + self.vent + ";" + self.humidex \
                   + ";" + self.humidite_relative

        return temp_str