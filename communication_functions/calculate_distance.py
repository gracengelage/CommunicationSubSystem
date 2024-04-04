from math import radians, sin, cos, sqrt, asin, pi, abs

# def loc_str2float(loc_str) -> tuple:
#     """
#     Convert a string of GPS location into tpules of floats containing angular coordinates

#     Parameters:
#     loc_str (str): String representation of the GPS location

#     Returns:
#     tuple: 
#         - float: latitude of the first point (N is positive)
#         - float: longtitude of the second point (E is positive)
#     """

#     # Extract angle coordinates (both integer and fractional part) and hemisphere information
#     # from location string "XXXYYYYYYYYDAAABBBBBBBBE"
#     coord1 = int(loc_str[0:11]) * 1e-8
#     hem1 = int(loc_str[11])
#     coord2 = int(loc_str[12:23]) * 1e-8
#     hem2 = int(loc_str[23])

#     # Convert the sign of the coordinates based on hemisphere
#     # If the hemisphere are S or W
#     coord1 *= -1 if hem1 in [2, 3] else 1
#     coord2 *= -1 if hem2 in [2, 3] else 1

#     # Return the north/south coordinates first then east/west
#     if hem1 in [0, 2]:
#         return (coord1, coord2)
#     return (coord2, coord1)

def haversine(theta) -> float:
    """ 
    Helper function for computing the haversine of an angle

    Parameter:
    theta (float): angle in radian

    Returns:
    float: the haversine of the angle
    """
    return (sin(theta/2))**2

def convert_coord(coord, hemi):
    coord *= -1 if hemi in [2, 3] else 1
    return coord

def calculate_distance(lat1, long1, lat2, long2) -> float:
    """
    Calculate the great circle distance between two points on the earth specified in decimal degrees and directions.

    Parameters:
    sender_loc_str (str): the GPS coordinate string of the signal sender
    receiver_loc_str (str): the GPS coordinate string of the signal receiver

    Returns:
    float: Distance between the two points in meters.
    """

    # Convert to radian
    lat1 *= pi/180
    long1 *= pi/180
    lat2 *= pi/180
    long2 *= pi/180

    # Compute distance using the Haversine formula
    # https://en.wikipedia.org/wiki/Haversine_formula 
    
    R = 6371.0 * 1e3 # Radius of earth in meters
    delta_lat = lat1 - lat2
    delta_long = long1 - long2
    h = haversine(delta_lat) + cos(lat1) * cos(lat2) * haversine(delta_long)
    d = 2 * R * asin(sqrt(h))

    return abs(d)

if __name__ == "__main__":
    loc_str_1 = "043653927650079366740613" # (43.6539276567441, -79.36674061713879)
    loc_str_2 = "043654256660079365365273" # (43.65425666252635, -79.36536527097456)

    # loc = loc_str2float(loc_str_1)
    print(calculate_distance(loc_str_1, loc_str_2))