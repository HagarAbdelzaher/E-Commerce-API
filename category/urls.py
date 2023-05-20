from django.urls import path,include
from rest_framework.routers import DefaultRouter
from category.views import *

router = DefaultRouter()





urlpatterns = [
    path('',category_list, name='categories'),
    path('<int:id>',category_details, name='categorydetails'),
  
]