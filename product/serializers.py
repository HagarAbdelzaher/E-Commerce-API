
from django.conf import settings
from rest_framework import serializers
from decimal import Decimal
from .models import Product
from category.models import Category


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,min_length=4,max_length=20)
    price = serializers.DecimalField(required=True,max_digits=8,decimal_places=2)
    # image = serializers.ImageField(required=True)
    description= serializers.CharField(required=True,min_length=15, max_length=200)
    quantity= serializers.IntegerField(required=True) 
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        # fields = ['name', 'price', 'description', 'quantity','category_id','image]
        fields = ['name', 'price', 'description', 'quantity','category_id']
      
    def validate_name(self, data):
        name = data.get('name')
     
        if not isinstance(name, str):
            raise serializers.ValidationError("Name must be a string.")
        
        if len(name) <= 4:
            raise serializers.ValidationError("Name length must be greater than 3  characters.")
        
        return data
    

    def validate_price(self, value):
        if not isinstance(value, Decimal):
            raise serializers.ValidationError("Price must be decimal.")
        
        if value <=1:
            raise serializers.ValidationError("Price must be greater than 0.")
        
        return value
    

    def validate_description(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Description must be a string.")
        
        if len(value) <= 15:
            raise serializers.ValidationError("Description length must be greater than 14 characters.")
        
        return value


    def validate_quantity(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Quantity must be a integer.")
        
        if value < 1:
            raise serializers.ValidationError("Quantity length must be greater than 0 .")
        
        return value
    
    def validate_category_id(self, value):

        if not isinstance(value, Category):
            raise serializers.ValidationError("Category must be a valid category object.")
        return value

    def save(self):
       
        # image = self.validated_data['image']
        
        if Product.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError({'error': 'Product name already exists!'})
        

    

        product = Product(
                name=self.validated_data['name'],
                price=self.validated_data['price'],
                description = self.validated_data['description'],
                quantity=self.validated_data['quantity'],
                category_id = self.validated_data['category_id'],
            )
        
     
        product.save()
        return product
