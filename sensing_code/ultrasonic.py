# ultrasonic sensor code
# not being used currently
# this one is carbon copy of the ultrasonic.py code from LAb 3

'''
ESC204 2024S Lab 3, Task G
Task: Calibrate an ultrasonic sensor.
'''

import time
import board
import adafruit_hcsr04
import digitalio

#set up LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up the ultrasonic sensor using a library
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP2, echo_pin=board.GP3)

# Take readings and output calibrated values
while True:
    try:
        # Take a reading (no button needed) of the range
        X = sonar.distance

        # Use calibration data to adjust this value
        real_dist = 1.084*(X-9.044)+10
        print((real_dist,))

        if(real_dist<=100): #in centimeters
            led.value = 1;
        else:
            led.value = 0;

    except RuntimeError:
        print("Retrying!")

    time.sleep(0.1)
