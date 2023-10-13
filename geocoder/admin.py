from django.contrib import admin
from .models import AddressPoint
# Register your models here.


@admin.register(AddressPoint)
class AddressPointAdmin(admin.ModelAdmin):
    pass
