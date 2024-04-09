import ustruct as struct
import utime

def transmit(nrf,
             long,
             long_hemi,
             lat,
             lat_hemi,
             handshake=0):
    
    """
    When motion sensor light is detected in the current device, transmit function is activated.
    Function stops the radio frequency object from listening and receiving incoming signals and goes into transmit mode.
    If transmit message is sent from handshake protocol:
        CMP is True
    If transmit message is sent from lighting devices:
        CMP is False and location information is broadcasted to other devices


    Input Parameters:
    nrf: radio frequency object
    long, long_hemi,lat,lat_hemi: current location
    handshake: 0 (1 is for debugging purposes, which the transmit function does not do)

    Output Parameters:
    a signal is sent using radio frequency

    """

    nrf.stop_listening()
    
    send_pack = struct.pack("!dhdhi", lat, lat_hemi, long, long_hemi, handshake)

    # transmit data pack
    try:
        nrf.send(send_pack)
    except OSError:
            pass
    

    # do a brief delay
    utime.sleep_ms(15)

    # print out what is sent
    print("sending:", struct.unpack("!dhdhi", send_pack))

    # start listening again
    nrf.start_listening()
