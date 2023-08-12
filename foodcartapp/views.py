from django.http import JsonResponse
from django.templatetags.static import static
import json

from .models import Product
from .models import Order
from .models import OrderItem
from .models import ProductCategory
from .models import Restaurant

from rest_framework.decorators import api_view


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def get_pic(url):
    import requests
    URL = 'https://raw.githubusercontent.com/devmanorg/star-burger-products/master/media/'
    response = requests.get(URL+url)
    if response.status_code == 200:
        return response.content
        print('Изображение успешно сохранено.')
    else:
        print('Ошибка при загрузке изображения. Статус код:', response.status_code)


@api_view(['POST'])
def register_order(request):
    cart = request.data
    order = Order.objects.create(
        name=cart['firstname'],
        surname=cart['lastname'],
        contact_phone=cart['phonenumber'],
        address=cart['address']
    )

    for product_info in cart['products']:
        product_id = product_info['product']
        amount = int(product_info['quantity'])

        product = Product.objects.get(pk=product_id)
        OrderItem.objects.create(
            product=product,
            amount=amount,
            order=order
        )
    return JsonResponse(cart)


@api_view(['POST'])
def create_product(request):
    from django.core.files.base import ContentFile
    
    products = request.data
    for product in products:
        category, _ = ProductCategory.objects.get_or_create(name=product['type'])
        img = get_pic(product['img'])
        Product.objects.get_or_create(
            name=product['title'],
            price=product['price'],
            category=category,
            description=product['description'],
            image=ContentFile(img, name=product['img'])
            )
    return JsonResponse({'message': 'Продукты успешно созданы'})


@api_view(['POST'])
def create_restaurant(request):
    restaurants = request.data
    for restaurant in restaurants:
        Restaurant.objects.get_or_create(
            name=restaurant['title'],
            address=restaurant['address'],
            contact_phone=restaurant['contact_phone']
        )
    return JsonResponse({'message': 'Рестораны успешно созданы'})
