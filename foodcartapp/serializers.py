from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        product = ProductSerializer(many=True)
        fields = ['quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True)

    def save(self):
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
        return order
    
    def validate_products(self, value):
        if not value:
            raise ValidationError('Products key cant be empty')
        return value

    class Meta:
        model = Order
        fields = '__all__'
