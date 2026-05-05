import pgeocode

nomi = pgeocode.Nominatim('gb')

def get_coordinates(postcode):
    result = nomi.query_postal_code(postcode)
    if result is not None and not result.isnull()['latitude']:
        return result['latitude'], result ['longitude']
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