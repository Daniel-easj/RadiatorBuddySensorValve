from GetData import *
from Sensor import *


def suggested_new_temperature(forecast, list_of_sensor_data, global_optimal_temperature, minimum_room_temperature, maximum_room_temperature, sensitivity, temperature_if_none_set):
    new_temperature = 0
    # Average of forecast for X time
    forecast_average = average_temperature(forecast)
    # Get current temp of Pi
    current_sensor_temp = get_sensor_temperature()
    # newest_outdoor_temperature = find_newest_temperature(
    #     list_of_PiData_objects=list_of_sensor_data, indoor=False)

    outdoor_PiData_object_list = filter_indoor(sensor_list, indoor=False)
    outdoor_average = average_temperature(outdoor_PiData_object_list)

    indoor_PiData_object_list = filter_indoor(sensor_list, indoor=True)
    indoor_average = average_temperature(indoor_PiData_object_list)

    # Indoor temp correction (Temperature rises or falls rapidly)
    if (indoor_average - current_sensor_temp) > 1 and (indoor_average - current_sensor_temp) >= sensitivity:
        if minimum_room_temperature != 0:
            new_temperature = minimum_room_temperature
        if global_optimal_temperature != 0:
            new_temperature = global_optimal_temperature
    if (current_sensor_temp - indoor_average) > 1 and (current_sensor_temp - indoor_average) >= sensitivity:
        if minimum_room_temperature != 0:
            new_temperature = minimum_room_temperature
        if global_optimal_temperature != 0:
            new_temperature = global_optimal_temperature
    if maximum_room_temperature != 0 and (current_sensor_temp - indoor_average) > 1 and (current_sensor_temp - indoor_average) >= sensitivity and current_sensor_temp >= maximum_room_temperature:
        if minimum_room_temperature != 0:
            new_temperature = minimum_room_temperature
        else:
            new_temperature = temperature_if_none_set

        # Getting warmer outside than it has been
    if (forecast_average - outdoor_average) > 1 and (forecast_average - outdoor_average) >= sensitivity:
        # 000
        if minimum_room_temperature == 0 and global_optimal_temperature == 0 and maximum_room_temperature == 0:
            new_temperature = temperature_if_none_set
        # 111
        if minimum_room_temperature != 0 and global_optimal_temperature != 0 and maximum_room_temperature != 0:
            new_temperature = global_optimal_temperature

    # Getting colder outside than it has been
    if (outdoor_average - forecast_average) > 1 and (outdoor_average - forecast_average) >= sensitivity:
        # 000
        if minimum_room_temperature == 0 and global_optimal_temperature == 0 and maximum_room_temperature == 0:
            new_temperature = temperature_if_none_set
        # 111
        if minimum_room_temperature != 0 and global_optimal_temperature != 0 and maximum_room_temperature != 0:
            new_temperature = global_optimal_temperature

    return new_temperature
