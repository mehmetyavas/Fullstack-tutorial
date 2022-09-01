from django.urls import path, re_path
from base.api import views as api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('products/', api_views.ProductListCreateAPIView.as_view(), name='ürün-listesi'),
    path('products/<int:pk>', api_views.ProductDetailAPIView.as_view(), name='ürün-bilgileri'),
    # path('image/', api_views.ImageAPIView.as_view(), name='image'),

    path('category/', api_views.CategoryListAPIView.as_view(), name='kategori'),
    path('category/<int:pk>', api_views.CategoryDetailAPIView.as_view(), name='kategori'),

    # user ekle
    path('cart/', api_views.CartListCreateAPIView.as_view(), name='sepet-listesi'),
    path('cart/<int:pk>', api_views.CartDetailAPIView.as_view(), name='sepet-bilgileri'),
    path('cart-item/', api_views.CartItemDetailAPIView.as_view(), name='sepetitem-bilgileri'),
    # daha sonra usera göre çek
    path('order/', api_views.OrderListCreateAPIView.as_view(), name='sipariş-listesi'),
    path('order/<int:pk>', api_views.OrderDetailAPIView.as_view(), name='sipariş-bilgileri'),

    path('user/', api_views.UserListAPIView.as_view(), name='user-bilgileri'),
    path('user/<int:pk>', api_views.UserDetailAPIView.as_view(), name='user-bilgileri'),
    path('address/', api_views.AddressDetailAPIView.as_view(), name='adres-bilgileri'),

    # path('cart/<int:pk>/user/1/'),
    path('iletisim/', api_views.IletisimAPIView.as_view(), name='iletisim'),  # FooterURL   Hakkimizda   Image
    path('iletisim/<int:pk>', api_views.IletisimDetailAPIView.as_view(), name='iletisim'),
    # FooterURL   Hakkimizda   Image

    path('footer-url/', api_views.FooterURLAPIView.as_view(), name='iletisim'),  # FooterURL   Hakkimizda   Image
    path('footer-url/<int:pk>', api_views.FooterURLDetailAPIView.as_view(), name='iletisim'),
    # FooterURL   Hakkimizda   Image

    path('hakkimizda/', api_views.HakkimizdaAPIView.as_view(), name='iletisim'),  # FooterURL   Hakkimizda   Image
    path('hakkimizda/<int:pk>', api_views.HakkimizdaDetailAPIView.as_view(), name='iletisim'),
    # FooterURL   Hakkimizda   Image
    path('user/<int:user_id>/cart', api_views.CartForUserAPIView.as_view(), name='userin-carti'),
    path('user/<int:user_id>/order', api_views.OrderForUserAPIView.as_view(), name='userin-orderi'),
    path('category/<category_slug>/products', api_views.ProductsForCategoryDetailAPIView.as_view(),
         name='category-products'),

    # path('Image/',),

    path('token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
