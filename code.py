"""
# demo.py
# Kevin McAleer
# test the nRF24L01 modules to send and receive data
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0

from nrf24l01 import NRF24L01
from machine import SPI, Pin
from time import sleep
import struct

csn = Pin(14, mode=Pin.OUT, value=1) # Chip Select Not
ce = Pin(17, mode=Pin.OUT, value=0)  # Chip Enable
led = Pin(25, Pin.OUT)               # Onboard LED
payload_size = 20

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

# role = "send"
role = "receive"

if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    print("Initialising the nRF24L0+ Module")
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=payload_size)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    return nrf

def flash_led(times:int=None):
    ''' Flashed the built in LED the number of times defined in the times parameter '''
    for _ in range(times):
        led.value(1)
        sleep(0.01)
        led.value(0)
        sleep(0.01)

def send(nrf, msg):
    print("sending message.", msg)
    nrf.stop_listening()
    for n in range(len(msg)):
        try:
            encoded_string = msg[n].encode()
            byte_array = bytearray(encoded_string)
            buf = struct.pack("s", byte_array)
            nrf.send(buf)
            # print(role,"message",msg[n],"sent")
            flash_led(1)
        except OSError:
            print(role,"Sorry message not sent")
    nrf.send("\n")
    nrf.start_listening()

# main code loop
flash_led(1)
nrf = setup()
nrf.start_listening()
msg_string = ""

while True:
    msg = ""
    if role == "send":
        send(nrf, "Yello world")
        send(nrf, "Test")
    else:
        # Check for Messages
        if nrf.any():
            package = nrf.recv()          
            message = struct.unpack("s",package)
            msg = message[0].decode()
            flash_led(1)

            # Check for the new line character
            if (msg == "\n") and (len(msg_string) <= 20):
                print("full message",msg_string, msg)
                msg_string = ""
            else:
                if len(msg_string) <= 20:
                    msg_string = msg_string + msg
                else:
                    msg_string = ""
"""

from external_packages.custom_rf.transmitter import Transmitter
from external_packages.custom_rf.receiver import Receiver
import utime
import machine
from communication_functions.get_location import get_location, location_string
from communication_functions.update_state import next_state
from communication_functions.calculate_distance import calculate_distance
from external_packages.nrf24l01test import nrf24l01test

nrf24l01test.master()


###############
# General Setup
###############

start_time = utime.ticks_ms()
current_time = utime.ticks_ms()

########################
# Receiver related setup
########################

# Create an instance of the Receiver class with GPIO27
receiver = Receiver(27)

# Call receive_message to start listening for messages
# receiver.receive_message()

# Create an instance of the Transmitter class with GPIO17
# transmitter = Transmitter(17)

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

################
# State setup
################

state = 0

# Initialise motion and communication
motion = 0
communication = 0
location = None
# need to keep track of when state 2 starts
wait_start_time = 0
# UPDATE THIS to be based on user input? --------------------------------------------------------------
wait_duration = 1  # seconds for the sake of testing
range_meters = 50000  # TBD!!




while True:
    # update the current time every loop
    current_time = utime.ticks_ms()
    # print("start")
    # print("current time:", current_time)
    # print("start time:", start_time)

    # get location at the beginning or once 10 seconds for testing
    if location is None or utime.ticks_diff(current_time, start_time) / 1000 > 10:
        location = get_location()
        print(location)
        # location = get_location()
        # print(location)
        location = location_string(43.659388, 'N', 79.396534, 'W')
        # print("location:", location)

    bit = receiver.read_bit()
    # if bit == 0:
    
    motion_location = location_string(43.659460, 'N', 79.396551, 'W')

    distance = calculate_distance(motion_location, location)
    communication = 1 if distance <= range_meters else 0

    # To simulate the end of night (and let the loop break)
    # if input("End (Y/N): ") == "Y":
        # break
    # ---------------------------------------------------------------------------------------------------

    state, wait_start_time = next_state(state, motion, communication, wait_start_time, wait_duration)

    ################
    # Big light
    ################
    # Light control
    if (state == 1 or state == 2) and bit == 0:
        # print(bit, end=' ')
        # print("Let there be light")
        LIGHT.on()
        utime.sleep(1)
        LIGHT.off()
    else:
        # print(bit, end=' ')
        # print("NO LIGHT")
        LIGHT.off()

    #################
    # Indicator LED
    #################
    # If a location is being received, light up
    if motion_location != 0:
        INDICATOR.on()
    else:
        INDICATOR.off()

    utime.sleep(0.1)  # Wait for 5 seconds every loop for debugging


