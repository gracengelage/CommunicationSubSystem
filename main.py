
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

start_time = utime.time()
current_time = utime.time()

########################
# Receiver related setup
########################

# Create an instance of the Receiver class with GPIO27
# receiver = Receiver(27)

# Create an instance of the Transmitter class with GPIO17
transmitter = Transmitter(17)

###################
# GPS related setup
###################

# variable to store the GPS location string
location = None

################
# LED setup
################

# This LED represents the big light
LIGHT = machine.Pin(13, machine.Pin.OUT) # GP13
# LIGHT.direction = digitalio.Direction.OUTPUT

# This LED represents the indicator that a signal has been received
INDICATOR = machine.Pin(14, machine.Pin.OUT) # GP14
# INDICATOR.direction = digitalio.Direction.OUTPUT

##############
# Sensor Setup
##############

pir = machine.Pin(3, machine.Pin.IN)

#############
# State setup
#############

state = 0

# Initialise motion and communication signal
motion = 0
communication = 0

# need to keep track of when state 2 starts
wait_start_time = utime.time()

# UPDATE THIS to be based on user input? --------------------------------------------------------------
wait_duration = 5  # seconds for the sake of testing
range_meters = 50000  # TBD!!

# Determines if testing statement for communication signal should be printed
print_state = 0


while True:
    ##################
    # Transmitter Code 
    ##################

    motion = pir.value()
    if motion == 1:
        LIGHT.on()
        for i in range(8):
            transmitter.send_bit(0)
            utime.sleep(0.01)
        print("message sent.")

    utime.sleep(0.1)

    ##################
    # Receiver Code 
    ##################

    # update the current time every loop
    current_time = utime.time()

    # get location at the beginning or once 10 seconds for testing
    if location is None or current_time - start_time > 10:
        location = get_location()
        print(location)
        location = location_string(43.659388, 'N', 79.396534, 'W')
    
    motion_location = location_string(43.659460, 'N', 79.396551, 'W')

    distance = calculate_distance(motion_location, location)

    if not distance <= range_meters:
        communication = 0
    else:
        # flip the bit value as during transmission bit gets flipped
        # 1 means communication signal received, 0 means no communication signal
        if receiver.read_bit() == 0:
            communication = 1
        else:
            communication = 0


    state, wait_start_time = next_state(state, motion, communication, wait_start_time, wait_duration)

    ################
    # Big light
    ################
    # Light control
    if (state == 1 or state == 2):
        LIGHT.on()
        utime.sleep(0.5)
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

    print("Signal received:", receiver.read_bit)

    if receiver.read_bit() == 0 and print_state == 0:
        print("Positive radio signal is being recieved")
        print_state = 1
    if print_state == 1 and motion_location == 0:
        print_state = 0

    utime.sleep(0.1)  # Wait for 5 seconds every loop for debugging
