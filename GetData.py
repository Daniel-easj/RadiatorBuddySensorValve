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
    counter = 1
    return base_string + str(counter)


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
    final_list = list()
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
        final_list.append(pidata_object)
    return final_list


def create_sensor_list(MAC_Address=None, datetime_start=datetime(2000, 1, 1), datetime_end=datetime(3000, 1, 1)):
    sensor_api_list = extract_json_api_data(SENSOR_REST_URI)
    pi_sensor_list = list()
    fixed_sensor_list = fix_sensor_data(sensor_api_list)
    for entry in fixed_sensor_list:
        if MAC_Address != None:
            if entry.id == MAC_Address and datetime_start <= entry.timestamp and datetime_end > entry.timestamp:
                pi_sensor_list.append(entry)
        else:
            if datetime_start <= entry.timestamp and datetime_end > entry.timestamp:
                pi_sensor_list.append(entry)
    return pi_sensor_list


def filter_indoor(list_of_PiData_objects, indoor=False):
    if len(list_of_PiData_objects) != 0:
        sorting_list = list()
        for element in list_of_PiData_objects:
            if element.inDoor == indoor:
                sorting_list.append(element)
            if len(sorting_list) != 1 and len(sorting_list) != 0:
                if sorting_list[0].timestamp > sorting_list[-1].timestamp:
                    del sorting_list[-1]
                if sorting_list[0].timestamp < sorting_list[-1].timestamp:
                    # Move object on last index to first index
                    sorting_list.insert(
                        0, sorting_list[-1])
        if len(sorting_list) != 0:
            return sorting_list


def newest_temperature(list_of_PiData_objects):
    if len(list_of_PiData_objects) != 0:
        sorting_list = list()
        for element in list_of_PiData_objects:
            sorting_list.append(element)
            if len(sorting_list) != 1 and len(sorting_list) != 0:
                if sorting_list[0].timestamp > sorting_list[-1].timestamp:
                    del sorting_list[-1]
                if sorting_list[0].timestamp < sorting_list[-1].timestamp:
                    # Move object on last index to first index
                    sorting_list.insert(
                        0, sorting_list[-1])
        if len(sorting_list) != 0:
            return sorting_list[0].temperature


def average_temperature(list_of_objects):
    if len(list_of_objects) > 0:
        total = 0
        number_of_elements = 0
        for element in list_of_objects:
            total += element.temperature
            number_of_elements += 1
    return total / number_of_elements


def get_room(MAC_address):
    room_api_list = extract_json_api_data(ROOMS_REST_URI)
    for element in room_api_list:
        location_string = element['location']
        if location_string.strip() == '':
            location_string_fixed = None
        else:
            location_string_fixed = location_string.strip()
        if MAC_address == element['macAddress']:
            room_object = create_new_name('room')
            room_object = RoomData.create_roomdata(element['macAddress'], location_string_fixed, element['inDoor'],
                                                   element['optimalTemperature'], element['minTemperature'], element['maxTemperature'])
    return room_object


def get_all_rooms():
    room_api_list = extract_json_api_data(ROOMS_REST_URI)
    room_list = list()
    for element in room_api_list:
        location_string = element['location']
        if location_string.strip() == '':
            location_string_fixed = None
        else:
            location_string_fixed = location_string.strip()
        room_object = create_new_name('room')
        room_object = RoomData.create_roomdata(element['macAddress'], location_string_fixed, element['inDoor'],
                                               element['optimalTemperature'], element['minTemperature'], element['maxTemperature'])
        room_list.append(room_object)
    return room_list


def transfer_room_data_to_pidata_object(sensor_list):
    room_list = get_all_rooms()
    for sensor in sensor_list:
        for room in room_list:
            if sensor.id == room.macAddress:
                sensor.location = room.location
                sensor.inDoor = room.inDoor
    return sensor_list
