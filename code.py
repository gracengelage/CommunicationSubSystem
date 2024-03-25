
from external_packages.custom_rf.transmitter import Transmitter
from external_packages.custom_rf.receiver import Receiver
import utime
import machine
from communication_functions.get_location import get_location, location_string
from communication_functions.update_state import next_state
from communication_functions.calculate_distance import calculate_distance

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
# receiver.receive_message()

# Create an instance of the Transmitter class with GPIO17
# transmitter = Transmitter(17)

###################
# GPS related setup
###################

# variable to store the GPS location string
location = None

################
# LED setup
################

# This LED represents the big light
LIGHT = machine.Pin(17, machine.Pin.OUT) # GP13
# LIGHT.direction = digitalio.Direction.OUTPUT

# This LED represents the indicator that a signal has been received
INDICATOR = machine.Pin(19, machine.Pin.OUT) # GP14
# INDICATOR.direction = digitalio.Direction.OUTPUT

################
# State setup
################

state = 0

# Initialise motion and communication
motion = 0
communication = 0
location = None
# need to keep track of when state 2 starts
wait_start_time = 0
# UPDATE THIS to be based on user input? --------------------------------------------------------------
wait_duration = 1  # seconds for the sake of testing
range_meters = 50000  # TBD!!


while True:
    # update the current time every loop
    current_time = utime.ticks_ms()
    # print("start")
    # print("current time:", current_time)
    # print("start time:", start_time)

    # get location at the beginning or once 10 seconds for testing
    if location is None or utime.ticks_diff(current_time, start_time) / 1000 > 10:
        # location = get_location()
        # print(location)
        location = location_string(43.659388, 'N', 79.396534, 'W')
        # print("location:", location)

    bit = receiver.read_bit()
    if bit == 0:
        print(bit, end=' ')
    motion_location = location_string(43.659460, 'N', 79.396551, 'W')

    distance = calculate_distance(motion_location, location)
    communication = 1 if distance <= range_meters else 0

    # To simulate the end of night (and let the loop break)
    # if input("End (Y/N): ") == "Y":
        # break
    # ---------------------------------------------------------------------------------------------------

    state, wait_start_time = next_state(state, motion, communication, wait_start_time, wait_duration)

    ################
    # Big light
    ################
    # Light control
    if (state == 1 or state == 2) and bit == 0:
        print("Let there be light")
        LIGHT.on()
        utime.sleep(2)
    else:
        LIGHT.off()

    #################
    # Indicator LED
    #################
    # If a location is being received, light up
    if motion_location != 0:
        INDICATOR.on()
    else:
        INDICATOR.off()

    # Delay to avoid hogging the CPU
    # time.sleep(1)


    utime.sleep(0.1)  # Wait for 5 seconds every loop for debugging

