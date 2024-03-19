from math import radians, sin, cos, sqrt, atan2

def loc_str2float(loc_str):
    """
    Convert a string of GPS location into tpules of floats containing angular coordinates

    Parameters:
    loc_str (str): String representation of the GPS location

    Returns:
    tuple: 
        - float: latitude of the first point (N is positive)
        - float: longtitude of the second point (E is positive)
    """

    # Extract angle coordinates (both integer and fractional part) and hemisphere information
    # from location string "XXXYYYYYYYYDAAABBBBBBBBE"
    coord1 = int(loc_str[0:11]) * 1e-8
    hem1 = int(loc_str[11])
    coord2 = int(loc_str[12:23]) * 1e-8
    hem2 = int(loc_str[23])

    # Convert the sign of the coordinates based on hemisphere
    # If the hemisphere are S or W
    coord1 *= -1 if hem1 in [2, 3] else 1
    coord2 *= -1 if hem2 in [2, 3] else 1

    # Return the north/south coordinates first then east/west
    if hem1 in [0, 2]:
        return (coord1, coord2)
    return (coord2, coord1)


def calculate_distance(sender_loc_str, receiver_loc_str) -> float:
    """
    Calculate the great circle distance between two points on the earth specified in decimal degrees and directions.

    Parameters:
    sender_loc_str (str): the GPS coordinate string of the signal sender
    receiver_loc_str (str): the GPS coordinate string of the signal receiver

    Returns:
    float: Distance between the two points in meters.
    """
    lat1, long1 = loc_str2float(sender_loc_str)
    lat2, long2 = loc_str2float(receiver_loc_str)

    return 1

if __name__ == "__main__":
    loc_str_1 = "044182738450115123456783"

    loc = loc_str2float(loc_str_1)
    print(loc)