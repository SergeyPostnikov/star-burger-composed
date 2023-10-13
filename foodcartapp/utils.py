from django.conf import settings
from geopy import distance
import requests
from foodcartapp.models import Product, Restaurant, Order, OrderItem

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(apikey, order, restaurant):
    order_address = fetch_coordinates(apikey, order.address)
    restaurant_address = fetch_coordinates(apikey, restaurant.address)
    return f'{distance.distance(order_address, restaurant_address).km:.3f} км'


def get_available_restaurants(apikey, order_id):
    products_in_order = set(OrderItem.objects.filter(order_id=order_id).values_list('product_id', flat=True))
    restaurants_with_all_products = []

    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        products_in_menu = set(restaurant.menu_items.values_list('product_id', flat=True))
        if set.intersection(products_in_order, products_in_menu) == products_in_order:
            restaurant.distance = get_distance(apikey, Order.objects.get(pk=order_id), restaurant)
            restaurants_with_all_products.append(restaurant)
    return sorted(restaurants_with_all_products, key=lambda restaurant: restaurant.distance)

