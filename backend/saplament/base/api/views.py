from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from base.api.serializers import *

from base.models import Products, Cart, Order, CartItem
from django.contrib.auth.models import User
# class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework import generics

from .serializers import CartItemSerializer

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response

# token

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),  # self.get_next_link(),
                'current': 'http://127.0.0.1:8000/api/products/?page=' + str(self.request.query_params.get('page', 1)),
                'previous': self.get_previous_link(),  # self.get_previous_link(),
                'count': self.page.paginator.num_pages,  # self.page.paginator.count => products'ın countu
                'current_page_num': str(self.request.query_params.get('page', 1)),
            },
            'results': data
        })


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = StandardResultsSetPagination

    # permission_classes =


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # def get_object(self):
    #     return categories.objects.get(pk=)


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = categories.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = categories.objects.all()
    serializer_class = CategorySerializer


class ProductsForCategoryDetailAPIView(generics.ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = categories.objects.get(slug=category_slug)
        return Products.objects.filter(category=category)
        # user_id = self.kwargs.get('user_id')
        # user = User.objects.get(pk=user_id)
        # return Cart.objects.filter(user=user)


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartItemDetailAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressDetailAPIView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


# class ImageAPIView(generics.ListCreateAPIView):
#
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer

class IletisimAPIView(generics.ListCreateAPIView):
    queryset = Iletisim.objects.all()
    serializer_class = IletisimSerializer


class IletisimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Iletisim.objects.all()
    serializer_class = IletisimSerializer


class FooterURLAPIView(generics.ListCreateAPIView):
    queryset = FooterURL.objects.all()
    serializer_class = FooterURLSerializer


class FooterURLDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FooterURL.objects.all()
    serializer_class = FooterURLSerializer


class HakkimizdaAPIView(generics.ListCreateAPIView):
    queryset = Hakkimizda.objects.all()
    serializer_class = HakkimizdaSerializer


class HakkimizdaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hakkimizda.objects.all()
    serializer_class = HakkimizdaSerializer


class CartForUserAPIView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        return Cart.objects.filter(user=user)


class OrderForUserAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        return Order.objects.filter(user=user)
