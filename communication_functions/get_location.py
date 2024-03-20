import time

# Output Parameters:
# Location Information ~ a string representing the location of the device in degrees
#                      ~ "XXXYYYYYYYYDAAABBBBBBBBE"
#                      ~ 3 X's is first coordinate's integer part; if magnitude is less than 100,
#                        leftmost digits are filled with zero
#                      ~ 8 Y's are the decimals of the first coordinate
#                      ~ D denotes hemisphere of second coordinate (N = 0, E = 1, S = 2, W = 3)
#                      ~ 3 A's is the second coordinate's integer part (similar to X's)
#                      ~ 8 B's are the decimals of the second coordinate
#                      ~ E denotes hemisphere of second coordinate (N = 0, E = 1, S = 2, W = 3)
#                      ~ Example: 44.18273845N, 115.12345678W
<<<<<<< HEAD
#                      ~ "20441827384503115123456784"
def get_location() -> str:
    # GPS needs warm up time, GPS until a valid location is received
    location_received = False
=======
#                      ~ "044182738450115123456783"
def get_location(last_update=None):
    pass
>>>>>>> 3c3fb9015a1ca8f83bd791301a132e055ad6e0b4
