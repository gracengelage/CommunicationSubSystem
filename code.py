import time
# import board
# import digitalio
from communication_functions.get_location import get_location

from external_packages.rpi_rf.rpi_rf import RFDevice

rfdevice = RFDevice(17)
rfdevice.enable_rx()

while True:
    receive_signal(rfdevice) 
