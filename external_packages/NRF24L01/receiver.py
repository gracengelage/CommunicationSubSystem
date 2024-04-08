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

    # nrf.start_listening() if you start listening again it will flush the buffer so don't do it here!!

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

            print("------------------------------------------------------------------")
            print("received:", s_lat, s_lat_quad, s_lon, s_lon_quad, handshake)
            print("------------------------------------------------------------------")
            
            distance = calculate_distance(current_lat, current_long, sender_lat, sender_long)

            # for communication testing
            if handshake == 1:
                print("**********************************")
                print("Control Message Protocol Activated")
                print("**********************************")
                
                # if valid an in range, you can flush the buffer
                nrf.flush_rx()
                
                return 2, 1
            
            # the sender device is less than 10 meters away
            if distance < 10:
                print("******************************")
                print("Close by device has been found")
                print("Distance: ", distance, "meters")
                print("******************************")

                # if valid an in range, you can flush the buffer
                nrf.flush_rx()
                
                # return has valid communication (in range) and has communication
                return 1, 1
            
            else:
                print("********************************")
                print("Signal is sent from far far away")
                print("Distance: ", distance, "meters")
                print("********************************")

            # the current device is not within 10 meters, proceed to parsing the other devices
            utime.sleep_ms(_RX_POLL_DELAY)
    
    # no device satisfies less than 10 meters requirement
    # return no valid_communication and maybe has communication signal
    # flush the buffer
    nrf.flush_rx()
    
    return 0, has_device