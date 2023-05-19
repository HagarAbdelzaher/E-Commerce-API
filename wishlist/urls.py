from django.urls import path
from rest_framework.routers import DefaultRouter
from .views  import WishlistItem, WishlistDetail

router = DefaultRouter()

urlpatterns = [
    path('',WishlistDetail.as_view() , name='wishlist_details'),
    path('items/<int:pk>', WishlistItem.as_view(), name='wishlist_items'),
]