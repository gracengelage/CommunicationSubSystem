
import time
import machine

# Define GPIO pins for trigger and echo
trigger_pin = 2
echo_pin = 3

# Set up pins
trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
echo = machine.Pin(echo_pin, machine.Pin.IN)
led = machine.Pin(led_pin, machine.Pin.OUT)
send_signal = False

# Function to measure distance
def measure_distance(trigger, echo):
    # Send trigger pulse
    trigger.on()
    time.sleep_us(10)
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
