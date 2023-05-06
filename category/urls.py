from django.urls import path,include
from rest_framework.routers import DefaultRouter
from category.views import *

router = DefaultRouter()


# urlpatterns = [
#     path('<int:id>/products/', name='categoryid'),
   
# ]