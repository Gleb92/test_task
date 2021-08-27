import string
import requests
import json
from datetime import datetime

class request_api:

    def __init__(self):
        self.response = None
        self.data = None
        self.data_sun = None
#    def get_response(self):
#        resp = requests.get("https://api.openweathermap.org/data/2.5/forecast?q=Novorossiysk&units=metric&appid={dc656efa3de1123bdfb47245cfa29e8c}")
#        self.response = resp.text
    def parser_json(self):
#        parsed_json = json.load(self.response)
#        self.data = parsed_json
        with open('rest.json') as f:
            self.data = json.load(f)
        return self.data
    def get_sun_response(self):
        #resp = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=44.7239&lon=37.7708&exclude=current&appid=dc656efa3de1123bdfb47245cfa29e8c")
        with open('sun.json') as f:
            self.data_sun = json.load(f)
        return self.data_sun

test = request_api()
#test.get_response()
data = test.parser_json()
data_sun = test.get_sun_response()

class MinDifferenceTemperature:
     
     def __init__(self):
         self.days = {}
         self.day = None
         self.different = None

     def count_day(self, data):
        for index in data["list"]:
            data_feel = index["main"]["feels_like"] 
            data_temp = index["main"]["temp"] 
            data_day= index["dt_txt"]
            day_fell_temper = data_feel - data_temp
            day_fell_temper = abs(day_fell_temper)
            self.days[data_day] = day_fell_temper
        return self.days

     def sort_dict(self):
        sorted_values = sorted(self.days, key=self.days.get)
        for day in sorted_values:
            if day.find("00:00:00") != -1 or day.find("03:00:00") != -1:
                self.day = day
                break

     def print_values(self):
         self.different = self.days.get(self.day)
         print(self.day,  " была минимальная разница ночной температу и составляла: ", self.different,"C")

test1 = MinDifferenceTemperature()
#test1.count_day(data)
#test1.count_day(data)
#test1.sort_dict()
#test1.print_values()


class MaxLengthDay:
    def __init__(self):
        self.days = {}
        self.day = None
        self.different = None
        self.time_code = f'%Y-%m-%d'
        self.hours_code = f'%H:%M:%S'

    def count_sun_day(self, data):
        for index in data["daily"]:
            data_sunset = index["sunset"]
            data_sunrise = index["sunrise"] 
            data_day= index["dt"]
            data_day = datetime.utcfromtimestamp(data_day).strftime(self.time_code)
            day_fell_temper = data_sunset - data_sunrise
            day_fell_temper = datetime.utcfromtimestamp(day_fell_temper).strftime(self.hours_code)
            self.days[data_day] = day_fell_temper
        return self.days
    def print_five_day(self):
       res1 = dict(list(self.days.items())[0:5])  
       return print(res1)

test2 = MaxLengthDay()
test2.count_sun_day(data_sun)
test2.print_five_day()
