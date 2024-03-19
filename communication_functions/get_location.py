# Output Parameters:
# Location Information ~ a string representing the location of the device in degrees
#                      ~ "NXXXYYYYYYYYDMAAABBBBBBBBE"
#                      ~ N is magnitude of first coordinate (ones - 1, tens - 2, hundreds - 3)
#                      ~ 3 X's is first coordinate excluding decimals; if magnitude is less than 100,
#                        rightmost digits are filled with zero
#                      ~ 8 Y's are the decimals of the first coordinate
#                      ~ D denotes hemisphere of second coordinate (N = 0, E = 1, S = 2, W = 4)
#                      ~ M is magnitude of second coordinate
#                      ~ 3 A's is the second coordinate excluding decimals (similar to X's)
#                      ~ 8 B's are the decimals of the second coordinate
#                      ~ E denotes hemisphere of second coordinate (N = 0, E = 1, S = 2, W = 4)
#                      ~ Example: 44.18273845N, 115.12345678W
#                      ~ "20441827384503115123456784"
def get_location(last_update=None):
    pass
