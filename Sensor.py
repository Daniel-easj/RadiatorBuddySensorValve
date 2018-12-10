from sense_hat import SenseHat
from datetime import *
from socket import *
import time as t
import json
import uuid

# Create an object of the sensehat
sense = SenseHat()

# Port to broadcast to
BROADCAST_TO_PORT = 11912

ETHERNET_INTERFACE = 'wlan0'

# Function to get MAC-address


def getMAC(interface):
    # Return the MAC address of the specified interface
    try:
        mac_hex_string = open('/sys/class/net/%s/address' % interface).read()
    except:
        mac_hex_string = "00:00:00:00:00:00"
    return mac_hex_string[0:17]

# Function to create a JSON string


def json_string():
        # Get temperature
    temperature = sense.get_temperature()
    # Get current time
    now = datetime.now()
    # Put everything into a JSON string
    # Get Mac-address(Id), convert to hexcode, then lastly to string
    json_data = {"Id": getMAC(ETHERNET_INTERFACE),
                 "Temperature": temperature,
                 # Format current time to the folllowing format
                 "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S")}
    # Return JSON object
    return json.dumps(json_data)


socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# Infinite loop
while True:
    # Calls function to convert to JSON
    data = json_string()
    # Sends the JSON object as bytes
    socket.sendto(bytes(data, "UTF-8"), ('<broadcast>', BROADCAST_TO_PORT))
    # Print the JSON object to console
    print(data)
    # Wait 30 seconds
    t.sleep(30)
