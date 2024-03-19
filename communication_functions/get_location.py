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
#                      ~ "044182738450115123456783"
def get_location(last_update=None):
    pass
