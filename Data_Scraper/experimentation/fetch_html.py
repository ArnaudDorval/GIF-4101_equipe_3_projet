import urllib.request
from bs4 import BeautifulSoup

url = "https://meteo.gc.ca/past_conditions/index_f.html?station=yqb"

fp = urllib.request.urlopen(url)
html = fp.read()
soup = BeautifulSoup(html)
tags = soup('td')

print("ok")

temp_list = []
temp_str = ""


print("heure")
heure = tags[0]
temp_list = str(heure).split('>')
temp_list = temp_list[1].split(' ')
print(temp_list[1])
print("************************************************************************")
print("Climat")
climat = tags[1]
temp_list = str(climat).split('>')
temp_list = temp_list[10].split('<')
print(temp_list[0])
print("************************************************************************")
print("temperature")
temperature = tags[2]
temp_list = str(temperature).split('>')
temp_list = temp_list[1].split('\n')
print(temp_list[0])
print("************************************************************************")
print("vent km/h")
vent = tags[4]
temp_list = str(vent).split('>')
temp_str = temp_list[2].split('<')[0] + temp_list[3].split('<')[0]
print(temp_str)
print("************************************************************************")
print("humidex")
humidex = tags[6]
temp_list = str(humidex).split('>')
temp_str = temp_list[2].split("<")[0]
print(temp_str)
print("************************************************************************")
print("humidite relative %")
humidite_relative = tags[8]
temp_list = str(humidite_relative).split('>')
temp_str = temp_list[1].split("<")[0]
print(temp_str)
print("************************************************************************")
print("point de rosee celsius")
point_rosee = tags[9]
temp_list = str(point_rosee).split('>')
temp_str = temp_list[1].split("<")[0]
print(temp_str)
print("************************************************************************")
print("Pression kPa")
pression = tags[11]
temp_list = str(pression).split('>')
temp_str = temp_list[1].split("<")[0]
print(temp_str)
print("************************************************************************")
print(" Visibilité km")
visibilite = tags[13]
temp_list = str(visibilite).split('>')
temp_str = temp_list[1].split("<")[0]
print(temp_str)
print("************************************************************************")