from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Category
from .serializers import CategorySerializer 
from  product.models import Product
from product.serializers import ProductSerializer 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status,permissions
from rest_framework.pagination import PageNumberPagination

@api_view(['GET', 'POST'])
def category_list (request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        categories = Category.objects.all()
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method == 'POST':
      permission_classes = [permissions.IsAdminUser]
      serializer = CategorySerializer(data=request.data)
      if serializer.is_valid():
          serializer.save ()
          return Response (serializer.data, status=status.HTTP_201_CREATED)
      else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@api_view(['GET', 'PUT','DELETE'])
def category_details (request,id):

    try:
      category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
      return Response (status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
      products = Product.objects.filter(category_id=category.id)
      product_serializer = ProductSerializer(products, many=True)
      serializer =  CategorySerializer(category)
      data = serializer.data
      data['products'] = product_serializer.data
      return Response(data)
    
    elif request.method == 'PUT': 
      permission_classes = [permissions.IsAdminUser]
      serializer = CategorySerializer(category,data=request.data,partial=True)
     
      if serializer.is_valid():
         
            serializer.update (category, serializer.validated_data)
            return Response(serializer.data)
      
      return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE' :
      permission_classes = [permissions.IsAdminUser]
      category.delete()
      return Response (status=status. HTTP_204_NO_CONTENT)