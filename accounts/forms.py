# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from store.models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید...'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن کلاس‌های Bootstrap به فیلدها
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label


class CustomPasswordResetForm(PasswordResetForm):
    """
    فرم بازنشانی رمز عبور که ایمیل را در UserProfile جستجو می‌کند
    """
    email = forms.EmailField(
        label='ایمیل',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید...'})
    )

    def get_users(self, email):
        """جستجوی کاربر با ایمیل در UserProfile و سپس User"""
        # جستجو در UserProfile
        try:
            profile = UserProfile.objects.get(email=email)
            return [profile.user]
        except UserProfile.DoesNotExist:
            # جستجو در User
            try:
                return [User.objects.get(email=email)]
            except User.DoesNotExist:
                return []