from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Max, Q, Prefetch
from django.utils import timezone
from datetime import timedelta

from .models import (
    Product,
    Order,
    OrderItem,
    ProductLike,
    Category,
    cleanup_orphan_categories,
)
from .forms import ProductForm, CommentForm
from .services.product_service import ProductService
from .services.cart_service import CartService
from core.utils import safe_redirect_url


# ======================== STORE PAGE (with optimizations) ========================
def store(request):
    products_page = ProductService.get_filtered_products(request)

    # Optimize category query: only fetch id and name (product_count is an annotation)
    categories_list = (
        Category.objects
        .annotate(product_count=Count('products'))
        .only('id', 'name')           # فقط فیلدهای واقعی را مشخص کن
        .order_by('-product_count')
    )

    max_price = Product.objects.aggregate(max_price=Max('price'))['max_price'] or 1000

    min_price = request.GET.get('min_price')
    max_price_filter = request.GET.get('max_price')
    selected_categories = request.GET.getlist('category')

    context = {
        "products": products_page,
        "categories": categories_list,
        "selected_categories": selected_categories,
        "max_price": int(max_price),
        "min_price": min_price,
        "max_price_filter": max_price_filter,
    }

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            order, _ = Order.objects.get_or_create(customer=profile, complete=False)
            context["order"] = order
        except Exception:
            pass

    return render(request, "store/store_panel.html", context)

# ======================== SHOPPING CART ========================
def cart(request):
    context = {}
    if request.user.is_authenticated:
        profile = request.user.profile
        # Optimize: fetch order with related items and product data in one go
        order, _ = Order.objects.get_or_create(customer=profile, complete=False)
        items = (
            OrderItem.objects
            .filter(order=order)
            .select_related('product')
            .only('id', 'quantity', 'price_at_purchase', 'product__id', 'product__name', 
                  'product__price', 'product__image', 'product__is_available')
        )
        context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


# ======================== CHECKOUT ========================
def checkout(request):
    context = {}
    if request.user.is_authenticated:
        profile = request.user.profile
        order, _ = Order.objects.get_or_create(customer=profile, complete=False)
        # Same optimization as cart
        items = (
            OrderItem.objects
            .filter(order=order)
            .select_related('product')
            .only('id', 'quantity', 'price_at_purchase', 'product__id', 'product__name', 
                  'product__price', 'product__image')
        )
        context = {"items": items, "order": order}
    return render(request, "store/checkout.html", context)


# ======================== SELLER UTILITY ========================
def is_seller(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "seller"
    )


# ======================== SELLER PANEL (optimized) ========================
@user_passes_test(is_seller)
def seller_panel(request):
    # Clean up orphan categories on each load
    cleanup_orphan_categories()

    profile = request.user.profile

    if not profile.is_approved:
        messages.error(request, "Your seller account is not approved.")
        return redirect("store:store_panel")

    # Handle product creation
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = profile
            product.save()
            product.categories.set(form.cleaned_data["categories"])
            cleanup_orphan_categories()
            return redirect(safe_redirect_url(request, "store:store_panel"))
    else:
        form = ProductForm()

    # Optimize seller's product list: select only necessary fields
    products = (
        Product.objects
        .filter(seller=profile)
        .select_related('seller')
        .prefetch_related(
            Prefetch('categories', queryset=Category.objects.only('id', 'name'))
        )
        .only(
            'id', 'name', 'price', 'digital', 'description', 'image',
            'is_available', 'date_added', 'seller__id', 'seller__name'
        )
        .order_by('-date_added')
    )

    return render(
        request,
        "store/seller_panel.html",
        {"form": form, "products": products}
    )


# ======================== EDIT PRODUCT ========================
@user_passes_test(is_seller)
def edit_product(request, product_id):
    profile = request.user.profile
    product = get_object_or_404(Product, id=product_id, seller=profile)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            product.categories.set(form.cleaned_data["categories"])
            cleanup_orphan_categories()
            return redirect(safe_redirect_url(request, "store:store_panel"))
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "store/edit_product.html",
        {"form": form, "product": product}
    )


# ======================== ADD / REMOVE FROM CART ========================
@login_required
def update_cart_item(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available:
        messages.error(request, "این محصول موجود نیست.")
        return redirect(request.POST.get("next", "store:store_panel"))

    CartService.update_cart(request.user.profile, product, action)
    return redirect(request.POST.get("next", "store:cart"))


# ======================== DELETE PRODUCT ========================
@user_passes_test(is_seller)
def delete_product(request, product_id):
    profile = request.user.profile
    product = get_object_or_404(Product, id=product_id, seller=profile)
    product.delete()
    cleanup_orphan_categories()
    return redirect("store:store_panel")


# ======================== LIKE / UNLIKE PRODUCT ========================
@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    like, created = ProductLike.objects.get_or_create(
        user=request.user.profile,
        product=product
    )
    if not created:
        like.delete()
    return redirect(safe_redirect_url(request, "store:store_panel"))


# ======================== ADD COMMENT ========================
@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user.profile
            comment.save()

    return redirect(safe_redirect_url(request, "store:store_panel"))


# ======================== ADD CATEGORY (standalone) ========================
@login_required
@user_passes_test(is_seller)
def add_category_standalone(request):
    if request.method == "POST":
        cat_name = request.POST.get("new_category_name", "").strip()
        if 2 <= len(cat_name) <= 50:
            Category.objects.get_or_create(name=cat_name)

    return redirect(safe_redirect_url(request, "store:store_panel"))


# ======================== HOMEPAGE (optimized) ========================
def homepage(request):
    yesterday = timezone.now() - timedelta(days=1)

    # New products: only necessary fields, with prefetched categories
    new_products = (
        Product.objects
        .select_related('seller')
        .prefetch_related(
            Prefetch('categories', queryset=Category.objects.only('id', 'name'))
        )
        .filter(date_added__gte=yesterday)
        .only(
            'id', 'name', 'price', 'image', 'description',
            'date_added', 'is_available', 'seller__id', 'seller__name'
        )
        .order_by('-date_added')[:8]
    )

    # Most liked products: annotated with like count, only necessary fields
    most_liked_products = (
        Product.objects
        .select_related('seller')
        .prefetch_related(
            Prefetch('categories', queryset=Category.objects.only('id', 'name'))
        )
        .annotate(like_count=Count('productlike'))
        .only(
            'id', 'name', 'price', 'image', 'description',
            'date_added', 'is_available', 'seller__id', 'seller__name'
        )
        .order_by('-like_count')[:8]
    )

    context = {
        "new_products": new_products,
        "most_liked_products": most_liked_products,
    }

    # Add order for authenticated users
    if request.user.is_authenticated:
        profile = request.user.profile
        order, _ = Order.objects.get_or_create(customer=profile, complete=False)
        context["order"] = order

    return render(request, "store/homepage.html", context)


# ======================== LIKED PRODUCTS PAGE ========================
@login_required
def liked_products(request):
    profile = request.user.profile

    # Optimize liked products query
    liked_products = (
        Product.objects
        .select_related('seller')
        .prefetch_related(
            Prefetch('categories', queryset=Category.objects.only('id', 'name'))
        )
        .filter(productlike__user=profile)
        .only(
            'id', 'name', 'price', 'image', 'description',
            'date_added', 'is_available', 'seller__id', 'seller__name'
        )
        .order_by('-date_added')
    )

    order, _ = Order.objects.get_or_create(customer=profile, complete=False)
    context = {
        "products": liked_products,
        "order": order,
    }

    return render(request, "store/liked_products.html", context)