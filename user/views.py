from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import SignUpSerializer
@api_view(['POST'])
def signupView(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
        
            # data['profile_pic'] = account.profile_pic
            token = Token.objects.get(user=account).key
            data['token'] = token
            print(data)
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
        # return (data)