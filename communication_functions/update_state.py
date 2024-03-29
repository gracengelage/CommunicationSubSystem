import utime


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
def next_state(current_state, motion, communication, wait_start_time, wait_duration):
    if current_state == 0:
        if communication == 1 or motion == 1:
            print("State changed to 1")
            return 1, wait_start_time
    elif current_state == 1:
        if communication == 0 and motion == 0:
            wait_start_time = utime.time()
            print("State changed to 2")
            return 2, wait_start_time
    elif current_state == 2:
        if communication == 1 or motion == 1:
            print("State changed to 1")
            return 1, wait_start_time
        elif utime.time() - wait_start_time >= wait_duration:
            print("State changed to 0")
            return 0, wait_start_time
    return current_state, wait_start_time
