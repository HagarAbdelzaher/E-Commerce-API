from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Wishlist, WishlistItem
from .serializer import WishListSerializer


# Create your views here.

class WachListAV(APIView):

    def get(self, request, id):
        try:
            wish_list = Wishlist.objects.get(user=id)
            print(wish_list)
        except Wishlist.DoesNotExist:
            return Response({'errors': "WishList doesn't Exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = WishListSerializer(wish_list)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = WishListSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CartItemsList(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishListSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)