# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="store:store_panel"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("change-password/", views.change_password, name="change_password"),
    
    # ===== مسیرهای بازنشانی رمز عبور =====
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]