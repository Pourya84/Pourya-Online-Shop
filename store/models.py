from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from .validators import validate_product_price


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = [("buyer", "خریدار"), ("seller", "فروشنده")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="buyer")
    store_name = models.CharField(max_length=200, blank=True, null=True)
    store_description = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name or self.user.username


class Product(models.Model):
    seller = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_product_price],
    )
    digital = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="products")
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name="موجود")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ""


class Order(models.Model):
    customer = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_total_price(self):
        items = self.orderitem_set.all()
        total = sum(item.get_total for item in items)
        return total

    @property
    def get_total_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        return self.price_at_purchase * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)


class ProductLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"نظر {self.user.name} برای {self.product.name}"


def cleanup_orphan_categories():
    Category.objects.annotate(product_count=Count("products")).filter(
        product_count=0
    ).delete()