#https://docs.python.org/3/library/struct.html


# we can send 32 byte payloads
# want to send a 20 digit unsigned int

import struct

# 20 digit unsigned int
value = 12345678901234567890
# pack it into a 4 byte string
packed = struct.pack("P", value)

unpacked = struct.unpack("P", packed)

print(value)
print(unpacked)