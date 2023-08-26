from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework import status
from rest_framework.response import Response

from .models import Product

from .serializers import OrderSerializer

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


@api_view(['POST'])
def register_order(request):
    data = request.data

    if data.get('products') is None:
        return Response(
            {'error': 'products key not presented or null'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(data['products'], list):
        return Response(
            {'error': 'Products key is not list'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if not data['products']:
        return Response(
            {'error': 'Products key cant be empty'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    serialized_order = OrderSerializer(data=data)
    if serialized_order.is_valid():
        serialized_order.save()
        return Response(
            {'message': 'Order succesfully created'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'errors': serialized_order.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
