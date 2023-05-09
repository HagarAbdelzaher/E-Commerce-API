
import re
from django.conf import settings
from rest_framework import serializers
from decimal import Decimal
from .models import Product
from category.models import Category


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    # image = serializers.ImageField(required=True)
    description= serializers.CharField()
    quantity= serializers.IntegerField() 
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        # fields = ['name', 'price', 'description', 'quantity','category_id','image]
        fields = ['id','name', 'price', 'description', 'quantity','category_id']
      
      
    def validate_name(self, value):
        pattern = r'[A-Za-z]'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Name must be string')
    
        
        if len(value) < 4:
            raise serializers.ValidationError("Name length must be greater than 3  characters.")
        
        return value
    

    def validate_price(self, value):
        if not isinstance(value, Decimal):
            raise serializers.ValidationError("Price must be decimal.")
        
        if value <1:
            raise serializers.ValidationError("Price must be greater than 0.")
        
        return value
    

    def validate_description(self, value):
        pattern = r'[A-Za-z]'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Description must be string')
        if len(value) < 15:
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


    
    def create(self, validated_data):
        if Product.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError({'error': 'Product name already exists!'})
      
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        if Product.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError({'error': 'Product name already exists!'})
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance



