from GetData import *
from Sensor import *


def average_temperature(list_of_objects):
    if len(list_of_objects) > 0:
        total = 0
        number_of_elements = 0
        for element in list_of_objects:
            total += element.temperature
            number_of_elements += 1
    return total / number_of_elements


def suggested_new_temperature(forecast, indoor_sensor_data, global_optimal_temperature, minimum_room_temperature, maximum_room_temperature):
    new_temperature = 0
    temperature_adjustment = 0
    # Average of forecast for X time
    forecast_average = average_temperature(forecast)
    # Get current temp of Pi
    current_sensor_temp = get_sensor_temperature()
    # Current outdoor temp
    current_outdoor_temp = newest_outdoor_temperature()
    # Average of previous X time indoor sensor meassurement
    indoor_average = average_temperature(indoor_sensor_data)
    if forecast_average > current_sensor_temp:
        if minimum_room_temperature == 0:
            temperature_adjustment += 0
        if global_optimal_temperature > 0:
            temperature_adjustment += 0
    if forecast_average < current_sensor_temp:
        if (forecast_average - current_outdoor_temp) > 7:
            if minimum_room_temperature == 0:
                temperature_adjustment += 0
            if global_optimal_temperature == 0:
                temperature_adjustment += 0

    return new_temperature
