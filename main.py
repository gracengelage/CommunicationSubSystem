import utime
import machine
from machine import Pin, SPI, SoftSPI
from micropython import const
import usys
from external_packages.NRF24L01.nrf24l01 import NRF24L01
from external_packages.NRF24L01.transmitter import transmit
from external_packages.NRF24L01.receiver import receive
from communication_functions.get_location import get_location, location_string
from communication_functions.update_state import next_state
from communication_functions.calculate_distance import calculate_distance
from sensing_functions.ultrasonic import measure_distance, is_motion


###############
# General Setup
###############

start_time = utime.time()
current_time = utime.time()

########################
# Receiver related setup
########################

# Create an instance of the Receiver class with GPIO27
# receiver = Receiver(27)


###################
# GPS related setup
###################

# variable to show if GPS location exists
has_location = True
latitude = 44.18273845
latitude_quad = 0
longitude = 115.12345678
longitude_quad = 3

################
# LED setup
################

# This LED represents the big light
sensor_led = machine.Pin(12, machine.Pin.OUT)
network_led = machine.Pin(14, machine.Pin.OUT)
main_led = machine.Pin(15, machine.Pin.OUT)

##############
# Utrasonic Sensor Setup
##############

# Define GPIO pins for trigger and echo
trigger_pin = 9
echo_pin = 10

# Define LED pin
led_pin = 25

# Set up pins
trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
echo = machine.Pin(echo_pin, machine.Pin.IN)
send_signal = False

# Calibration reference
reference = 800

#############
# State setup
#############

state = 0

# Initialise motion and communication signal
motion = 0
has_comm = 0
valid_comm = 0

# need to keep track of when state 2 starts
wait_start_time = utime.time()

#######################
# Radio frequency Setup
#######################

device = 0# 0 , 1 , 2
CHANNEL = 125
sender =  True
PAYLOAD_SIZE = 32

# use button to trigger sending
button = machine.Pin(0, machine.Pin.IN)

if usys.platform == "pyboard":
    spi = SPI(2)  # miso : Y7, mosi : Y8, sck : Y6
    cfg = {"spi": spi, "csn": "Y5", "ce": "Y4"}
elif usys.platform == "esp8266":  # Hardware SPI
    spi = SPI(1)  # miso : 12, mosi : 13, sck : 14
    cfg = {"spi": spi, "csn": 4, "ce": 5}
elif usys.platform == "esp32":  # Software SPI
    spi = SoftSPI(sck=Pin(25), mosi=Pin(33), miso=Pin(32))
    cfg = {"spi": spi, "csn": 26, "ce": 27}
elif usys.platform == "rp2":  # Hardware SPI with explicit pin definitions
    spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
    cfg = {"spi": spi, "csn": 13, "ce": 17}
else:
    raise ValueError("Unsupported platform {}".format(usys.platform))


# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0", b"\xf0\xf0\xf0\xf0\xf0" )

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, payload_size=PAYLOAD_SIZE, channel=CHANNEL)

nrf.open_tx_pipe(pipes[device]) # send through your own pipe

# open the other pipes for receiving
other_pipes = [pipes[i] for i in range(3) if i != device]
for i, pipe in enumerate(other_pipes):
    nrf.open_rx_pipe(i, pipe)

nrf.start_listening()

#########################
# Ultrasonic Sensor Setup
#########################

trigger = machine.Pin(2, machine.Pin.OUT)
echo = machine.Pin(3, machine.Pin.IN)

# Calibration reference
reference = 800

send_signal = False

#################
# Debugging setup
#################

# Determines if testing statement for communication signal should be printed
print_state = 0

# UPDATE THIS to be based on user input? --------------------------------------------------------------
#wait_duration = int(input("Please set the wait duration in seconds: "))  # seconds for the sake of testing
wait_duration = 5 #seconds
range_meters = 50000  # TBD!!

while True:
    # update the current time every loop
    current_time = utime.time()
    
    ###################
    # Ultrasonic Sensor
    ###################
    # Measure distance
    real_dist = measure_distance(trigger, echo)
    print((real_dist, reference))

    # Check if distance is out of range
    if is_motion(reference, real_dist) == True:
        sensor_led.on()  # Turn on the LED
        motion = 1
    else:
        sensor_led.off()
        motion = 0

    # Update reference distance
    reference = real_dist

    ##################
    # Transmitter Code 
    ##################
    if motion==1 :
        transmit(
            nrf=nrf,
            long=longitude,
            long_hemi=longitude_quad,
            lat=latitude,
            lat_hemi=latitude_quad
        )

    ##################
    # Receiver Code 
    ##################

    # get location at the beginning or once 10 seconds for testing
    # if not has_location or current_time - start_time > 10:
    #     latitude, latitude_quad, longitude, longitude_quad = get_location()
    #     print("Location:", latitude, latitude_quad, longitude, longitude_quad)
    if motion == 0:
        valid_comm, has_comm = receive(nrf, c_lat=latitude, c_lat_quad=latitude_quad, c_long=longitude, c_long_quad=longitude_quad)

    state, wait_start_time = next_state(state, motion, valid_comm, wait_start_time, wait_duration)

    ################
    # Big light
    ################
    if (state == 1 or state == 2):
        main_led.on()

    else:
        main_led.off()

    ###################
    # Communication LED
    ###################
    if has_comm == 1:
        network_led.on()
    else:
        sensor_led.off()

    if valid_comm == 1 and print_state == 0:
        print("Correct radio signal is being recieved")
        print_state = 1
    if print_state == 1 and valid_comm == 1:
        print_state = 0

    
    
 
    
    utime.sleep(0.1)  # Wait for 0.1 seconds every loop for debugging

