from temperature_fetch import *
from hospital_fetch import *
import time


temperature_obj = Temperature()
while(1):

    temperature_obj.fetch()
    print(temperature_obj.format_csv() + "\n")
    time.sleep(5)