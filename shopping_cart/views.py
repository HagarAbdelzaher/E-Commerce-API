from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Cart
from .serializar import CartSerializer, CartItemSerializer


# Create your views here.
class CartDetail(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        user_id = self.request.user.id
        return Cart.objects.filter(user=user_id)
  
class CartItem(generics.CreateAPIView):
    serializer_class = CartItemSerializer  
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
      
    
