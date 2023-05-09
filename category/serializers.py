
import re
from django.conf import settings
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)


    class Meta:
        model = Category
        fields = ['id' ,'name']
      
    # def validate_name(self, value):
    #     pattern = r'[A-Za-z]'
    #     if not re.match(pattern, value):
    #         raise serializers.ValidationError('Name must be string')
    
        
    #     if len(value) < 4:
    #         raise serializers.ValidationError({"Name length must be greater than 3  characters."})
        
    #     if len(value) > 20:
    #         raise serializers.ValidationError({"Name length must be less than 20  characters."})
        
    #     return value

    
    # def create(self, validated_data):
    #     if Category.objects.filter(name=self.validated_data['name']).exists():
    #         raise serializers.ValidationError({'error': 'Category name already exists!'})
      
    #     category = Category.objects.create(**validated_data)
    #     return category

    # def update(self, instance, validated_data):
    #     if Category.objects.filter(name=self.validated_data['name']).exists():
    #         raise serializers.ValidationError({'error': 'Category name already exists!'})
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance




