from GetData import *
from Sensor import *


def suggested_new_temperature(forecast, indoor_sensor_data, global_optimal_temperature, minimum_room_temperature, maximum_room_temperature):
    # Average of forecast for X time
    if len(forecast) > 0:
        forecast_total = 0
        forecast_number_of_elements = 0
        for element in forecast:
            forecast_total += element.temperature
            forecast_number_of_elements += 1
        average_forecast_temperature = forecast_total / forecast_number_of_elements
    # Get current temp of Pi
    current_sensor_temp = get_sensor_temperature()
    # Current outdoor temp
    current_outdoor_temp = newest_outdoor_temperature()
    # Average of previous X time indoor sensor meassurement
    if len(indoor_sensor_data) > 0:
        indoor_total = 0
        indoor_number_of_elements = 0
        for element in indoor_sensor_data:
            indoor_total += element.temperature
            indoor_number_of_elements += 1
        average_indoor_temperature = indoor_total / indoor_number_of_elements

    temperature_to_set = 0
    return temperature_to_set
