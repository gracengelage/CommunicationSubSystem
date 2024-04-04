

import usys
import ustruct as struct
import utime
from machine import Pin, SPI, SoftSPI
from external_packages.NRF24L01.nrf24l01 import NRF24L01
from micropython import const

device = 2 # 0 , 1 , 2
CHANNEL = 125
sender =  True
PAYLOAD_SIZE = 32


# use button to trigger sending
button = machine.Pin(0, machine.Pin.IN)

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
nrf = NRF24L01(spi, csn, ce, payload_size= PAYLOAD_SIZE, channel = CHANNEL)

nrf.open_tx_pipe(pipes[device]) # send through your own pipe

# open the other pipes for receiving
other_pipes = [pipes[i] for i in range(3) if i != device]
for i, pipe in enumerate(other_pipes):
    nrf.open_rx_pipe(i, pipe)
    
nrf.start_listening()

def transmit(nrf,
             long,
             long_hemi,
             lat,
             lat_hemi,
             handshake=0):
    
    nrf.stop_listening()
    
    send_pack = struct.pack("!dhdhi", lat, lat_hemi, long, long_hemi, handshake)

    # transmit data pack
    nrf.send(send_pack)

    # do a brief delay
    utime.sleep_ms(15)

    # print out what is sent
    print("sending:", struct.unpack("!dhdhi", send_pack))

    # start listening again
    nrf.start_listening()

def receiver(nrf,
             current_lat,
             current_long,
             _RX_POLL_DELAY,
             ):
    
    nrf.start_listening()

    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            s_lat, s_lat_quad, s_lon, s_lon_quad, millis, handshake = struct.unpack("!dhdhi", buf)
            
            sender_lat = convert_coord(s_lat, s_lat_quad)
            sender_long = convert_coord(s_lon, s_lon_quad)

            print("received:", r_lat, r_lat_quad, r_lon, r_lon_quad)
            print("------------------------------------------------------------------")

            # the sender device is less than 10 meters away
            if calculate_distance(current_lat, current_long, sender_lat, sender_long) < 10:
                print("******************************")
                print("Close by device has been found")
                print("******************************")

                return True

            # the current device is not within 10 meters, proceed to parsing the other devices
            utime.sleep_ms(_RX_POLL_DELAY)
    
    # no device satisfies less than 10 meters requirement
    return False

        


while True:
    if button.value():
        nrf.stop_listening()
        millis = utime.ticks_ms()
        
        try:
            nrf.send(struct.pack("!dhdhi", 44.18273845, 0, 115.12345678, 3, millis))
        # each int is 4 bytes 
        except OSError:
            pass
        
        sent_pack = struct.pack("!dhdhi", 44.18273845, 0, 115.12345678, 3, millis)

        print("sending:", struct.unpack("!dhdhi", sent_pack))
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

        else:
            # recv packet
            buf = nrf.recv()
            (_, _, _, _, got_millis) = struct.unpack("!dhdhi", buf)

            # print response and round-trip delay
            print("delay: {} ms".format(utime.ticks_diff(utime.ticks_ms(), got_millis)))
            
            if sent_pack == buf:
                print("perfect transmission")
                utime.sleep(1)  
        # delay then loop
        utime.sleep_ms(25)
        
    # responder prototcol
    if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                r_lat, r_lat_quad, r_lon, r_lon_quad, millis = struct.unpack("!dhdhi", buf)
                print("received:", r_lat, r_lat_quad, r_lon, r_lon_quad)
                print("Formatted Number: {:.15f}".format(r_lat))
                print("Original sent:    {:.15f}".format(44.18273845))
                print("Formatted Number: {:.15f}".format(r_lon))
                print("Original sent:    {:.15f}".format(115.12345678))

                utime.sleep_ms(_RX_POLL_DELAY)

            # Give initiator time to get into receive mode.
            utime.sleep_ms(_RESPONDER_SEND_DELAY)
            nrf.stop_listening()
            try:
                nrf.send(buf)
                pass
            except OSError:
                pass
            print("sent response")
            nrf.start_listening()
            
