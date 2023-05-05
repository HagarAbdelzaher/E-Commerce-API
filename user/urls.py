from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from user.views import *

router = DefaultRouter()


urlpatterns = [
    path('register/', signupView, name='register'),
    path('login/',obtain_auth_token , name='login')
]