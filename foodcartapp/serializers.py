from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'pk': {'source': 'product'},
            'amount': {'source': 'quantity'}
        }


class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True)
    # def save(self):
    #     order = Order.objects.create(
    #         name=self.validated_data['firstname'],
    #         surname=self.validated_data['lastname'],
    #         contact_phone=self.validated_data['phonenumber'],
    #         address=self.validated_data['address']
    #         )
    #     print(order)
        # for item in self.validated_data['products']:


    class Meta:
        model = Order
        # fields = ['name', 'surname', 'contact_phone', 'address',]
        # fields = '__all__'
        fields = ['name',]



        extra_kwargs = {
            'firstname': {'source': 'name'},
        #     'lastname': {'source': 'surname'},
        #     'phonenumber': {'source': 'contact_phone'},
        #     # 'products': {'source': 'items'}
        }
