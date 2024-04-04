# demo.py
# Kevin McAleer
# test the nRF24L01 modules to send and receive data
# Watch this video for more information about that library https://www.youtube.com/watch?v=aP8rSN-1eT0

from nrf24l01 import NRF24L01
from machine import SPI, Pin
from time import sleep
import struct

csn = Pin(13, mode=Pin.OUT, value=1) # Chip Select Not
ce = Pin(17, mode=Pin.OUT, value=0)  # Chip Enable
led = Pin(25, Pin.OUT)               # Onboard LED
payload_size = 32

# Define the channel or 'pipes' the radios use.
# switch round the pipes depending if this is a sender or receiver pico

CHANNEL = 1
role = "send"
role = "receive"






if role == "send":
    send_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xd2\xf0\xf0\xf0\xf0"
else:
    send_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    receive_pipe = b"\xe1\xf0\xf0\xf0\xf0"

def setup():
    print("Initialising the nRF24L0+ Module")
    
    spi_sck=machine.Pin(6) #or whichever pin you're using for sck
    spi_mosi=machine.Pin(7) #or whichever pin you're using for mosi
    spi_miso=machine.Pin(4) #or whichever pin you're using for miso
    machine.SPI(0,baudrate=992063,sck=spi_sck, mosi=spi_mosi, miso=spi_miso)


    nrf = NRF24L01(SPI(0), csn, ce, payload_size=payload_size, channel = CHANNEL)
    nrf.open_tx_pipe(send_pipe)
    nrf.open_rx_pipe(1, receive_pipe)
    nrf.start_listening()
    
    print("initialized")
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
        send(nrf, "hello gordon")
    else:
        # Check for Messages
        if nrf.any():
            package = nrf.recv()          
        
            message = struct.unpack("s",package)
            good=False
            if message != (b'\x00',):
                good=True
            msg = message[0].decode()
            flash_led(1)
            
            if good:
                print(msg)
                good = False
        

            # Check for the new line character
            if (msg == "\n") and (len(msg_string) <= 20):
                print("full message",msg_string, msg)
                msg_string = ""
            else:
                if len(msg_string) <= 20:
                    msg_string = msg_string + msg
                else:
                    msg_string = ""

