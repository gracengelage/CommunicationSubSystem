from external_packages.GPS import l76x
from external_packages.GPS.micropyGPS import MicropyGPS

def location_string(latitude_val,
                    latitude_hemisphere,
                    longitude_val,
                    longitude_hemisphere) -> str:
    """
    Input Parameters:
    Latitude ~ the latitude value as a decimal number
    Longitude ~ the longitude value as a decimal number

    Output Parameters:
    Output Parameters:
    Location Information ~ a string representing the location of the device in degrees
                         ~ "XXXYYYYYYYYDAAABBBBBBBBE"
                         ~ 3 X's is latitude's integer part; if magnitude is less than 100,
                           leftmost digits are filled with zero
                         ~ 8 Y's are the decimals of the latitude
                         ~ D denotes hemisphere of latitude (N = 0, E = 1, S = 2, W = 3)
                         ~ 3 A's is the longitude's integer part (similar to X's)
                         ~ 8 B's are the decimals of the longitude
                         ~ E denotes hemisphere of longitude (N = 0, E = 1, S = 2, W = 3)
                         ~ Example: 44.18273845N, 115.12345678W
                         ~ "044182738450115123456783"
    """

    # convert latitude value into a string and
    # split latitude value into integer part and the 8 decimals that follow
    latitude_int, latitude_dec = '{:.8f}'.format(latitude_val).split(".")[0], '{:.8f}'.format(latitude_val).split(".")[1][:8]

    # convert longitude value into a string and
    # split longitude value into integer part and the 8 decimals that follow
    longitude_int, longitude_dec = '{:.8f}'.format(longitude_val).split(".")[0], '{:.8f}'.format(longitude_val).split(".")[1][:8]

    # convert North, East, South, West into numerical representations
    hemisphere_code = {
        "N": "0",
        "E": "1",
        "S": "2",
        "W": "3"
    }

    return ''.join(["0" * (3 - len(latitude_int)),
                    latitude_int,
                    latitude_dec,
                    "0" * (8 - len(latitude_dec)),
                    hemisphere_code[latitude_hemisphere],
                    "0" * (3 - len(longitude_int)),
                    longitude_int,
                    latitude_dec,
                    "0" * (8 - len(longitude_dec)),
                    hemisphere_code[longitude_hemisphere]])

# Output Parameters:
# Location Information ~ the location string as detailed in the location_string function output
def get_location() -> str:
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

            if location_received and location.valid:
                return location.latitude[0], location.latitude[1], location.longitude[0], location.latitude[1]