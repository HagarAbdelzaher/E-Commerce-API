from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True,min_length=3,max_length=20)
    last_name = serializers.CharField(required=True,min_length=3,max_length=20)
    # image = serializers.ImageField(required=True)
    username = serializers.CharField(required=True,min_length=3, max_length=20)

    class Meta:
        model = User
        # fields = ['username', 'email', 'password', 'first_name','last_name','image']
        fields = ['username', 'email', 'password', 'first_name','last_name']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    def validate_first_name_last_name(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not isinstance(first_name, str):
            raise serializers.ValidationError("First name must be a string.")
        
        if not isinstance(last_name, str):
            raise serializers.ValidationError("Last name must be a string.")
        
        if len(first_name) <= 3:
            raise serializers.ValidationError("First name length must be greater than 2  characters.")
        
        if len(last_name) <= 3:
            raise serializers.ValidationError("Last name length must be greater than 2  characters.")
        
        return data
    def validate_username(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Username must be a string.")
        
        if len(value) <= 3:
            raise serializers.ValidationError("Username length must be greater than 2  characters.")
        
        return value
    
    def save(self):
        password = self.validated_data['password']
        # image = self.validated_data['image']
        
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'username already exists!'})
        

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name = self.validated_data['last_name'],
            )
        
        user.set_password(password)
        user.save()
        return user
