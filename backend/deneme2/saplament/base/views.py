from django.utils import timezone
from django.db.models import Count

from django.db.models import Sum
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages

from django.core.paginator import Paginator

from django.contrib.auth.models import User
# Create your views here.
from .models import (
    Products,
    categories,
    Cart,
    CartItem,
    FooterURL,
    Iletisim,
    Hakkimizda,
    Address,
    Order,
    OrderItem,
    Image,

)


def count(request):
    if request.user.is_authenticated:
        q = CartItem.objects.filter(cart__user=request.user).annotate(Count('quantity'))
        result = 0
        for x in range(0, q.count()):
            res = "".join([ele for ele in str(q[x])[0:3] if ele.isdigit()])
            _int1 = int(res)
            result = result + _int1

    else:
        result = '0'  # burayı düzelt
    return result


def hakkimizda():
    hakkimizda = Hakkimizda.objects.all().values()
    return hakkimizda


def footer():
    footer = FooterURL.objects.all().values()
    return footer


def iletisim():
    iletisim = Iletisim.objects.all().values()
    return iletisim


def index(request):
    product = Products.objects.all().values().order_by('-id')
    category = categories.objects.all().values()

    # template = loader.get_template('index.html')
    toplam = 0
    p = Paginator(product, per_page=10)
    page = request.GET.get('page')
    products = p.get_page(page)

    context = {
        'product': product,
        'products': products,
        'category': category,
        'count': count(request),
        'url': footer(),
        'iletisim': iletisim(),
        'hakkimizda': hakkimizda(),
    }
    return render(request, 'index.html', context)  # HttpResponse(template.render(context,request))


# Category


def category(request, slug):
    product = Products.objects.filter(category__slug=slug).order_by('-id')
    p = Paginator(product, per_page=10)
    page = request.GET.get('page')
    products = p.get_page(page)
    template = loader.get_template('category.html')
    context = {
        'category': categories.objects.all().values(),
        'products': products,
        'url': footer(),
        'iletisim': iletisim(),
        'hakkimizda': hakkimizda(),
        'count': count(request),
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def cart(request):
    product = Products.objects.all()
    item = CartItem.objects.filter(cart__user=request.user)

    # quantity_sum=CartItem.objects.filter(user=request.user)
    # print(quantity_sum)# ürünlerin fiyatını topluyor adeti 1 olarak alıyor
    # print(type(quantity_sum))
    price_sum = CartItem.objects.filter(cart__user=request.user).aggregate(
        Sum('total_price')).get('total_price__sum')


    context = {
        'item': item,
        'product': product,
        'url': footer(),
        'iletisim': iletisim(),
        'hakkimizda': hakkimizda(),
        'count': count(request),
        'price_sum': price_sum,
    }
    return render(request, 'apps/cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, slug):
    item = get_object_or_404(Products,slug=slug)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            user=request.user,ordered_date=timezone.now()
        )
    cart_item, is_created = CartItem.objects.get_or_create(
        item=item,
        cart=cart,
    )
    if is_created==True:
        messages.info(request, "This item was added to your cart.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if is_created==False:
        cart_item.quantity += 1
        cart_item.total_price = item.price*cart_item.quantity
        cart_item.cart_item_price=item.price
        cart_item.save()
        messages.info(request, "This item was updated")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))









    # if add_to_cart:
    #     order = add_to_cart
    #     # check if the order item is in the order
    #
    #     if CartItem.objects.filter(item__slug=item.slug).exists():
    #         order_item.quantity += 1
    #         order_item.total_price = order_item.quantity * item.price
    #         print(order_item.total_price)
    #         order_item.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #     else:
    #         print('elseAltı')
    #         order.cart_item.add(order_item)
    #         messages.info(request, "This item was added to your add_to_cart.")
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = CartItem.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if CartItem.objects.filter(item__slug=item.slug).exists():
            order_item = CartItem.objects.filter(
                item=item,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.total_price = order_item.quantity * item.price
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def deleteCart(request, slug):
    product = Products.objects.get(slug=slug)
    cart_item = CartItem.objects.filter(item=product)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def cart_summary(request):
    cart_item=CartItem.objects.filter(cart__user=request.user)
    price_sum = cart_item.aggregate(
        Sum('total_price')).get('total_price__sum')
    context={
        'cart_item':cart_item,
        'price_sum':price_sum,
        'count':count(request),
        'url': footer(),
        'iletisim': iletisim(),
        'hakkimizda': hakkimizda(),
    }
    return render(request, 'apps/cart-summary.html', context)





def order(request):
    price_sum = CartItem.objects.filter(cart__user=request.user).aggregate(
        Sum('total_price')).get('total_price__sum')
    order_price_sum = Order.objects.filter(user=request.user).aggregate(
        Sum('order_total_price')).get('order_total_price__sum')

    try:
        cart_item = CartItem.objects.filter(cart__user=request.user)
        cart=Cart.objects.get(
            user=request.user)

    except CartItem.DoesNotExist:
        messages.warning(request, "You do not have an active order")
    except Cart.DoesNotExist:
        messages.warning(request, "You do not have an active order")
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone_no=request.POST['phone_no']
        _address=request.POST['address']
        city=request.POST['city']
        region=request.POST['region']
        zip_code=request.POST['zip-code']
        country=request.POST['country']
        user = User.objects.get(username=request.user)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if not Address.objects.filter(user=user).exists():
            address,is_created = Address.objects.get_or_create(
                user=user,
                phone=phone_no,
                address=_address,
                city=city,
                region=region,
                zip_code=zip_code,
                country=country,
            )
            if is_created == True:
                messages.info(request, "Adres kaydedildi")
                return HttpResponseRedirect(request.META.get('cart-summary.html', '/'))

        # else:
        #
        #     address= Address.objects.get(user=user)
        #     address.phone=phone_no
        #     address.address=_address
        #     address.city=city
        #     address.region=region
        #     address.zip_code=zip_code
        #     address.country=country
        #     address.save()
        #     messages.info(request, "adres güncellendi")
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))





    # for x in range(0, cart_item.count()):
    #
    #     order_item, created = OrderItem.objects.get_or_create(
    #         order=order,
    #         title=cart_item[x].item.title,
    #         price=cart_item[x].item.price,
    #         category=cart_item[x].item.category,
    #         urun_desc=cart_item[x].item.urun_desc,
    #         urun_foto=cart_item[x].item.urun_foto,
    #         quantity=cart_item[x].quantity,
    #     )
    #     order_item.total_price=order_item.price*cart_item[x].quantity
    #     order_item.save()
    #
    # if created == True:
    #     messages.info(request, "Siparişiniz Oluşturuldu.")
    #     cart.delete()
    #     cart_item.delete()
    #     order_price_sum = Order.objects.filter(user=request.user).aggregate(
    #         Sum('order_total_price')).get('order_total_price__sum')
    #     try:
    #         address=Address.objects.get(
    #             user=request.user,
    #         )
    #         context = {
    #             'address':Address.objects.get(user=request.user),
    #             'price_sum': order_price_sum,
    #             'order_item':OrderItem.objects.filter(order__user=request.user)
    #         }
    #
    #         return render(request, 'apps/order-summary.html', context)
    #     except Address.DoesNotExist:
    #         context = {
    #             'price_sum': order_price_sum
    #         }
    #         return render(request, 'apps/order-index.html', context)
    # if created == False:
    #     # order_item=OrderItem.objects.filter(order__user=request.user).delete()
    #
    #     print('false')
    #     for x in range(0, cart_item.count()):
    #
    #         order_item.order=order
    #         order_item.title=cart_item[x].item.title
    #         order_item.price=cart_item[x].item.price
    #         order_item.category=cart_item[x].item.category
    #         order_item.urun_desc=cart_item[x].item.urun_desc
    #         order_item.urun_foto=cart_item[x].item.urun_foto
    #         order_item.quantity += cart_item[x].quantity
    #
    #     order_item.save()
    #     cart.delete()
    #     cart_item.delete()



    try:
        address=Address.objects.get(
            user=request.user,
        )
        order, order_created = Order.objects.get_or_create(user=request.user)
        if order_created:
            order.order_total_price = price_sum
            order.save()

        if order_created == False:
            order.user = request.user
            if order.order_total_price is None:
                order.order_total_price = 0
                order.order_total_price = order.order_total_price + price_sum
            else:
                print('deneme')
                order.order_total_price = order.order_total_price + price_sum
                print(order.order_total_price)
            order.save()
        try:
            for x in range(0, cart_item.count()):
                order_item = OrderItem.objects.get(order=order, title=cart_item[x].item.title)
                order_item.quantity += cart_item[x].quantity
                order_item.total_price = order_item.price * order_item.quantity
                order_item.save()

            cart.delete()
            cart_item.delete()

        except OrderItem.DoesNotExist:

            for x in range(0, cart_item.count()):
                if OrderItem.objects.filter(order=order,title=cart_item[x].item.title).exists():
                    order_item = OrderItem.objects.get(order=order, title=cart_item[x].item.title)
                    order_item.quantity+=cart_item[x].quantity

                else:

                    order_item = OrderItem.objects.create(
                        order=order,
                        title=cart_item[x].item.title,
                        price=cart_item[x].item.price,
                        category=cart_item[x].item.category,
                        urun_desc=cart_item[x].item.urun_desc,
                        urun_foto=cart_item[x].item.urun_foto,
                    )
                    order_item.quantity=cart_item[x].quantity
                    order_item.total_price = order_item.price * order_item.quantity
                    order_item.save()
            messages.info(request, "Siparişiniz güncellendi.")
            cart.delete()
            cart_item.delete()
        context = {
            'address':Address.objects.get(user=request.user),
            'price_sum': order.order_total_price,
            'count': count(request),
            'order_item':OrderItem.objects.filter(order__user=request.user),
            'url': footer(),
            'iletisim': iletisim(),
            'hakkimizda': hakkimizda(),

        }
        messages.info(request, "Siparişiniz güncellendi.")
        return render(request, 'apps/order-summary.html', context)
    except Address.DoesNotExist:

        context = {
            'price_sum': order_price_sum,
            'url': footer(),
            'iletisim': iletisim(),
            'hakkimizda': hakkimizda(),

            'count': count(request),
        }
        return render(request, 'apps/order-index.html', context)



def order_summary(request):
    price_sum = Order.objects.filter(user=request.user).aggregate(
        Sum('order_total_price')).get('order_total_price__sum')
    try:

        address=Address.objects.get(user=request.user)
        order=OrderItem.objects.filter(order__user=request.user)

        context = {
            'order_item': order,
            'price_sum': price_sum,
            'address': address,
            'count':count(request),
            'url': footer(),
            'iletisim': iletisim(),
            'hakkimizda': hakkimizda(),
        }

        return render(request, 'apps/order-summary.html', context)
    except Order.DoesNotExist:
        messages.warning(request, "Siparişiniz yoktur")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Address.DoesNotExist:
        messages.warning(request, "Siparişiniz yoktur")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))






def product(request,slug):
    product = Products.objects.filter(slug=slug)

    image=Image.objects.filter(product__slug=slug)

    context = {
        'product':product,
        'image': image,
        'count':count(request),
        'url': footer(),
        'iletisim': iletisim(),
        'hakkimizda': hakkimizda(),
    }
    return render(request, 'apps/product.html', context)

# def product_update(request):
#     product = Products.objects.all().values()
#     template = loader.get_template('apps/product-update.html')
#     context = {
#         'product': product,
#     }
#     return HttpResponse(template.render(context, request))

# def table(request):
#     product = products.objects.all().values()
#     category= categories.objects.all().values()
#     template= loader.get_template('apps/table.html')
#     context = {
#         'product': product, 'category':category
#     }
#     return HttpResponse(template.render(context,request))


# def dashboard(request):
#     template = loader.get_template('dashboard/dashboard.html')
#     context={
#     }
#     return HttpResponse(template.render(context,request))


# #Productt


# def add(request):
#     template = loader.get_template('apps/add.html')
#     return HttpResponse(template.render({},request))


# def addRecord(request):
#     urunAdi= request.POST['urunAdi']
#     urunFiyat = request.POST['urunFiyat']
#     categoryID= request.POST['categoryID']
#     urunDesc = request.POST['urunDesc']
#     urunFoto = request.POST['urunFoto']
#     #foto copy
#     path="C:\\Users\\mehme\\Desktop\\fotoEkleme\\"+urunFoto
#     destination ="C:\\Users\\mehme\\Desktop\\djangoDeneme\\saplament\\base\\static\\images\\"+urunFoto
#     shutil.copyfile(path,destination)

#     product = products(
#         urun_adi=urunAdi,
#         urun_fiyat=urunFiyat,
#         category_name=categoryID,
#         urun_desc=urunDesc,
#         urun_foto=urunFoto

#     )
#     product.save()
#     messages.info(request, 'Added successfully!')
#     return HttpResponseRedirect(reverse('add'))

# def update(request,id):
#     product = products.objects.get(id=id)
#     template = loader.get_template('apps/update.html')
#     context = {
#         'product':product
#     }
#     return HttpResponse(template.render(context,request))

# def updateRecord(request,id):

#     product = products.objects.get(id=id)
#     urunAdi=request.POST['urunAdi']
#     urunFiyat=request.POST['urunFiyat']
#     urunCategory=request.POST['categoryID']
#     urunDesc=request.POST['urunDesc']
#     urunFoto= request.POST['urunFoto']
#     product.urun_adi=urunAdi
#     product.urun_fiyat=urunFiyat
#     product.category_name=urunCategory
#     product.urun_desc = urunDesc
#     product.urun_foto=urunFoto
#     try:
#     #copy foto
#         path="C:\\Users\\mehme\\Desktop\\fotoEkleme\\"+urunFoto
#         destination ="C:\\Users\\mehme\\Desktop\\djangoDeneme\\saplament\\base\\static\\images\\"+urunFoto
#         shutil.copyfile(path,destination)
#     except:
#         print('')
#     product.save()
#     return HttpResponseRedirect(reverse('index'))


# def delete(request,id):
#     product = products.objects.get(id=id)
#     product.delete()
#     return HttpResponseRedirect(reverse('table'))


# def addCategory(request):
#     template = loader.get_template('apps/add-category.html')
#     return HttpResponse(template.render({},request))


# def addCategoryRecord(request):
#     categoryName= request.POST['categoryName']
#     category = categories(
#         category_name=categoryName

#     )
#     category.save()
#     return HttpResponseRedirect(reverse('table'))

# def categoryUpdate(request,id):
#     category = categories.objects.get(id=id)
#     template = loader.get_template('apps/update-category.html')
#     context = {
#         'category':category
#     }
#     return HttpResponse(template.render(context,request))


# def categoryUpdateRecord(request,id):
#     category = categories.objects.get(id=id)
#     catID = request.POST['catID']
#     categoryName=request.POST['categoryName']
#     category.delete()
#     category.category_name=categoryName
#     category.id=catID
#     category.save()
#     return HttpResponseRedirect(reverse('table'))


# def categoryDelete(request,id):
#     category = categories.objects.get(id=id)
#     category.delete()
#     return HttpResponseRedirect(reverse('table'))




