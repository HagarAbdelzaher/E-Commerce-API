from django.db import models
from django.forms import ValidationError
import re

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
    def clean(self):
    
        pattern = r'[A-Za-z]'
        if not re.match(pattern, self.name):
            raise ValidationError('Name must be string')
    
        
        if len(self.name) < 4:
            raise ValidationError("Name length must be greater than 3  characters.")
        
        if len(self.name) > 20:
            raise ValidationError("Name length must be less than 20  characters.")
        
        return self.name

