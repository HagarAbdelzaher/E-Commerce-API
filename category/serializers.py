
from django.conf import settings
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,min_length=4,max_length=20)


    class Meta:
        model = Category
        fields = ['id' ,'name']
      
    def validate_name(self, data):
        name = data.get('name')
     
        if not isinstance(name, str):
            raise serializers.ValidationError("Name must be a string.")
        
        if len(name) <= 4:
            raise serializers.ValidationError("Name length must be greater than 3  characters.")
        
        return data

    
    def save(self):
     
        
        if Category.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError({'error': 'Category name already exists!'})
        

     

        category = Category(
    
                name=self.validated_data['name'],
              
            )
        
      
        category.save()
        return  category 
