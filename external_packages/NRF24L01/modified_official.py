"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import usys
import ustruct as struct
import utime
from machine import Pin, SPI, SoftSPI
from nrf24l01 import NRF24L01
from micropython import const

def initiator(cfg, spi, CHANNEL, PAYLOAD_SIZE, pipes):
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size= PAYLOAD_SIZE, channel = CHANNEL)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.open_rx_pipe(2, pipes[2])
    nrf.start_listening()

    num_needed = 1
    num_successes = 0
    num_failures = 0
    led_state = 0

    print("NRF24L01 initiator mode, sending %d packets..." % num_needed)

    while num_successes < num_needed and num_failures < num_needed:
        # stop listening and send packet
        nrf.stop_listening()
        millis = utime.ticks_ms()
        led_state = max(1, (led_state << 1) & 0x0F)
        
        try:
            nrf.send(struct.pack("!dhdhi", 44.18273845, 0, 115.12345678, 3, millis)) # each int is 4 bytes 
        except OSError:
            pass

        print("sending:", struct.unpack("!dhdh", struct.pack("!dhdhi", 44.18273845, 0, 115.12345678, 3, millis)))
        

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
            (_, _, _, _, got_millis) = struct.unpack("!dhdhi", nrf.recv())

            # print response and round-trip delay
            print(
                "got response:",
                got_millis,
                "(delay",
                utime.ticks_diff(utime.ticks_ms(), got_millis),
                "ms)",
            )
            num_successes += 1
            

        # delay then loop
        utime.sleep_ms(25)

    print("initiator finished sending; successes=%d, failures=%d" % (num_successes, num_failures))


def responder(cfg, PAYLOAD_SIZE, CHANNEL, pipes, _RX_POLL_DELAY, _RESPONDER_SEND_DELAY):
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1, pull = Pin.PULL_UP)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size= PAYLOAD_SIZE, channel = CHANNEL)

    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.open_rx_pipe(2, pipes[2])
    nrf.start_listening()

    print("NRF24L01 responder mode, waiting for packets... (ctrl-C to stop)")

    if nrf.any():
        while nrf.any():
            buf = nrf.recv()
            millis, led_state, long, la, _ = struct.unpack("!dhdhi", buf)
            print("received:", millis, led_state, long, la)
            print("Formatted Number: {:.15f}".format(millis))
            print("Original sent:    {:.15f}".format(44.18273845))
            print("Formatted Number: {:.15f}".format(long))
            print("Original sent:    {:.15f}".format(115.12345678))
            for led in leds:
                if led_state & 1:
                    led.on()
                else:
                    led.off()
                led_state >>= 1
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


try:
    import pyb

    leds = [pyb.LED(i + 1) for i in range(4)]
except:
    leds = []

