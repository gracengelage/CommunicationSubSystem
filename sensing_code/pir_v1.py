'''
PIR Sensor Code v1
Modified from ESC204 2024S Lab 5, Task E
Task: Take readings using a passive infrared sensor.
'''

import time
import board
import digitalio
# since the PIR sensor is all handled by the sensor and gives a digital output, no need for a library
# potentially needed for other sensors


# set up code constants:
useOnBoardLED = True
pollingRate = 0.1 #in seconds, LIKELY NEED TO CHANGE THIS ACROSS ALL CODE unless we run things in parallel
sensorPin = board.GP1   #! change for other pins if necessary
                        # data input pin for the PIR sensor
pir_value = pir.value #! the sensor returns a value of true or false
#? calibration for PIR is done physically by adjusting resistance in the circuit, not in code
#? will explore best calibration later if necessary
#? for now accept that 1 = motion detected, 0 = no motion detected in the code (no further post processing)


if useOnBoardLED:
    # Configure the internal GPIO connected to the LED as a digital output
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

# Set up digital input for PIR sensor:
pir = digitalio.DigitalInOut(sensorPin)
pir.direction = digitalio.Direction.INPUT


while True:
    # set LED value to match PIR sensor output
    pir_value = pir.value
    
    if useOnBoardLED:
        led.value = pir_value

    # plot PIR sensor output to serial
    if pir_value:
        print((1,))
    else:
        print((0.01,))

    time.sleep(pollingRate)
