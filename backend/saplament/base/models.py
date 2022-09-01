from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from django.utils.text import slugify

fs = FileSystemStorage(location='/static/images')

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class categories(models.Model):
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.category_name


def categories_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.category_name)


pre_save.connect(categories_pre_save, sender=categories)


def categories_post_save(sender, created, instance, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.category_name)
        instance.save()


post_save.connect(categories_post_save, sender=categories)


class Products(models.Model):
    title = models.CharField(max_length=200, verbose_name='Ürün Adı')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ürün Fiyatı')
    category = models.ForeignKey(categories, on_delete=models.CASCADE, related_name='products_category')
    urun_desc = models.CharField(max_length=200, verbose_name='Ürün Açıklaması')
    urun_foto = models.ImageField(storage=fs, max_length=200, verbose_name='Index Foto')
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("views.product/", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("/add-to-cart/", kwargs={
            'slug': self.slug
        })


def products_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)


pre_save.connect(products_pre_save, sender=Products)


def products_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.title)
        instance.save()


post_save.connect(products_post_save, sender=Products)


class Image(models.Model):
    product_image = models.ImageField(storage=fs, max_length=200, verbose_name='Ürün Fotoğraf')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='product_image')


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_user')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}\'in sepeti'.format(self.user)


class CartItem(models.Model):
    item = models.ForeignKey(Products, related_name='items', on_delete=models.CASCADE)

    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    total_price = models.DecimalField(max_digits=10,
                                      blank=True,
                                      null=True,
                                      decimal_places=2,
                                      verbose_name='Total Fiyat', )

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


def cart_item_pre_save(sender, instance, *args, **kwargs):
    print(instance.item.price)
    if instance.total_price is None:
        instance.total_price = slugify(int(instance.item.price))


pre_save.connect(cart_item_pre_save, sender=CartItem)


def cart_item_post_save(created, instance, *args, **kwargs):
    if created:
        instance.total_price = instance.item.price
        instance.save()


post_save.connect(cart_item_post_save, sender=CartItem)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='address')
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='order_user')
    order_total_price = models.DecimalField(max_digits=10,
                                            blank=True,
                                            null=True,
                                            decimal_places=2,
                                            verbose_name='Total Fiyat', )

    def __str__(self):
        return '{0}\'in siparişi'.format(self.user)


class OrderItem(models.Model):
    title = models.CharField(max_length=200, verbose_name='Ürün Adı', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Ürün Fiyatı', blank=True)
    category = models.ForeignKey(categories, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='order_item_category')
    urun_desc = models.CharField(max_length=200, verbose_name='Ürün Açıklaması', null=True, blank=True)
    urun_foto = models.ImageField(max_length=200, verbose_name='Index Foto', null=True, blank=True)
    quantity = models.IntegerField(default=1)
    slug = models.SlugField(null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=10,
                                      blank=True,
                                      null=True,
                                      decimal_places=2,
                                      verbose_name='Total Fiyat',
                                      )

    def __str__(self):
        return '{0}\'in siparişi'.format(self.order.user)


def OrderItem_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)


pre_save.connect(OrderItem_pre_save, sender=OrderItem)


def OrderItem_post_save(created, instance, *args, **kwargs):
    if created:
        instance.total_price = instance.price * instance.quantity

        instance.save()


post_save.connect(OrderItem_post_save, sender=OrderItem)


class FooterURL(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name='Adı')
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title


class Iletisim(models.Model):
    name = models.CharField(max_length=300, null=True, verbose_name='Alan Adı')
    field = models.CharField(max_length=300, null=True, verbose_name='Alan')
    icon = models.CharField(max_length=200, null=True, verbose_name='İKON')

    def __str__(self):
        return self.name


class Hakkimizda(models.Model):
    name = models.CharField(max_length=300, null=True, verbose_name='Alan Adı')
    field = models.CharField(max_length=300, null=True, verbose_name='Alan')
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
