from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.save()
        return instance