from external_packages.rpi_rf.rpi_rf import RFDevice

# Input Parameters:
# location ~ a string of digits representing the coordinate of the device
#          ~ in the format NXXXYYYYYYYYYDMAAABBBBBBBBBE (More details in get location function)
# status ~ a single char - "1" or "0" - which denotes if motion signal is detected or not detected, respectively

# Output Parameters: NONE
def send_signal(location, status):

    # Enable the radio frequency transmitter; transmitter is connected to GPIO17
    rf_transmitter = RFDevice(17)
    rf_transmitter.enable_tx()

    # concatenate location and status and convert it into an encoded decimal value
    # FORMAT: (int) NX...BES, where N -> E encode for location info and S encodes for status info
    transmission_info = int(location + status)

    # Use the tx_code function in radio frequency transmitter
    # to broadcast the encoded location and status information.
    rf_transmitter.tx_code(code=transmission_info, tx_length=128)

    # Disable the transmitter device
    rf_transmitter.cleanup()
    

# Input Parameters:
# rf_receiver ~ the receiver device initiated in the main code.py file
    
# Output Parameters
# recevier code: a string "N...ES" that denotes the location of signal source and S denotes motion sensing status 
# (More details about N -> E location signal in get location section)
def receive_signal(rf_receiver) -> str:
    return str(rf_receiver.rx_code)