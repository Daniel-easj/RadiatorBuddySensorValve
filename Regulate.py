from GetData import *
from datetime import datetime, timedelta
import time
from Sensor import *


this_room = get_room(get_MAC(ETHERNET_INTERFACE))


def regulate_temp(forecast, indoor_sensor_data, outdoor_sensor_data, global_optimal_temperature, minimum_room_temperature, maximum_room_temperature):
    # Average of forecast for X time
    forecast_total = 0
    forecast_number_of_elements = 0
    for element in forecast:
        total += element.temperature
        number_of_elements += 1
    average_forecast = total / number_of_elements
    # Get current temp of Pi
    current_sensor_temp = get_sensor_temperature()
    # Current outdoor temp

    # Average of previous X time indoor sensor meassurement
    indoor_total = 0
    indoor_number_of_elements = 0
    for 
    temperature_to_set = 0
    return temperature_to_set


while (True):
    now = datetime.now()
    ten_hours_from_now = now + timedelta(hours=10)
    one_day_before_now = now + timedelta(hours=-24)
    one_day_forecast_list = create_forecast_list(
        datetime_hours_from_now=ten_hours_from_now)
    global_optimal_temperature = this_room.optimalTemperature
    minimum_room_temperature = this_room.minTemperature
    maximum_room_temperature = this_room.maxTemperature
    indoor_pidata_list_one_day_old = create_sensor_list(
        datetime_start=one_day_before_now)
    # Function to regulate temperature

    regulate_temp(one_day_forecast_list, indoor_pidata_list_one_day_old, TODO, global_optimal_temperature,
                  minimum_room_temperature, maximum_room_temperature)

    time.sleep(300)
