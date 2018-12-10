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


def create_new_name(base_string):
    base_string = base_string
    counter = 1
    name = base_string + str(counter)
    return name


def extract_json_api_data(URI):
    api_request = requests.get(URI)
    api_list = json.loads(api_request.text)
    api_list == api_request.json()
    return api_list


def create_forecast_list(datetime_hours_from_now):
    weather_api_list = extract_json_api_data(WEATHER_REST_URI)
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


def fix_sensor_data(sensor_data_list):
    for element in sensor_data_list:
        # Fix inserted "T" in timestamp, remove whitespace from location, round temperature
        datetime_string_with_T = element['timestamp']
        datetime_string = datetime_string_with_T.replace('T', ' ')
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M:%S')
        location_string = element['location']
        if location_string.strip() == '':
            location_string_fixed = None
        else:
            location_string_fixed = location_string.strip()
        too_long_temperature = element['temperature']
        temperature_with_2_decimals = round(too_long_temperature, 2)
        # Create PiData object, with API data
        pidata_object = create_new_name('reading')
        pidata_object = PiData.create_pidata(element['id'], temperature_with_2_decimals,
                                             location_string_fixed, element['inDoor'],
                                             datetime_object)
        sensor_data_list.append(pidata_object)
    return sensor_data_list


def create_sensor_list(MAC_Address=None, datetime_start=datetime(2000, 1, 1), datetime_end=datetime(3000, 1, 1)):
    sensor_api_list = extract_json_api_data(SENSOR_REST_URI)
    pi_sensor_list = list()
    for element in sensor_api_list:
        # Fix inserted "T" in timestamp, remove whitespace from location, round temperature
        datetime_string_with_T = element['timestamp']
        datetime_string = datetime_string_with_T.replace('T', ' ')
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M:%S')
        location_string = element['location']
        if location_string.strip() == '':
            location_string_fixed = None
        else:
            location_string_fixed = location_string.strip()
        too_long_temperature = element['temperature']
        temperature_with_2_decimals = round(too_long_temperature, 2)
        # Create PiData object, with API data
        pidata_object = create_new_name('reading')
        pidata_object = PiData.create_pidata(element['id'], temperature_with_2_decimals,
                                             location_string_fixed, element['inDoor'],
                                             datetime_object)
        if MAC_Address != None:
            if pidata_object.id == MAC_Address and datetime_start <= datetime_object and datetime_end > datetime_object:
                pi_sensor_list.append(pidata_object)
        else:
            if datetime_start <= datetime_object and datetime_end > datetime_object:
                pi_sensor_list.append(pidata_object)
    return pi_sensor_list


def newest_outdoor_temperature():
    sensor_api_list = extract_json_api_data(SENSOR_REST_URI)
    pi_sensor_list = list()
    for element in sensor_api_list:
        # Fix inserted "T" in timestamp, remove whitespace from location, round temperature
        datetime_string_with_T = element['timestamp']
        datetime_string = datetime_string_with_T.replace('T', ' ')
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d %H:%M:%S')
        location_string = element['location']
        if location_string.strip() == '':
            location_string_fixed = None
        else:
            location_string_fixed = location_string.strip()
        too_long_temperature = element['temperature']
        temperature_with_2_decimals = round(too_long_temperature, 2)
        # Create PiData object, with API data
        pidata_object = create_new_name('reading')
        pidata_object = PiData.create_pidata(element['id'], temperature_with_2_decimals,
                                             location_string_fixed, element['inDoor'],
                                             datetime_object)
        if element['inDoor'] == False:
            pi_sensor_list.append(pidata_object)
        if len(pi_sensor_list) != 1:
            if pi_sensor_list[0].timestamp > pi_sensor_list[-1].timestamp:
                del pi_sensor_list[-1]
            if pi_sensor_list[0].timestamp < pi_sensor_list[-1].timestamp:
                pi_sensor_list.insert(
                    0, pi_sensor_list[-1])
    return pi_sensor_list[0]


def get_room(MAC_address):
    room_api_list = extract_json_api_data(ROOMS_REST_URI)
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


# print(PiData.__str__(newest_outdoor_temperature()))
test = create_sensor_list()
for element in test:
    print(PiData.__str__(element))
