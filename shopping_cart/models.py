from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User
from product.models import Product


# Create your models here.

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
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart")
    
    
    def __str__(self) -> str:
        return self.product.name
