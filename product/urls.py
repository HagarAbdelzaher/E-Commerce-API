from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product.views import *

router = DefaultRouter()


# urlpatterns = [
#     path('<int:id>',name='productid'),
   
# ]