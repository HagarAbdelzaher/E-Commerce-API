from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from shopping_cart.views import CartDetail, CartItem

router = DefaultRouter()

urlpatterns = [
    path('', CartDetail.as_view(), name='cart_details'),
    path('/items/<int:pk>/<str:action>', CartItem.as_view(), name='cart_items'),
]
