from django.urls import path,include
from rest_framework.routers import DefaultRouter
from shopping_cart.views  import CartDetail, CartItem 

router = DefaultRouter()



urlpatterns = [
    path('',CartDetail.as_view(), name='cart_details'),
    path('item',CartItem.as_view(), name='cart_items'),
  
]