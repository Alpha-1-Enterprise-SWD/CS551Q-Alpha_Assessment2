import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# address = "526 King Street"
# postcode = "AB24 5RS"

# geolocator = Nominatim(user_agent="test_app")
# location = geolocator.geocode(f"{address}, {postcode}")
# print((location.latitude, location.longitude))


def get_coordinates(address, postcode):
    if not address and not postcode:
        return None, None

    geolocator = Nominatim(user_agent="gp_radar_app")
    query = f"{address}, {postcode}"
    try:
        location = geolocator.geocode(query, timeout=10)
        time.sleep(1)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not find coordinates for {query}")
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for '{query}': {e}")
        return None, None


lat, lon = get_coordinates("526 King Street, Aberdeen", "AB24 3NG")
print(lat, lon)
