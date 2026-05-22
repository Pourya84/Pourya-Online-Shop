from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    role = models.CharField(
        max_length=10,
        choices=[("buyer", "خریدار"), ("seller", "فروشنده")],
        default="buyer",
    )

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="seller_profile"
    )
    store_name = models.CharField(max_length=200, verbose_name="نام فروشگاه")
    store_description = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(
        default=False, verbose_name="تایید شده توسط ادمین؟"
    )

    def __str__(self):
        return self.store_name


class Product(models.Model):

    seller = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products",
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_orderd = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_Price(self):
        orderItem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItem])
        return total

    @property
    def get_tota_lItem(self):
        orderItem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItem])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipecode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
