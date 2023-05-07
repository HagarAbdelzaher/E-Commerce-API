from django.db import models
from user.models import User
from product.models import Product

# Create your models here.


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    def __str__(self) -> str:
        return f'{self.user.username} shopping cart'


class Cart_Item(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items")
    quntity = IntegerRangeField(min_value=1, max_value=15)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items")
    
    def __str__(self) -> str:
        return self.product.name
