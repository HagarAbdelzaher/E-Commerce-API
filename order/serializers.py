from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer
from user.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_description(self, obj):
        return "Order #{} - {}".format(obj.id, obj.created_at.strftime("%d %B %Y"))