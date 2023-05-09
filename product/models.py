from decimal import Decimal
from django.db import models
from category.models import Category
from django.forms import ValidationError
import re



class Product(models.Model):
    name = models.CharField(max_length=20,unique=True)
    image = models.CharField(max_length=200,default='')
    category_id= models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
    
       
      
    def clean(self):
        pattern = r'[A-Za-z]'
        if not re.match(pattern,self.name):
            raise ValidationError('Name must be string')
    
        
        if len(self.name) < 4:
            raise ValidationError("Name length must be greater than 3  characters.")
        
        if len(self.name) > 20:
           raise ValidationError("Name length must be less than 20  characters.")
        
        
    
        if not isinstance(self.price, Decimal):
            raise ValidationError("Price must be decimal.")
        
        if self.price < 1:
            raise ValidationError("Price must be greater than 0.")
        
       
        pattern = r'[A-Za-z]'
        if not re.match(pattern, self.description):
            raise ValidationError('Description must be string')
        if len(self.description) < 15:
            raise ValidationError("Description length must be greater than 14 characters.")
        
        if len(self.description) > 150:
            raise ValidationError("Description length must be less than 150 characters.")
    
        if not isinstance(self.quantity, int):
            raise ValidationError("Quantity must be a integer.")
        
        if self.quantity < 1:
            raise ValidationError("Quantity length must be greater than 0 .")
        
      

        if not isinstance(self.category_id, Category):
            raise ValidationError("Category must be a valid category object.")
        return self.category_id

