import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coordinates(address, postcode):
    if not address and not postcode:
        return None, None
    
    geolocator = Nominatim(user_agent="gp_radar_app")
    query = f"{address, postcode}"
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

HB_LOOKUP = {
    'S08000015': 'Ayrshire and Arran',
    'S08000016': 'Borders',
    'S08000017': 'Dumfries and Galloway',
    'S08000019': 'Forth Valley',
    'S08000020': 'Grampian',
    'S08000022': 'Highland',
    'S08000024': 'Lothian',
    'S08000025': 'Orkney',
    'S08000026': 'Shetland',
    'S08000028': 'Western Isles',
    'S08000029': 'Fife',
    'S08000030': 'Tayside',
    'S08000031': 'Greater Glasgow and Clyde',
    'S08000032': 'Lanarkshire',
}