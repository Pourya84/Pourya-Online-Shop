from django.urls import path
from . import views_api, views_web
from rest_framework.routers import DefaultRouter

app_name = "store"

router = DefaultRouter()
router.register(r"api/products", views_api.ProductViewSet)
router.register(r"api/orders", views_api.OrderViewSet, basename="orders")
router.register(r"api/profiles", views_api.UserProfileViewSet, basename="profiles")

urlpatterns = [
    path("", views_web.homepage, name="homepage"),
    path("store/", views_web.store, name="store_panel"),
    path("store/cart", views_web.cart, name="cart"),
    path("store/checkout", views_web.checkout, name="checkout"),
    path(
        "store/update_cart_item/<int:product_id>/<str:action>/",
        views_web.update_cart_item,
        name="update_cart_item",
    ),
    path("store/seller-panel/", views_web.seller_panel, name="seller_panel"),
    path(
        "store/seller-panel/edit/<int:product_id>/",
        views_web.edit_product,
        name="edit_product",
    ),
    path(
        "store/seller-panel/delete/<int:product_id>/",
        views_web.delete_product,
        name="delete_product",
    ),
    path("store/like/<int:product_id>/", views_web.like_product, name="like_product"),
    path(
        "store/product/<int:product_id>/comment/",
        views_web.add_comment,
        name="add_comment",
    ),
    path(
        "add-category/",
        views_web.add_category_standalone,
        name="add_category_standalone",
    ),
    path("liked/", views_web.liked_products, name="liked_products"),
]

urlpatterns += router.urls