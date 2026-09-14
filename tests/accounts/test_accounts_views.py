import pytest
from django.urls import reverse
from django.contrib.auth.models import User  # ← اضافه کردن import
from store.models import UserProfile

@pytest.mark.integration
class TestAccountsViews:
    def test_login_view(self, client):
        response = client.get(reverse("accounts:login"))
        assert response.status_code == 200

    def test_register_view(self, client):
        response = client.get(reverse("accounts:register"))
        assert response.status_code == 200

    def test_register_post_creates_user(self, client):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "role": "buyer"
        }
        response = client.post(reverse("accounts:register"), data)
        assert response.status_code == 302  # redirect after login
        user = User.objects.get(username="testuser")
        assert user.email == "test@example.com"
        profile = user.profile
        assert profile.role == "buyer"

    def test_change_password_requires_login(self, client):
        response = client.get(reverse("accounts:change_password"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_change_password_authenticated(self, authenticated_client):
        response = authenticated_client.get(reverse("accounts:change_password"))
        assert response.status_code == 200

    def test_password_reset_view(self, client):
        response = client.get(reverse("accounts:password_reset"))
        assert response.status_code == 200