import time

# State 0 - light is OFF
# State 1 - light is ON and needed
# State 2 - light is ON but not needed (waiting time)
# Initialise state
state = 0
print("state:", state)

# Initialise motion and communication
motion = 0
communication = 0

# need to keep track of when state 2 starts
wait_start_time = 0
wait_duration = 10  # seconds for the sake of testing

# stopping the loop while testing
loop = True  # Changed to True

while loop:  # Simplified loop condition to while loop

    # Update motion and communication (terminal inputs for now)
    motion = 1 if input("Motion detected? (0/1): ") == "1" else 0
    communication = 1 if input("Communication detected? (0/1): ") == "1" else 0
    
    if input("End (Y/N): ") == "Y":
        break

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

    # Delay to avoid hogging the CPU
    time.sleep(1)  # Adjust sleep time as necessary
