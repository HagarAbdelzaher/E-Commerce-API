from django.shortcuts import render, redirect
from .models import Order, OrderItem
from shopping_cart.models import Cart

def start_order(request):
    # cart = Cart.objects.filter(user=request.user)
    cart = Cart(request)

    if(request.method == 'POST'):
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        
        order = Order.objects.create(user=request.user, shipping_address=shipping_address, payment_method=payment_method, payment_status='unpaid')
        
        # for item in request.user.cart_items.all():
        #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        #     item.delete()
        
        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = item['price'] * quantity
            
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            cart.remove(item['product'])
            
        return redirect('account')
    
    # return redirect('cart')
    