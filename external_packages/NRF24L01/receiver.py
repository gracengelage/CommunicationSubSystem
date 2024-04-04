from communication_functions.calculate_distance import convert_coord, calculate_distance
import ustruct as struct
import utime

def receive(nrf,
             c_lat,
             c_lat_quad,
             c_long,
             c_long_quad,
             ):
    _RX_POLL_DELAY = 15

    # this keeps track of whether or not the device receive any signal, regardless of in range or not
    has_device = 0

    if nrf.any():
        while nrf.any():
            has_device = 1
            buf = nrf.recv()
            s_lat, s_lat_quad, s_lon, s_lon_quad, handshake = struct.unpack("!dhdhi", buf)
            
            current_lat = convert_coord(c_lat, c_lat_quad)
            current_long = convert_coord(c_long, c_long_quad)

            sender_lat = convert_coord(s_lat, s_lat_quad)
            sender_long = convert_coord(s_lon, s_lon_quad)

            print("received:", s_lat, s_lat_quad, s_lon, s_lon_quad, handshake)
            print("------------------------------------------------------------------")

            # the sender device is less than 10 meters away
            if calculate_distance(current_lat, current_long, sender_lat, sender_long) < 10:
                print("******************************")
                print("Close by device has been found")
                print("******************************")

                # return has valid communication (in range) and has communication
                return 1, 1
            
            else:
                print("********************************")
                print("Signal is sent from far far away")
                print("********************************")

            # the current device is not within 10 meters, proceed to parsing the other devices
            utime.sleep_ms(_RX_POLL_DELAY)
    
    # no device satisfies less than 10 meters requirement
    # return no valid_communication and maybe has communication signal
    return 0, has_device