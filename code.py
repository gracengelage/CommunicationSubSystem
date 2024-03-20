import time
from communication_functions.get_location import get_location


while True:
    location_received = ""
    print(get_location(location_received))
    time.sleep(1)