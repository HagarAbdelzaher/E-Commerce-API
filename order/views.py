from .models import Order, OrderItem
from shopping_cart.models import Cart, Cart_Item
from user.models import Address
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class StripeCheckout(APIView):
    permission_classes = [IsAuthenticated]
    """
    Create and return checkout session ID for order payment of type 'Stripe'
    """
    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = Cart_Item.objects.filter(cart=cart)
        
        # validation before checkout
        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        for item in cart_items:
            if item.quantity > item.product.quantity:
                return Response({'detail': f"Sorry, we do not have enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        #make checkout Session
        line_items = []
        for item in cart_items:
            product_name = item.product.name
            price = int(item.product.price * 100)  # Stripe requires the price in cents
            line_item = {
                'price_data' :{
                    'currency' : 'usd',  
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': price
                },
                'quantity' : item.quantity
            }
            line_items.append(line_item)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,  # include the line_items parameter here
                mode='payment',
                success_url= 'http://localhost:3000/orders',
                cancel_url= 'http://localhost:3000/cart',
                )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': checkout_session.url})

class PaymentSuccess(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        order = Order.objects.filter(user=user).last()
        order.paid = True
        order.save()
        # Redirect to all orders page
        return redirect('order_list')

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
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            product = item.product
            product.quantity -= item.quantity
            product.save()

        cart_items.delete()

        serializer = OrderSerializer(
            order, data={'user': user.pk, 'order_items': [], **request.data})
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
        if order.created_at + timedelta(days=3) < timezone.now():
            return Response({'error': 'Free cancelation time exceeded, you are not allowed to cancel this order'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'cancelled'
        order.save()
        return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)
