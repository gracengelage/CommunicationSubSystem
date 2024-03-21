import time
import board
import digitalio
from external_packages.custom_rf.receiver import Receiver
from communication_functions.get_location import get_location
from communication_functions.signal_transmission import receive_signal
from communication_functions.calculate_distance import calculate_distance

#######################
# next_state function
####################### 
# outputs are:  current state (0,1 or 2)
#               wait_start_time (from time.time()) which tells the time that state 2 started
# inputs are:   current state (0,1 or 2)
#               motion (0, 1) 1 if motion is detected, otherwise 0
#               communication (0,1) 1 if communication is detected in range, otherwise 0
#               wait_start_time (from time.time()) which tells the time that state 2 started
#               wait_duration (in seconds) how long the light should stay on once there is no motion detected in range
#               
def next_state(current_state, motion, communication, wait_start_time, wait_duration):
    if current_state == 0:
        if communication == 1 or motion == 1:
            print("State changed to 1")
            return 1, wait_start_time
    elif current_state == 1:
        if communication == 0 and motion == 0:
            wait_start_time = time.time()
            print("State changed to 2")
            return 2, wait_start_time
    elif current_state == 2:
        if communication == 1 or motion == 1:
            print("State changed to 1")
            return 1, wait_start_time
        elif time.time() - wait_start_time >= wait_duration:
            print("State changed to 0")
            return 0, wait_start_time
    return current_state, wait_start_time

################
# LED setup
################

# This LED represents the big light
LIGHT = digitalio.DigitalInOut(board.GP23)
LIGHT.direction = digitalio.Direction.OUTPUT

# This LED represents the indicator that a signal has been received
INDICATOR = digitalio.DigitalInOut(board.GP24)
INDICATOR.direction = digitalio.Direction.OUTPUT

################
# State setup
################

state = 0

# Initialise motion and communication
motion = 0
communication = 0
location = 0
# need to keep track of when state 2 starts
wait_start_time = 0
# UPDATE THIS to be based on user input? --------------------------------------------------------------
wait_duration = 10  # seconds for the sake of testing
range_meters = 20  # TBD!!
# -----------------------------------------------------------------------------------------------------

while True:

    ######################################
    # Variables that influence the state
    ######################################
    # CHECK THAT THIS WORKS!! ---------------------------------------------------------------------------
    # Update location at 5 pm every day
    if location == 0 or time.localtime() == "17:00:00":
        location = get_location()

    # Motion is a terminal input for now 
    motion = 1 if input("Motion detected? (0/1): ") == "1" else 0
    #communication = 1 if input("Communication detected? (0/1): ") == "1" else 0

    # Detect incoming signal, check if it's in range, and update accordingly
    motion_location = receive_signal(Receiver(27))
    distance = calculate_distance(motion_location, location)
    communication = 1 if distance <= range_meters else 0

    # To simulate the end of night (and let the loop break)
    if input("End (Y/N): ") == "Y":
        break
    # ---------------------------------------------------------------------------------------------------

    state, wait_start_time = next_state(state, motion, communication, wait_start_time, wait_duration)

    ################
    # Big light
    ################
    # Light control
    if state == 1 or state == 2:
        LIGHT.value = True
    else:
        LIGHT.value = False

    #################
    # Indicator LED
    #################
    # If a location is being received, light up
    if motion_location != 0:
        INDICATOR.value = True
    else:
        INDICATOR.value = False

    # Delay to avoid hogging the CPU
    time.sleep(1)
