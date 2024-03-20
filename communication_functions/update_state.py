import time
import board
import digitalio
from external_packages.custom_rf.receiver import Receiver
from communication_functions.get_location import get_location
from communication_functions.signal_transmission import receive_signal
from communication_functions.calculate_distance import calculate_distance

# This LED represents the big light
LIGHT = digitalio.DigitalInOut(board.GP23)
LIGHT.direction = digitalio.Direction.OUTPUT

# This LED represents the indicator that a signal has been recieved
INDICATOR = digitalio.DigitalInOut(board.GP24)
INDICATOR.direction = digitalio.Direction.OUTPUT


# State 0 - light is OFF
# State 1 - light is ON and needed
# State 2 - light is ON but not needed (waiting time)
# Initialise state
state = 0
print("state:", state)

# Initialise motion and communication
motion = 0
communication = 0
location = 0
# UPDATE THIS to be based on user input? --------------------------------------------------------------
range = 20 # meters TBD!!
# -----------------------------------------------------------------------------------------------------

# need to keep track of when state 2 starts
wait_start_time = 0
wait_duration = 10  # seconds for the sake of testing

# stopping the loop while testing
loop = True  # Changed to True

while loop:  # Simplified loop condition to while loop

    #CHECK THAT THIS WORKS!! ---------------------------------------------------------------------------
    #update location at 5pm every day
    if location == 0 or time.localtime() == "17:00:00":
        location = get_location()
    
    # motion is a terminal input for now
    motion = 1 if input("Motion detected? (0/1): ") == "1" else 0
    
    # detects incoming signal, checks if it's in range, updates accordingly
    motion_location = receive_signal(Receiver)
    distance = calculate_distance(motion_location, location)
    communication = 1 if distance <= range else 0
    #communication = 1 if input("Communication detected? (0/1): ") == "1" else 0
    
    # similates the end of the night
    if input("End (Y/N): ") == "Y":
        break
    # ---------------------------------------------------------------------------------------------------

    # Changing of States
    # State 0 until motion or communication is detected
    if state == 0:
        light = 0
        if communication == 1 or motion == 1:
            print("state changed to 1")
            state = 1

    # State 1 until motion and communication not detected
    if state == 1:
        light = 1
        if communication == 0 and motion == 0:
            wait_start_time = time.time()
            print("state changed to 2")
            state = 2

    # State 2 until enough time has passed, if another signal is detected, back to 1
    # The communication signal should be sent more frequently than the determined wait time
    if state == 2:
        light = 1
        if communication == 1 or motion == 1:
            print("state changed to 1")
            state = 1
        if time.time() - wait_start_time >= wait_duration:
            print("state changed to 0")
            state = 0
    

    #Light control
    if state == 1 or state == 2:
        LIGHT.value = True
    else:
        LIGHT.value = False

    # If a location is being recieved, light up
    if motion_location != 0:
        INDICATOR.value = True
    else:
        INDICATOR.value = False

    # Delay to avoid hogging the CPU
    time.sleep(1)  # Adjust sleep time as necessary
