from .models import Order, OrderItem
from shopping_cart.models import Cart, Cart_Item
from user.models import Address
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date


class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrderCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        user_address = Address.objects.filter(user=user).first()

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = Cart_Item.objects.filter(cart=cart)
        
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in cart_items:
            if item.quantity > item.product.quantity:
                return Response({'error': f'Product {item.product.name} is out of stock'}, status=status.HTTP_400_BAD_REQUEST)
            
        order = Order.objects.create(user=user, shipping_address=user_address)
        order.save()

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            product = item.product
            product.quantity -= item.quantity
            product.save()
            
        cart_items.delete()
        
        serializer = OrderSerializer(order, data={'user':user.pk, 'order_items': [], **request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        order = Order.get_order_by_user(self, request.user, pk)
        if type(order) == Response:
            return order   
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
class CancelOrder(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        order = Order.get_order_by_id(self, pk)
        if type(order) == Response:
            return order
        if order.user != request.user:
            return Response({'error': 'You are not allowed to cancel this order'}, status=status.HTTP_403_FORBIDDEN)
        # cancel order within the free cancelation time 3 days
        if (date.today() - order.created_at.date()).days > 3 and order.status == 'pending':
            return Response({'error': 'You are not allowed to cancel this order'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)