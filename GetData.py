import requests
import json
import PiData
import WeatherData
import random
import RoomData
from datetime import datetime

WEATHER_REST_URI = 'https://radiatorbuddy.azurewebsites.net/api/weatherdata'
SENSOR_REST_URI = 'https://radiatorbuddy.azurewebsites.net/api/sensorsdata'
ROOMS_REST_URI = 'https://radiatorbuddy.azurewebsites.net/api/sensorsdata/rooms'


# Function to create incremented name for each meassurement


def create_new_name(base_string):
    base_string = base_string
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
        forecast_object = create_new_name('forecast')
        forecast_object = WeatherData.create_weatherdata(
            element['main']['temp'], datetime_object, element['clouds']['all'])
        if datetime_object <= datetime_hours_from_now:
            forecast_list.append(forecast_object)
    return forecast_list


# Function to create a list of meassurements, from objects, taken by all sensors

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
        pidata_object = create_new_name('reading')
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


def newest_outdoor_temperature():
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
        pidata_object = create_new_name('reading')
        pidata_object = PiData.create_pidata(element['id'], temperature_with_2_decimals,
                                             location_string, element['inDoor'],
                                             datetime_object)
        if element['inDoor'] == False:
            pi_sensor_list.append(pidata_object)
        while len(pi_sensor_list) > 1:
            if pi_sensor_list[0].timestamp > pi_sensor_list[len(pi_sensor_list)].timestamp:
                del pi_sensor_list[-1]
            if pi_sensor_list[0].timestamp < pi_sensor_list[len(pi_sensor_list)].timestamp:
                pi_sensor_list.insert(
                    1, pi_sensor_list[len(pi_sensor_list)])
    return pi_sensor_list[0]

# Function to create a list of rooms


def get_room(MAC_address):
    room_api_request = requests.get(ROOMS_REST_URI)
    room_api_list = json.loads(room_api_request.text)
    room_api_list == room_api_request.json()
    for element in room_api_list:
        location_string = element['location']
        if location_string.strip() == '':
            location_string = None
        else:
            location_string.strip()
        if MAC_address == element['macAddress']:
            room_object = create_new_name('room')
            room_object = RoomData.create_roomdata(element['macAddress'], location_string, element['inDoor'],
                                                   element['optimalTemperature'], element['minTemperature'], element['maxTemperature'])
    return room_object

    # Test of formatting


# print(newest_outdoor_temperature)
test = create_sensor_list()
for element in test:
    print(PiData.__str__(element))
