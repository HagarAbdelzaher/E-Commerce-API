from django.shortcuts import render, redirect
from .models import Order, OrderItem
from shopping_cart.models import Cart
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # # cart = Cart.objects.filter(user=request.user)
    # cart = Cart(request)

    # if(request.method == 'POST'):
    #     shipping_address = request.POST.get('shipping_address')
    #     payment_method = request.POST.get('payment_method')
        
    #     order = Order.objects.create(user=request.user, shipping_address=shipping_address, payment_method=payment_method, payment_status='unpaid')
        
    #     # for item in request.user.cart_items.all():
    #     #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    #     #     item.delete()
        
    #     for item in cart:
    #         product = item['product']
    #         quantity = int(item['quantity'])
    #         price = item['price'] * quantity
            
    #         OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
    #         cart.remove(item['product'])
            
    #     return redirect('account')
    
    # return redirect('cart')
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response({'success': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)