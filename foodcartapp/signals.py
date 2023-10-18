from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def your_signal_handler(sender, instance, created, **kwargs):
    if created:
        instance.price = instance.product.price
