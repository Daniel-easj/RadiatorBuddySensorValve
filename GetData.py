import requests
import json
import PiData
import WeatherData
import random
from datetime import datetime

WEATHER_REST_URI = 'https://radiatorbuddy.azurewebsites.net/api/weatherdata'
SENSOR_REST_URI = 'https://radiatorbuddy.azurewebsites.net/api/sensorsdata'

# Function to fake optimal temp until real optimal temp can be gathered


def fake_temp(minimum_number, maximum_number):
    return random.randint(minimum_number, maximum_number)


# Function to create incremented name for each meassurement


def create_new_pi_name():
    base_string = 'reading'
    counter = 1
    name = base_string + str(counter)
    return name

# Function to create incremented name for each forecast


def create_new_forecast_name():
    base_string = 'forecast'
    counter = 1
    name = base_string + str(counter)
    return name


# Function to create a list of forecasts, from objects


def create_forecast_list(datetime_hours_from_now):
    weather_api_request = requests.get(WEATHER_REST_URI)
    weather_api_list = json.loads(weather_api_request.text)
    weather_api_list == weather_api_request.json()
    forecast_list = list()
    for element in weather_api_list:
        datetime_string = element['dt_txt']
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M:%S')
        forecast_object = create_new_forecast_name()
        forecast_object = WeatherData.create_weatherdata(
            element['main']['temp'], datetime_object, element['clouds']['all'])
        if datetime_object <= datetime_hours_from_now:
            forecast_list.append(forecast_object)
    return forecast_list


# Function to create a list of meassurements, from objects, taken by all sensors

# Filter on inDoor as well???
def create_sensor_list(MAC_Address=None, datetime_start=datetime(2000, 1, 1), datetime_end=datetime(3000, 1, 1)):
    sensor_api_request = requests.get(SENSOR_REST_URI)
    sensor_api_list = json.loads(sensor_api_request.text)
    sensor_api_list == sensor_api_request.json()
    pi_sensor_list = list()
    for element in sensor_api_list:
        # Fix inserted "T" in timestamp, remove whitespace from location, round temperature
        datetime_string_with_T = element['timestamp']
        datetime_string = datetime_string_with_T.replace('T', ' ')
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M:%S')
        location_string = element['location']
        if location_string.strip() == '':
            location_string = None
        else:
            location_string.strip()
        too_long_temperature = element['temperature']
        temperature_with_2_decimals = round(too_long_temperature, 2)
        # Create PiData object, with API data
        pidata_object = create_new_pi_name()
        pidata_object = PiData.create_pidata(element['id'], temperature_with_2_decimals,
                                             location_string, element['inDoor'],
                                             datetime_object)
        if MAC_Address != None:
            if pidata_object.id == MAC_Address and datetime_start <= datetime_object and datetime_end > datetime_object:
                pi_sensor_list.append(pidata_object)
        else:
            if datetime_start <= datetime_object and datetime_end > datetime_object:
                pi_sensor_list.append(pidata_object)
    return pi_sensor_list


# Test of formatting
sensor_list = create_sensor_list()
print(len(sensor_list))
for element in sensor_list:
    # PiData "ToString()"
    print(PiData.__str__(element))
