from external_packages.GPS import l76x
from external_packages.GPS.micropyGPS import MicropyGPS

"""
Output Parameters:
Latitude Value (float)
Latitude Quadrant (int)
Longitude Vlaue (float)
Longitude Quadrant (int)
"""
def get_location():
    
    hemisphere_code = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    
    # GPS module setup code from datasheet: https://www.waveshare.com/wiki/Pico-GPS-L76B
    # define the UART number (default 0) and its baudrate (default 9600)
    UARTx = 0
    BAUDRATE = 9600

    # make an object of gnss device
    gnss_l76b=l76x.L76X(uartx=UARTx, _baudrate=BAUDRATE)

    # exit the backup mode when start
    gnss_l76b.l76x_exit_backup_mode()

    # enable/disable sync PPS when NMEA output (OPTIONAL)
    gnss_l76b.l76x_send_command(gnss_l76b.SET_SYNC_PPS_NMEA_ON)

    # make an object of NMEA0183 sentence parser
    # location_formatting (str)
    # Style For Presenting Longitude/Latitude: Decimal Degrees (dd) - 40.446° N
    # This object stores the longitude and latitude information!!!
    location = MicropyGPS(location_formatting='dd')

    # GPS needs warm up time, GPS until a valid location is received
    location_received = False
    while not location_received:
        if gnss_l76b.uart_any(): # make sure GPS module is getting connection
            # new data received from satellites
            new_char = chr(gnss_l76b.uart_receive_byte()[0])
            # parse the GPS signal and return the new data (or None if no data received)
            location_received = location.update(new_char)
            
            if location_received != None and location.valid != False:
                return location.latitude[0], hemisphere_code[location.latitude[1]], location.longitude[0], hemisphere_code[location.longitude[1]]
