from django.urls import path

from .views import OrderList, OrderDetail, OrderCreate, CancelOrder, StripeCheckout

urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('<int:pk>/cancel', CancelOrder.as_view(), name='order_cancel'),
    path('checkout/', StripeCheckout.as_view(), name='stripe_checkout'),
]
