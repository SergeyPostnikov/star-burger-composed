from .models import AddressPoint
from django.contrib import admin


@admin.register(AddressPoint)
class AddressPointAdmin(admin.ModelAdmin):
    pass
