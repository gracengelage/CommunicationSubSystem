from external_packages.rpi_rf.rpi_rf import RFDevice

# Input Parameters:
# location ~ a string of digits representing the coordinate of the device
# status ~ a single char - "1" or "0" - which denotes if motion signal is detected or not detected, respectively

# Output Parameters: NONE
def send_signal(location, status):

    # Enable the radio frequency transmitter; transmitter is connected to GPIO17
    rf_transmitter = RFDevice(17)
    rf_transmitter.enable_tx()

    # concatenate location and status and convert it into an encoded decimal value
    # FORMAT: (int) XXXXXXXXS, where X's encode for location info and S encodes for status info
    transmission_info = int(location + status)

    # Use the tx_code function in radio frequency transmitter
    # to broadcast the encoded location and status information.
    rf_transmitter.tx_code(transmission_info)

    # Disable the transmitter device
    rf_transmitter.cleanup()
    

# Input Parameters:
# rf_receiver ~ the receiver device initiated in the main code.py file
    
# Output Parameters
# recevier code: a string "XXXXXXS",
# where X's denote location of signal source and S denotes motion sensing status of signal source
def receive_signal(rf_receiver):
    return str(rf_receiver.rx_code)