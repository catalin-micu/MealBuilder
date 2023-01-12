import googlemaps
import random

gmaps = googlemaps.Client(key='AIzaSyCD7Xa_QbIWjWJ1D8YS0mjSVHTruI82TU8')


def get_nearby_restaurants_from_gmaps(address: str) -> list:
    try:
        geo = gmaps.geocode(address)[0]
        coordinates = geo['geometry']['location']
        whole_restaurants_info = gmaps.places(query='restaurant', location=coordinates, radius=1, type='restaurant')['results']

        useful_restaurant_info = []
        for r in whole_restaurants_info:
            useful_restaurant_info.append({
                'restaurant_name': r['name'],
                'city': address.split(',')[1].strip().lower(),
                'provides_custom_meals': bool(random.getrandbits(1)),
                'provides_scheduled_delivery': bool(random.getrandbits(1)),
            })

        return useful_restaurant_info
    except Exception as exc:
        raise ValueError(f'Cannot find given address: "{address}. The following exception occured: "{exc}')
