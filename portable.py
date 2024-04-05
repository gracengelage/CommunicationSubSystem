import utime
import machine
from machine import Pin, SPI, SoftSPI
from micropython import const
import usys
from external_packages.NRF24L01.nrf24l01 import NRF24L01
from external_packages.NRF24L01.control_message import control_message

###############
# General Setup
###############

start_time = utime.time()
current_time = utime.time()

###################
# GPS related setup
###################

# variable to show if GPS location exists
has_location = True
latitude = 44.18273845
latitude_quad = 0
longitude = 115.12345678
longitude_quad = 3

#############
# Click Setup
#############

button = machine.Pin(0, machine.Pin.IN)

#######################
# Radio frequency Setup
#######################

CHANNEL = 125
PAYLOAD_SIZE = 32

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

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]
nrf = NRF24L01(spi, csn, ce, payload_size=PAYLOAD_SIZE, channel=CHANNEL)

nrf.open_tx_pipe(b"\xf3\xf0\xf0\xf0\xf0") # send through your own pipe

while True:
    
    ##################
    # Transmitter Code 
    ##################
    if button.value():
        while button.value():
            pass

        control_message(
            nrf=nrf,
            long=longitude,
            long_hemi=longitude_quad,
            lat=latitude,
            lat_hemi=latitude_quad
        )
    
        utime.sleep(0.15)  # Wait for 0.1 seconds every loop for debugging

