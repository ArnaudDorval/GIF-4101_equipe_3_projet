import urllib.request
from bs4 import BeautifulSoup
import datetime
import re

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
        fp = urllib.request.urlopen(url)
        html = fp.read()
        #soup = BeautifulSoup(html, features="lxml")
        soup = BeautifulSoup(html, features="html.parser")

        html_body = soup.find("body").get_text().split("\n")
        now = datetime.datetime.now()
        now_str = " " + str(now.hour) + ":00 "

        hourly_data = []
        temp_data = []
        counter = 0
        for i in html_body:
            if (i != ""):
                temp_data.append(i)

        for r in temp_data:
            if str(r) == now_str:
                for j in range(16):
                    hourly_data.append(temp_data[counter + j])
                break
            counter += 1

        self.heure = hourly_data[0]
        self.temperature_value = re.sub(r'[()]', '', str(hourly_data[3]).replace(u'\xa0', u' ').strip(" "))
        self.temperature_value.replace(",", ".")
        self.temperature_value.strip()
        self.climat = hourly_data[1]
        self.vent = hourly_data[8]
        self.humidex = "NA"
        self.humidite_relative = hourly_data[10]


        return True

    def format_csv(self):
        temp_str = self.heure + ";" + self.temperature_value + ";" \
                   + self.climat + ";" + self.vent + ";" + self.humidex \
                   + ";" + self.humidite_relative

        return temp_str