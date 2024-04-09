import utime
import machine

# Function to measure distance
def measure_distance(trigger, echo):
    """
    The function takes in the trigger and echo pins of the circuit and measures the distance of the closest object in the sensor’s field of view 

    Input Parameters:
    trigger: pin
    echo: pin

    Output Parameter:
    distance: distance of closest object in field of view (in cm)
    """

    # Send trigger pulse
    trigger.on()
    utime.sleep(0.1)
    trigger.off()

    # Measure pulse duration
    pulse_duration = machine.time_pulse_us(echo, 1)
    # Calculate distance in centimeters
    distance = pulse_duration * 0.034 / 2
    
    return distance

def is_motion(ref, cur):
    """
    Takes in the current measured distance and compares it to a reference distance to determine if there is an object in motion

    Input Parameters:
    ref: reference distance
    cur: current measured distance

    Output Parameters:
    motion: True if motion, False if no motion
    """

    if abs(ref - cur) >= 7:
        return True
    return False