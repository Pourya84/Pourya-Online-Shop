from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import LogoutView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 
    path("", views.store, name="store"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('update_cart_item/<int:product_id>/<str:action>/', views.update_cart_item, name='update_cart_item'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('seller-panel/', views.seller_panel, name='seller_panel'),
    path('seller-panel/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller-panel/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('change-password/', PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='change_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
]
