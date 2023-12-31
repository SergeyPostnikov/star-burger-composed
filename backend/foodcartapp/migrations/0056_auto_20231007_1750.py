# Generated by Django 3.2.15 on 2023-10-07 17:50

from django.db import migrations

def create_restaurants(apps, schema_editor):
    Restaurant = apps.get_model('foodcartapp', 'Restaurant')

    restaurants_data = [
        {
            "title": "Star Burger Арбат",
            "address": "Москва, ул. Новый Арбат, 15",
            "contact_phone": "+7 (967) 157-44-13"
        },
        {
            "title": "Star Burger Цветной",
            "address": "Москва, Цветной бульвар, 11с2",
            "contact_phone": "+7 (929) 949-55-36"
        },
        {
            "title": "Star Burger Европейский",
            "address": "Москва, пл. Киевского Вокзала, 2",
            "contact_phone": "+7 (929) 680-47-58"
        }
    ]

    for restaurant_data in restaurants_data:
        Restaurant.objects.create(
            name=restaurant_data['title'],
            address=restaurant_data['address'],
            contact_phone=restaurant_data['contact_phone']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_alter_order_payment_method'),
    ]

    operations = [
        migrations.RunPython(create_restaurants),
    ]
