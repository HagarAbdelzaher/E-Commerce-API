from django.contrib import admin
from shopping_cart.models import Cart, Cart_Item

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cart_Item)