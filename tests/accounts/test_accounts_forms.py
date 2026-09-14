import pytest
from accounts.forms import CustomUserCreationForm, CustomPasswordResetForm
from store.models import UserProfile
from django.contrib.auth.models import User

@pytest.mark.unit
class TestAccountsForms:
    def test_custom_user_creation_form_valid(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }
        form = CustomUserCreationForm(data)
        assert form.is_valid()

    def test_custom_user_creation_form_missing_email(self):
        data = {
            "username": "newuser",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }
        form = CustomUserCreationForm(data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_password_reset_form_finds_user_via_profile(self, create_user):
        user, profile = create_user(email="ali@test.com")
        form = CustomPasswordResetForm(data={"email": "ali@test.com"})
        assert form.is_valid()
        users = form.get_users("ali@test.com")
        assert len(users) == 1
        assert users[0] == user