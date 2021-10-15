import urllib.request
from bs4 import BeautifulSoup
import datetime

url = "https://meteo.gc.ca/past_conditions/index_f.html?station=yqb"

fp = urllib.request.urlopen(url)
html = fp.read()

soup = BeautifulSoup(html)

h = soup.find("td").findParent()
v = soup.find("body").get_text()
w = v.split("\n")
#print(v)

now = datetime.datetime.now()
print(now.hour)

now_str = " " + str(now.hour) + ":00 "
hourly_data = []
temp_data = []
counter = 0
for i in w:
    if (i != ""):
        temp_data.append(i)

for r in temp_data:
    if(str(r) == now_str):
        for j in range(16):
            hourly_data.append(temp_data[counter + j])
        break
    counter += 1

print("ok")