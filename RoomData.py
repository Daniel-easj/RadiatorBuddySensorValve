class RoomData:
    def __init__(self, macAddress, location, inDoor, optimalTemperature, minTemperature, maxTemperature):
        self.macAddress = macAddress
        self.location = location
        self.inDoor = inDoor
        self.optimalTemperature = optimalTemperature
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature

# Function to initialize WeatherData objects


def create_roomdata(macAddress, location, inDoor, optimalTemperature, minTemperature, maxTemperature):
    room_data = RoomData(macAddress, location, inDoor,
                         optimalTemperature, minTemperature, maxTemperature)
    return room_data

# Function to display data from WeatherData object in string format


def __str__(self):
    return (f"MAC-Address : {self.macAddress}, location : {self.location}, indoor : {self.inDoor}, optimal temperatur : {self.optimalTemperature}, minimum temperatur : {self.minTemperature}, maximum temperature : {self.maxTemperature}")
