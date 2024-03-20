from machine import Pin
import utime

class Transmitter:
    def __init__(self, data_pin) -> None:
        """
        Initializes the Transmitter with a specific GPIO pin.

        Paramters:
        data_pin (int): The GPIO pin number to which the transmitter's data line is connected.
        """
        self.data_pin = Pin(data_pin, Pin.OUT)
    
    def send_bit(self, bit) -> None:
        """
        Sends a single bit over the RF transmitter.
        This method sets the data pin to high or low based on the bit value, simulating the transmission of a single bit.

        Paramters:
        bit (int): The bit (0 or 1) to send.
        """
        self.data_pin.value(bit)
        utime.sleep(0.01)  # Adjust the bit duration as necessary

    def send_message(self, message) -> None:
        """
        Encodes and sends a message string over the RF transmitter.
        This method iterates over each character in the message, converts it to its binary representation, and sends each bit using the send_bit method. After each character, a pause is added to separate characters.

        Paramters:
        message (str): The string message to be sent.
        """
        for char in message:
            # ord(char) converts the character to its ASCII value (an integer).
            # bin(ord(char)) converts this integer to a binary string (e.g., '0b1100001' for 'a').
            # The [2:] slices the binary string to remove the '0b' prefix.
            # .zfill(8) ensures that the binary string is padded with zeros to make it 8 bits long, which is standard for ASCII characters.
            bit_string = bin(ord(char))[2:]
            padded_bit_string = '0' * (8 - len(bit_string)) + bit_string
            for bit in padded_bit_string:
                self.send_bit(int(bit))
            self.data_pin.value(0)  # Inter-character spacing
            utime.sleep(0.01)
        
        # Print a new line character at the end
        ending = '00001010' # binary rep of new line
        for bit in ending:
            self.send_bit(int(bit))
        self.data_pin.value(0)
        utime.sleep(0.01)
