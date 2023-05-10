from rest_framework import serializers
from .models import Cart , CartItem
from user.serializers import SignUpSerializer
from product.serializers import ProductSerializer
 
class CartItemSerializer(serializers.ModelSerializer):
    cart_items = ProductSerializer(many = True)
    
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        user = self.context.get('user')

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return cart_item 
 
 
class CartSerializer(serializers.ModelSerializer):  
    user = SignUpSerializer(read_only=True)
    cart_items =  CartItemSerializer(many= True, read_only=True)
    # cart_items = ProductSerializer(many= True, read_only=True)
    # products = ProductSerializer(many = True)

    class Meta:
        model = Cart
        fields = "__all__"
    
