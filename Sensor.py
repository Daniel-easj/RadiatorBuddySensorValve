from sense_hat import SenseHat
from datetime import *
from socket import *
import time
import json

# Create an object of the sensehat
sense = SenseHat()

# Port to broadcast to
BROADCAST_TO_PORT = 11912
# Interface name
ETHERNET_INTERFACE = 'wlan0'

# Function to get temperature


def get_sensor_temperature():
    return sense.get_temperature()

# Function to get MAC-address


def get_MAC(interface):
    # Return the MAC address of the specified interface
    try:
        mac_hex_string = open('/sys/class/net/%s/address' % interface).read()
    except:
        mac_hex_string = "00:00:00:00:00:00"
    return mac_hex_string[0:17]

# Function to create a JSON string


def json_string():
    # Get temperature
    temperature = get_sensor_temperature
    # Get current time
    now = datetime.now()
    # Put everything into a JSON string
    # Get Mac-address(Id) of the specific interface
    json_data = {"Id": get_MAC(ETHERNET_INTERFACE),
                 "Temperature": temperature,
                 # Format current time to the folllowing format
                 "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S")}
    # Return JSON object
    return json.dumps(json_data)


socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
