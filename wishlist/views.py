from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, Wishlist_Item
from .serializers import WishListSerializer, EditWishlistItemSerializer


# Create your views here.
class WishlistDetail(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        print(user_id)
        return Wishlist.objects.filter(user=user_id)


class CartItem_create(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditWishlistItemSerializer

    def post(self, request, product, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         "user": request.user, "product_id": product})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishlistItem(generics.CreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditWishlistItemSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        wishlist = Wishlist.objects.filter(user=user_id).first()
        items = Wishlist_Item.objects.filter(wish_list=wishlist)
        return items

    def post(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         "user": request.user, "product_id": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk, *args, **kwargs):
        print(self.get_queryset().values())
        try:
            instance = self.get_queryset().get(product_id=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Wishlist_Item.DoesNotExist:
            return Response({"error": "WishList Item doesn't exist"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
