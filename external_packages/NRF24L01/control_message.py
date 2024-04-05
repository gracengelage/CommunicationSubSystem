import ustruct as struct
import utime

def control_message(nrf,
             long,
             long_hemi,
             lat,
             lat_hemi):
    
    send_pack = struct.pack("!dhdhi", lat, lat_hemi, long, long_hemi, 1)

    # transmit data pack
    try:
        nrf.send(send_pack)
    except OSError:
            pass

    # print out what is sent
    print("sending:", struct.unpack("!dhdhi", send_pack))

