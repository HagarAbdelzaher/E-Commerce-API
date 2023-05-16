from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from shopping_cart.models import Cart_Item, Cart
from .serializers import CartSerializer, EditCartItemSerializer
from rest_framework.permissions import IsAuthenticated
from product.models import Product


# Create your views here.
class CartDetail(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        print(user_id)
        return Cart.objects.filter(user=user_id)


class CartItem_create(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditCartItemSerializer

    def post(self, request, product, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         "user": request.user, "product_id": product})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItem(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditCartItemSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        cart = Cart.objects.filter(user=user_id).first()
        items = Cart_Item.objects.filter(cart=cart).filter()
        return items

    def post(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         "user": request.user, "product_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, action, *args, **kwargs):
        try:
            instance = self.get_queryset().get(product=pk)
            serializer = self.get_serializer(
                instance, data=request.data, context={"action": action, "product_id": pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Cart_Item.DoesNotExist:
            return Response({"error": "Cart Item doesn't exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, pk, action=None, *args, **kwargs):
        try:
            instance = self.get_queryset().get(product=pk)
            product = Product.objects.get(id=pk)
            product.quantity += instance.quantity
            product.save()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart_Item.DoesNotExist:
            return Response({"error": "Cart Item doesn't exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
