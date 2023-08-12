from django.urls import path

from .views import product_list_api, banners_list_api, register_order, create_product, create_restaurant


app_name = "foodcartapp"

urlpatterns = [
    path('products/', product_list_api),
    path('banners/', banners_list_api),
    path('order/', register_order),
    path('create_product/', create_product),
    path('create_restaurant/', create_restaurant)
]
