from machine import Pin
import utime

class Receiver:
    def __init__(self, data_pin):
        """
        Initializes the Receiver with a specific GPIO pin.

        Paramters:
        data_pin (int): The GPIO pin number to which the receiver's data line is connected.
        """
        self.data_pin = Pin(data_pin, Pin.IN)

    def read_bit(self) -> int:
        """
        Reads a single bit from the RF receiver.
        This method reads the current value of the data pin, interpreting it as a bit.

        Return:
        (int): The bit read (0 or 1).
        """
        return self.data_pin.value()

    def receive_message(self):
        """
        Listens for and decodes a message from the RF receiver.
        This method continuously listens for data on the data pin, assembling received bits into characters and characters into a message. 
        The message is printed to the console once complete.
        Note: This is a blocking method that waits for data; need to consider using interrupts later
        """
        message = ''
        char_binary = ''
        while True:
            bit = self.read_bit()
            if bit is not None:
                char_binary += str(bit)
                if len(char_binary) == 8:  # Once we have 8 bits, we have a character
                    message += chr(int(char_binary, 2))
                    char_binary = ''  # Reset for the next character
                    if message[-1] == '\n':  # If the message ends with a newline, it's complete
                        print(message.strip())
                        message = ''  # Reset for the next message
            utime.sleep(0.01)  # Adjust based on the expected transmission rate
