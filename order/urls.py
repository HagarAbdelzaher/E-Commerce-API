from django.urls import path

from .views import OrderList, OrderDetail, OrderCreate, CancelOrder, StripeCheckout, PaymentSuccess

urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('<int:pk>/cancel', CancelOrder.as_view(), name='order_cancel'),
    path('<int:pk>/payment/', StripeCheckout.as_view(), name='stripe_checkout'),
    path('payment/success/', PaymentSuccess.as_view(), name='payment_success'),
]
