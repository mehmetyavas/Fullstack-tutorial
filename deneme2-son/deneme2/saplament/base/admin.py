from django.contrib import admin

from .models import *

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display=('id','title','price','category','urun_desc','slug')
    list_display_links=('id','title')
    search_fields = ('title','urun_desc')
    list_per_page= 10
    list_filter = ('category',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', )
    list_filter = ('product',)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','slug')
    list_display_links=('id','slug')
    list_per_page= 10


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','item', 'quantity','total_price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order',)



admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Products, ItemAdmin)
admin.site.register(categories,CategoryAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Image,ImageAdmin)

admin.site.register(FooterURL)
admin.site.register(Iletisim)
admin.site.register(Hakkimizda)
admin.site.index_title = 'deneme'