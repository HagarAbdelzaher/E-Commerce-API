from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views  import WachListAV

router = DefaultRouter()



urlpatterns = [
    path('',WachListAV.as_view() , name='wishlist_details'),
  
]