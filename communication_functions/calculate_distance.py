from math import radians, sin, cos, sqrt, asin, pi

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

    lat1 = 43.66392
    long1 = -79.38653

    lat2 = 43.66388
    long2 = -79.38648
    
    print(calculate_distance(lat1, long1, lat2, long2))