# Generated by Django 3.2.15 on 2023-10-06 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, help_text='Необязательный комментарий к заказу', verbose_name='комментарий'),
        ),
    ]
