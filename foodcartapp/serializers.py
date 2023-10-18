from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Order, OrderItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(
        many=True, 
        write_only=True,
        allow_empty=False, 
        source='items'
    )

    def save(self):
        with transaction.atomic():
            order = Order.objects.create(
                firstname=self.validated_data['firstname'],
                lastname=self.validated_data['lastname'],
                phonenumber=self.validated_data['phonenumber'],
                address=self.validated_data['address']
            )

            for item in self.validated_data['products']:
                product = item['product']
                amount = int(item['quantity'])
                OrderItem.objects.create(
                    product=product,
                    quantity=amount,
                    order=order
                )
            order.calculate_total_price()
            return order

    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'address',
            'products'
        ]
