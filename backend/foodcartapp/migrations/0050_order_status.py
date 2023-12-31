# Generated by Django 3.2.15 on 2023-10-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('UN', 'Необработанный'), ('CA', 'Отмененный'), ('AC', 'Принятый'), ('PR', 'Приготовленный'), ('SH', 'Отгруженный'), ('CO', 'Выполненный')], default='UN', max_length=2, verbose_name='статус'),
        ),
    ]
