'''Modified from Official.py test code to better suit our praxis project'''

"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import usys
import ustruct as struct
import utime
from machine import Pin, SPI, SoftSPI
from nrf24l01 import NRF24L01
from micropython import const

#! Configurations
CHANNEL = 125   # 2.4 GHz channel + however many MHz (up to 125)
                # use wifi analyzer to find the best channel
PAYLOAD_SIZE = 32 # <= 32 Bytes
sender = True

# Responder pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)
# Responder pauses an additional _RESPONER_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) initiator time to get into receive mode. The
# initiator may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_RESPONDER_SEND_DELAY = const(10)

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
    spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4)) #! pinout here must be correct physically as well!!!
    cfg = {"spi": spi, "csn": 13, "ce": 17}
else:
    raise ValueError("Unsupported platform {}".format(usys.platform))

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
# ie. the last byte is the first byte transmitted
#! IMPORTANT: addresses must share the same MSBs, only the LSBs should be different
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0", b"\xf0\xf0\xf0\xf0\xf0")
#todo assign the addresses to specific picos so we can identify them



csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = cfg["spi"]

#1! define radio
nrf = NRF24L01(spi, csn, ce, payload_size= PAYLOAD_SIZE, channel = CHANNEL)

# open pipes
MODULE_ID = 0 # 0, 1, 2
OTHER_MODULES = [1, 2]

nrf.open_tx_pipe(pipes[MODULE_ID])
nrf.open_rx_pipe(1, pipes[OTHER_MODULES[0]])
nrf.open_rx_pipe(2, pipes[OTHER_MODULES[1]])
    
# GPS input    
latitude = 44.18273845
longitude = 115.12345678
latitude_hemisphere = 0
longitude_hemisphere = 3

# Sensor input
status = 1

# received inputs
r_lat_whole = 0
r_lat_decimals = 0
r_lat_hemishpere = 0
r_lon_whole = 0
r_lon_decimals = 0
r_lon_hemishpere = 0
r_status = 0
r_millis = 0 # to use if you want to calculate transmission time

# counters
num_successes = 0
num_failures = 0

while True:
    if status == 1:
        #sending logic
        lat_decimals = '{:.8f}'.format(latitude).split(".")[1][:8] # 4byte
        lon_decimals = '{:.8f}'.format(longitude).split(".")[1][:8] # 4byte
        lat_whole = '{:.8f}'.format(latitude).split(".")[0] # 2byte
        lon_whole = '{:.8f}'.format(longitude).split(".")[0] # 2byte
        
        # convert ALL to int/short
        lat_whole = int(lat_whole)
        lat_decimals = int(lat_decimals)
        lon_whole = int(lon_whole)
        lon_decimals = int(lon_decimals)

        status # 2byte (shorts)
        millis = utime.ticks_ms() # 4byte
        
        nrf.stop_listening()
        
        sent_pack = struct.pack("!hdhhdhhd",   lat_whole, lat_decimals, latitude_hemisphere, 
                                        lon_whole, lon_decimals, longitude_hemisphere,
                                        status, millis)
        
        print("sending:", struct.unpack("!hdhhdhhd", sent_pack))
        
        try:
            nrf.send(sent_pack)
        except OSError:
            pass
        
        #verify the sent pack logic
        # start listening again
        nrf.start_listening()

        # wait for response, with 250ms timeout
        start_time = utime.ticks_ms()
        timeout = False
        while not nrf.any() and not timeout:
            if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
                timeout = True

        if timeout:
            print("failed, response timed out")
            num_failures += 1

        else:
            # recv packet
            (_,_,_,_,_,_,_,got_millis) = struct.unpack("!hdhhdhhd", nrf.recv())

            # print response and round-trip delay
            print(
                "got response:",
                got_millis,
                "(delay",
                utime.ticks_diff(utime.ticks_ms(), got_millis),
                "ms)",
            )
            num_successes += 1
            if got_millis != millis:
                num_failures += 1

        # delay then loop
        utime.sleep_ms(25)
    # receiving logic
    nrf.start_listening()
    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            
            r_lat_whole, r_lat_decimals, r_lat_hemishpere,
            r_lon_whole, r_lon_decimals, r_lon_hemishpere,
            r_status, r_millis = struct.unpack("!hdhhdhhd", buf)
            
            print("received:", r_lat_whole, r_lat_decimals, r_lat_hemishpere,
                                r_lon_whole, r_lon_decimals, r_lon_hemishpere,
                                r_status, r_millis)
            
        #todo make it so you can check the pack you received is the correct one    
        # Give initiator time to get into receive mode.
            utime.sleep_ms(_RESPONDER_SEND_DELAY)
            nrf.stop_listening()
            try:
                nrf.send(buf)
            except OSError:
                pass
            print("sent response")
    
    utime.sleep_ms(25)
    # back to loop

        
        
        
    

