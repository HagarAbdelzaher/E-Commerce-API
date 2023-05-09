from django.urls import path

from .views import *

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('<int:pk>/', order_detail, name='order_detail')
]
