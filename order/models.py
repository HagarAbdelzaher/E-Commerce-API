from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Order(models.Model):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

    STATUS_CHOICES = ((PENDING, "pending"), (SHIPPED, "shipped"), (DELIVERED, "delivered"))
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on delivery'),
        ('online', 'Online payment'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # shippingAddress = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
        
    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return str(self.id)