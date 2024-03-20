from external_packages.custom_rf.transmitter import Transmitter
from external_packages.custom_rf.receiver import Receiver
import utime
from communication_functions.get_location import get_location


# Create an instance of the Receiver class with GPIO27
receiver = Receiver(27)

# Call receive_message to start listening for messages
receiver.receive_message()


# Create an instance of the Transmitter class with GPIO17
transmitter = Transmitter(17)

while True:
    transmitter.send_message("sheep")
    utime.sleep(5)  # Wait for 5 seconds before sending the message again
