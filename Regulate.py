from GetData import *
from datetime import datetime, timedelta
import time
from Sensor import *


one_day_from_now = datetime.now() + timedelta(hours=24)
one_day_before_now = datetime.now() + timedelta(hours=-24)
this_room = get_room(get_MAC(ETHERNET_INTERFACE))


def regulate_temp(forecast, outdoor_sensor_data, global_optimal_temperature, minimum_room_temperature, maximum_room_temperature):
    # Average of forecast for X time
    total = 0
    number_of_elements = 0
    for element in forecast:
        total += element['main']['temp']
        number_of_elements += 1
    average = total / number_of_elements
    # Get current temp of Pi
    sensor_temp = get_sensor_temperature()

    temperature_to_set = 0
    return temperature_to_set


while (True):

    pi_indoor = create_sensor_list()
    pi_outdoor = create_sensor_list()
    one_day_forecast_list = create_forecast_list(one_day_from_now)
    global_optimal_temperature = this_room.optimalTemperature
    minimum_room_temperature = this_room.minTemperature
    maximum_room_temperature = this_room.maxTemperature
    # Function to regulate temperature

    regulate_temp(one_day_forecast_list, TODO, optimal_temperature,
                  minimum_room_temperatur, maximum_room_temp)

    time.sleep(300)
