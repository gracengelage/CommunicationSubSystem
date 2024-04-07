import utime
import machine

# Function to measure distance
def measure_distance(trigger, echo):
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
    if abs(ref - cur) >= 7:
        return True
    return False