# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import Product, Customer, Order, OrderItem
from .forms import ProductForm


def store(request):
    products = Product.objects.select_related("seller").all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context = {"order": order, "products": products}
    else:
        context = {"products": products}
    return render(request, "store/store.html", context)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not self.request.POST.get("remember_me"):
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("store")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get("role", "buyer")
            customer = Customer.objects.create(
                user=user, name=user.username, email=user.email, role=role
            )
            if role == "seller":
                group, _ = Group.objects.get_or_create(name="Sellers")
                user.groups.add(group)
            else:
                group, _ = Group.objects.get_or_create(name="Buyers")
                user.groups.add(group)
            auth_login(request, user)
            return redirect("store")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        context = {"items": items, "order": order}
    else:
        context = {}
    return render(request, "store/cart.html", context)


@login_required
def update_cart_item(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product, defaults={"quantity": 0}
    )
    if action == "increase":
        order_item.quantity += 1
    elif action == "decrease":
        order_item.quantity -= 1
    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        context = {"items": items, "order": order}
    else:
        context = {}
    return render(request, "store/checkout.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {"product": product}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context["order"] = order
    return render(request, "store/product_detail.html", context)


def is_seller(user):
    return (
        user.is_authenticated
        and hasattr(user, "customer")
        and user.customer.role == "seller"
    )


@user_passes_test(is_seller)
def seller_panel(request):
    customer = request.user.customer
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = customer
            product.save()
            return redirect("seller_panel")
    else:
        form = ProductForm()

    products = Product.objects.filter(seller=customer)
    return render(
        request, "accounts/seller_panel.html", {"form": form, "products": products}
    )


@user_passes_test(is_seller)
def edit_product(request, product_id):
    customer = request.user.customer
    product = get_object_or_404(Product, id=product_id, seller=customer)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("seller_panel")
    else:
        form = ProductForm(instance=product)

    return render(
        request, "store/edit_product.html", {"form": form, "product": product}
    )


@user_passes_test(is_seller)
def delete_product(request, product_id):
    customer = request.user.customer
    product = get_object_or_404(Product, id=product_id, seller=customer)
    product.delete()
    return redirect("seller_panel")
