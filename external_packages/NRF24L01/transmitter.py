import ustruct as struct
import utime

def transmit(nrf,
             long,
             long_hemi,
             lat,
             lat_hemi,
             handshake=0):
    
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
    
    utime.sleep(1)
    
