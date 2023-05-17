from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view , permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import SignUpSerializer , AddressSerializer , UserUpdateSerializer
from.models import Address




class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        address = Address.objects.filter(user=user).first()
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address': AddressSerializer(address).data if address else None,
                # add any additional user data fields here
            }
        })



@api_view(['POST'])
def signupView(request):
    if request.method == 'POST':
        #send request data to serializer
        serializer = SignUpSerializer(data=request.data)
        address_serializer = AddressSerializer(data=request.data.get('address'));
        
        data = {}
        #check validity of requests of address and user
        if serializer.is_valid():
            if address_serializer.is_valid():
                account = serializer.save()
                address_serializer.save(user=account)
            else:
                return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # sending response back
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['address'] = address_serializer.data
            
            token = Token.objects.get(user=account).key
            data['token'] = token
    
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def logoutView(request):
        user = request.user
        user.auth_token.delete()
        return Response({'success':'logged out successfuly'},status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateView(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateAddressView(request):
    user = request.user
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        return Response({'detail': 'Address not found'}, status=404)

    serializer = AddressSerializer(address, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)