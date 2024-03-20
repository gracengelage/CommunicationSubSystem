
from external_packages.custom_rf.transmitter import Transmitter
from external_packages.custom_rf.receiver import Receiver
import utime
from communication_functions.get_location import get_location

while True:
    transmitter.send_message("sheep")
    utime.sleep(5)  # Wait for 5 seconds before sending the message again

