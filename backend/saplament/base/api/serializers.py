from dataclasses import Field, field, fields
from re import T
from rest_framework import serializers
from base.models import *
from django.contrib.auth.models import User


#
# class CartItemSerializer(serializers.ModelSerializer):
#     item = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CartItem
#         fields = '__all__'
#
#     def get_item(self, object):
#         return f'http://127.0.0.1:8000/api/products/{object.item_id}'

class CategorySerializer(serializers.ModelSerializer):
    # products_category = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = categories
        fields = '__all__'




class ProductsSerializer(serializers.ModelSerializer):
    # category = serializers.DictField(child = serializers.CharField())
    category = serializers.SerializerMethodField()
    foto = serializers.SerializerMethodField()

    class Meta:
        model = Products
        exclude = ['urun_foto']

    def get_category(self, object):
        category = categories.objects.get(pk=object.category_id)
        return [{
            'category_id': object.category_id,
            'category_name': category.category_name,
            'slug': category.slug
        }]

    def get_foto(self, object):
        return f'/images/{object.urun_foto}'


class CartItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        exclude = ['quantity']

    def get_item(self, object):
        product = Products.objects.get(pk=object.item_id)
        return [{
            'item_id': object.item_id,
            'item': product.title,
            'slug': product.slug,
            'price': product.price,
            'quantity': object.quantity,
            # 'total_price': object.total_price

        }]
    # def get_item(self, object):


#     return f'http://127.0.0.1:8000/api/products/{object.item_id}'


class ProductsDetailSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,
                                      read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_user(self, object):
        return f'http://127.0.0.1:8000/api/user/{object.user_id}'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


#
# class ImageSerializer(serializers.ModelSerializer):
#     product_image = ProductsSerializer(read_only=True)
#
#     class Meta:
#         model = Image
#         fields = '__all__'
#

# FOOTER *---------------------------------------*
class FooterURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterURL
        fields = '__all__'


class IletisimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iletisim
        fields = '__all__'


class HakkimizdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hakkimizda
        fields = '__all__'
