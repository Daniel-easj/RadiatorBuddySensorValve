class RoomData:
    def __init__(self, macAddress, location, inDoor, optimalTemperature, minTemperature, maxTemperature):
        self.macAddress = macAddress
        self.location = location
        self.inDoor = inDoor
        self.optimalTemperature = optimalTemperature
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature


def create_roomdata(macAddress, location, inDoor, optimalTemperature, minTemperature, maxTemperature):
    room_data = RoomData(macAddress, location, inDoor,
                         optimalTemperature, minTemperature, maxTemperature)
    return room_data
