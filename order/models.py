from django.db import models
from product.models import Product
from user.models import Address
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class Order(models.Model):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    STATUS_CHOICES = ((PENDING, "pending"), (SHIPPED, "shipped"), (DELIVERED, "delivered"), (CANCELED, "canceled"))

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username + '__' + str(self.id) + '__' + str(self.total_price)
    
    def get_order_by_id(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_order_by_user(self, user, pk):
        order = Order.get_order_by_id(self, pk)
        if type(order) == Order and order.user != user:
            return Response({'error': 'You are not allowed to view this order'}, status=status.HTTP_403_FORBIDDEN)
        return order    

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.product.name + '__' + str(self.quantity)

    def get_item_price(self):
        return self.quantity * self.product.price

    def get_product_name(self):
        return self.product.name
    
    # post save increase order total price
    def save(self, *args, **kwargs):
        self.price = self.get_item_price()
        super(OrderItem, self).save(*args, **kwargs)
        self.order.total_price += self.price
        self.order.save()
