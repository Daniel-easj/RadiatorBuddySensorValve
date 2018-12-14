from Regulate import *
from Sensor import *


while True:
    #
    #
    # Logic related to UDP broadcast of sensor readings
    # Calls function to create JSON
    data = json_string()
    # Sends the JSON object as bytes
    socket.sendto(bytes(data, "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
    # Print the JSON object to console
    print(data)
    #
    #
    # Logic related to temperature regulation
    now = datetime.now()
    ten_hours_from_now = now + timedelta(hours=10)
    one_day_forecast_list = create_forecast_list(
        datetime_hours_from_now=ten_hours_from_now)

    this_room = get_room(get_MAC(ETHERNET_INTERFACE))
    global_optimal_temperature = this_room.optimalTemperature
    minimum_room_temperature = this_room.minTemperature
    maximum_room_temperature = this_room.maxTemperature
    print(this_room.minTemperature)
    print(this_room.optimalTemperature)
    print(this_room.maxTemperature)

    one_day_before_now = now + timedelta(hours=-24)
    pidata_list_one_day_old = create_sensor_list(
        datetime_start=one_day_before_now)

    pidata_objects_with_room_data = transfer_room_data_to_pidata_object(
        pidata_list_one_day_old)

    regulated_new_temperature = suggested_new_temperature(one_day_forecast_list, pidata_objects_with_room_data, global_optimal_temperature,
                                                          minimum_room_temperature, maximum_room_temperature, 3.0, 23.0)

    if regulated_new_temperature < 1:
        sense.show_message('No change')
    if regulated_new_temperature > 1:
        sense.show_message(str(round(regulated_new_temperature, 1)))
    time.sleep(15)
