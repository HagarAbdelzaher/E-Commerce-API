from django.db import models
from category.models import Category


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ecommerce/productimages')
    category_id= models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
