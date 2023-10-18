from rest_framework import serializers
from .models import Order, OrderItem
from django.db import transaction
from phonenumber_field.modelfields import PhoneNumberField


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(
        many=True, 
        write_only=True,
        allow_empty=False, 
        source='items'
    )
    phonenumber = PhoneNumberField(region="RU")

    def save(self):
        with transaction.atomic():
            order = Order.objects.create(
                firstname=self.validated_data['firstname'],
                lastname=self.validated_data['lastname'],
                phonenumber=self.validated_data['phonenumber'],
                address=self.validated_data['address']
            )

            for item in self.validated_data['items']:
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
