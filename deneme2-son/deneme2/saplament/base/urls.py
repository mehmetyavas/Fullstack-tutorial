from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('product-update/',views.product_update,name='product-update'),

    #path('table/', views.table,name='table'),
    #path('dashboard/',views.dashboard,name='dashboard'),

    # path('add/', views.add, name='add'),
    # path('add/addrecord/', views.addRecord, name='addrecord'),
    # path('update/<int:id>', views.update, name="update"),
    # path('update/updaterecord/<int:id>', views.updateRecord, name='updaterecord'),
    # path('table/delete/<int:id>',views.delete,name='delete'),
    path('product/<slug>',views.product,name='product'),
    path('category/<slug>', views.category, name='category'),
    path('order/',views.order,name='order'),
    path('order-summary/',views.order_summary,name='order-summary'),
    path('cart/',views.cart,name='cart'),
    path('add-to-cart/<slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove-item-from-cart'),
    path('deleteCart/<slug>',views.deleteCart,name='deleteCart'),
    path('cart-summary/', views.cart_summary, name='cart-summary'),

    # path('table/add-category/', views.addCategory,name='add-category'),
    # path('table/add-category/addCategoryRecord/', views.addCategoryRecord,name='addcategoryrecord'),
    # path('table/categoryUpdate/<int:id>',views.categoryUpdate,name='categoryUpdate'),
    # path('table/categoryUpdate/categoryUpdateRecord/<int:id>',views.categoryUpdateRecord, name='categoryUpdateRecord'),
    # path('table/categoryDelete/<int:id>',views.categoryDelete,name='categoryDelete'),
]