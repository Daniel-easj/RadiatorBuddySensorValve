class PiData:
    def __init__(self, id, temperature, location, inDoor, timestamp):
        self.id = id
        self.temperature = temperature
        self.location = location
        self.inDoor = inDoor
        self.timestamp = timestamp

# Function to initialize PiData objects


def create_pidata(id, temperature, location, inDoor, timestamp):
    pidata = PiData(id, temperature, location, inDoor, timestamp)
    return pidata

# Function to display data from PiData object in string format


def __str__(self):
    return (f"MAC-address : {self.id}, temperature : {self.temperature}, location : {self.location}, indoor : {self.inDoor}, timestamp : {self.timestamp}")
