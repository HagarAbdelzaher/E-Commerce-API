from django.db import models

# Create your models here.
from django.db import models
from user.models import User
from product.models import Product

# Create your models here.


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    products = models.ManyToManyField(Product, related_name='wishes', through='Wishlist_Item')
    
    def __str__(self) -> str:
        return f'{self.user.username} wish list'


class Wishlist_Item(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist_items")
    wish_list = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="fav_items")
    
    def __str__(self) -> str:
        return self.product.name

