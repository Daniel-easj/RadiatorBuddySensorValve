import GetData
from datetime import datetime, timedelta
import time

optimal_temperature = GetData.fake_temp(20, 25)
minimum_room_temperatur = optimal_temperature - 2
maximum_room_temp = optimal_temperature + 3

while (True):
    one_day_from_now = datetime.now() + timedelta(hours=24)
    pi_indoor = GetData.create_sensor_list()
    pi_outdoor = GetData.create_sensor_list()
    one_day_forecast_list = GetData.create_forecast_list(one_day_from_now)

    # Function to regulate temperature

    def regulate_temp(forecast, indoor_sensor_data, outdoor_sensor_data, global_optimal_temperature, minimum_room_temperatur, maximum_room_temp):
        temperature_to_set = 0
        return temperature_to_set

    # regulate_temp(one_day_forecast_list, TODO, TODO, optimal_temperature, minimum_room_temperatur, maximum_room_temp)

    time.sleep(300)
