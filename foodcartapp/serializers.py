from rest_framework import serializers
from .models import Order, OrderItem, Product
from pprint import pprint


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

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

    class Meta:
        model = Order
        fields = '__all__'


data = {
  "products": [
    {
      "product": 1,
      "quantity": 1
    },
    {
      "product": 2,
      "quantity": 1
    }
  ],
  "firstname": "Perer",
  "lastname": "Swann",
  "phonenumber": "+79046396540",
  "address": "СПб Литейный 45"
}


# serializer = OrderSerializer(data=data)
# if serializer.is_valid():
#     order = serializer.save()
#     print('All ok!')
# else:
#     print(serializer.errors)
