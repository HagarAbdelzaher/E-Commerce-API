from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product.views import *

router = DefaultRouter()



urlpatterns = [
    path('',product_list, name='products'),
    path('<int:id>',product_details, name='productdetails'),
  
]