import requests

from django.conf import settings
from foodcartapp.models import Order
from foodcartapp.models import OrderItem
from foodcartapp.models import Restaurant
from geocoder.models import AddressPoint
from geopy import distance
from requests.exceptions import HTTPError


def fetch_coordinates(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {
        "geocode": address,
        "apikey": settings.GEOCODER_KEY,
        "format": "json"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection'][
            'featureMember']
        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lat, lon
    except HTTPError:
        return None


def get_address_point(address: str) -> tuple[float, float]:
    address_point, created = AddressPoint.objects.get_or_create(
        address=address
    )
    if created:
        lat, lon = fetch_coordinates(address)
        address_point.latitude = lat
        address_point.longitude = lon
        address_point.save()

    return address_point.latitude, address_point.longitude


def get_distance(order, restaurant):
    order_point = get_address_point(order.address)
    restaurant_point = get_address_point(restaurant.address)
    distance_between = distance.distance(order_point, restaurant_point).km
    return f'{distance_between:.3f} км'


def get_available_restaurants(order_id):
    order_items = OrderItem.objects.filter(order_id=order_id)
    order_product_ids = set(order_items.values_list('product_id', flat=True))

    eligible_restaurants = []

    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        menu_items = restaurant.menu_items
        menu_product_ids = set(menu_items.values_list('product_id', flat=True))
        if order_product_ids.issubset(menu_product_ids):
            order = Order.objects.get(pk=order_id)
            restaurant.distance = get_distance(order, restaurant)
            eligible_restaurants.append(restaurant)

    return sorted(eligible_restaurants, key=lambda rest: rest.distance)
