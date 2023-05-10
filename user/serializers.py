from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Address
from rest_framework import serializers
User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'user']


    def validate(self, data):
        detailed_address = data.get('detailed_address')
        country = data.get('country')
        city = data.get('city')
        apartment_no = data.get('apartment_no')
        building_no = data.get('building_no')
        floor_no = data.get('floor_no')          

    
        if detailed_address and not isinstance(detailed_address, str):
            raise  serializers.ValidationError("detailed address must be a string.")
        if detailed_address and len(detailed_address) > 300:
            raise  serializers.ValidationError("detailed address can't exceed 300 character");
    
        if country and not isinstance(country , str):
            raise  serializers.ValidationError("Country must be a string.");
        if len(country) < 1 or len(country) > 100:
            raise  serializers.ValidationError("Country length must be more than 1");

        if city and not isinstance(city , str):
            raise  serializers.ValidationError("Country must be a string.");
        if len(city) < 1 or len(city) > 100:
            raise  serializers.ValidationError("city length must be between 1 and 100 characters.");

        if apartment_no and not isinstance(apartment_no,int):
             raise  serializers.ValidationError("apartment number must be a number")
        
        if floor_no and not isinstance(floor_no,int):
             raise  serializers.ValidationError("floor number must be a number")
        if building_no and not isinstance(building_no,int):
             raise  serializers.ValidationError("building number must be a number")
        return data
class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True,min_length=3,max_length=20)
    last_name = serializers.CharField(required=True,min_length=3,max_length=20)
    image = serializers.CharField(required=False , max_length=300)
    username = serializers.CharField(required=True,min_length=3, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'image')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("First name length must be greater than 2 characters.")
        return value

    def validate_last_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Last name length must be greater than 2 characters.")
        return value
    def validate_username(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Username must be a string.")
        
        if len(value) <= 3:
            raise serializers.ValidationError("Username length must be greater than 2  characters.")
        
        return value
    
    def save(self):
        password = self.validated_data['password']
        
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

        # address_data = self.validated_data['address']
        # Address.objects.create( **address_data)
        return user

