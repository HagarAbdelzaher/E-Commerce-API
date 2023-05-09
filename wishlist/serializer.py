from rest_framework import serializers
from .models import Wishlist
from user.serializers import SignUpSerializer
from product.serializers import ProductSerializer
 

class WishListSerializer(serializers.ModelSerializer):  
    user = SignUpSerializer(read_only=True)
    products = ProductSerializer(many = True)
      
    class Meta:
        model = Wishlist
        fields = "__all__"
