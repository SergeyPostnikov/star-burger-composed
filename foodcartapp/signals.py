from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(pre_save, sender=OrderItem)
def set_price(sender, instance, **kwargs):
    instance.price = instance.product.price
