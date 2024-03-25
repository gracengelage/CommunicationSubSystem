
from external_packages.custom_rf.transmitter import Transmitter
from external_packages.custom_rf.receiver import Receiver
import utime
from communication_functions.get_location import get_location

###############
# General Setup
###############

start_time = utime.ticks_ms()
current_time = utime.ticks_ms()

########################
# Receiver related setup
########################

# Create an instance of the Receiver class with GPIO27
receiver = Receiver(27)

# Call receive_message to start listening for messages
receiver.receive_message()

# Create an instance of the Transmitter class with GPIO17
transmitter = Transmitter(17)

###################
# GPS related setup
###################

# variable to store the GPS location string
location = None

while True:
    # update the current time every loop
    current_time = utime.ticks_ms()

    # get location at the beginning or once 10 seconds for testing
    if location is None or utime.ticks_diff(current_time, start_time) / 1000 > 10:
        location = get_location()
        print(location)

    # transmitter sending signal
    transmitter.send_message("sheep")

    utime.sleep(5)  # Wait for 5 seconds every loop for debugging
