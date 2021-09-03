import requests
import json
from datetime import datetime
from requests.api import request

class RequestApi:
    def __init__(self, key, url):
        self.key = key
        self.url = url

    def get_json(self):
        return requests.get(f"{self.url}={self.key}").text
            
    def convert_text_to_json(self):
        response = self.get_json()
        return json.loads(response)

class MinDifferenceTemperature:  
     def __init__(self):
         self.temperature_diff_by_days = {}
         self.day = None
         
     def fill_temperature_dict(self, data):
        for index in data["list"]:
            feel_temperature = index["main"]["feels_like"] 
            actual_temperature = index["main"]["temp"] 
            day = index["dt_txt"]
            self.temperature_diff_by_days[day] = self.calculate_temperature_diff(feel_temperature,actual_temperature)

     def calculate_temperature_diff(self, feel_temperature, actual_temperature):
         return abs(feel_temperature - actual_temperature)

     def get_day_min_feel_temperature(self):
        sorted_temperature_dict_by_day = sorted(self.temperature_diff_by_days, key=self.temperature_diff_by_days.get)
        for day in sorted_temperature_dict_by_day:
            if "00:00:00" in day or "03:00:00" in day:
                return day

     def print_values(self):
         day = self.get_day_min_feel_temperature()
         difference = self.temperature_diff_by_days.get(day)
         print(f"{day},  минамальная разница фактической и ощущаемой температуры ночью, которая состовила: , {difference}")

class MaxLengthDay:
    def __init__(self):
        self.days = {}
        self.time_code = f'%Y-%m-%d'
        self.hours_code = f'%H:%M:%S'

    def fill_sun_day_dict(self, data):
        for index in data["daily"]:
            sunset = index["sunset"]
            sunrise = index["sunrise"] 
            day = self.convert_unix_time(index["dt"],self.time_code)
            day_lenght = self.convert_unix_time(self.calculate_sun_day_len(sunset,sunrise), self.hours_code)
            self.days[day] = day_lenght

    def convert_unix_time(self,  timestamp,time_format):
        return datetime.utcfromtimestamp(timestamp).strftime(time_format)

    def calculate_sun_day_len(self,sunset, sunrise):
        return (sunset - sunrise)

    def print_five_day(self):
       res1 = dict(list(self.days.items())[0:5])  
       return print(res1)
       
# client code
my_key = 'dc656efa3de1123bdfb47245cfa29e8c'
host = 'https://api.openweathermap.org/data/2.5/'
path = 'forecast'
params = '?q=Novorossiysk&units=metric'
url = f"{host}{path}{params}&appid"

request_client = RequestApi(my_key,url)
request_client.get_json()
json_response = request_client.convert_text_to_json()

task_one = MinDifferenceTemperature()
task_one.fill_temperature_dict(json_response)
task_one.print_values()

path = 'onecall'
params = '?lat=44.7239&lon=37.7708&exclude=current'
url = f"{host}{path}{params}&appid"

request_client = RequestApi(my_key,url)
request_client.get_json()
json_response = request_client.convert_text_to_json()

task_two = MaxLengthDay()
task_two.fill_sun_day_dict(json_response)
task_two.print_five_day()
