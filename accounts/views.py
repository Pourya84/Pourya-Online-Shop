# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib import messages

from store.models import UserProfile
from core.utils import safe_redirect_url
from .forms import CustomUserCreationForm, CustomPasswordResetForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not self.request.POST.get("remember_me"):
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def get_success_url(self):
        return safe_redirect_url(self.request, reverse_lazy("store:store_panel"))


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Save the email in the User model
            user.email = form.cleaned_data['email']
            user.save()

            role = request.POST.get("role", "buyer")
            allowed_roles = [choice[0] for choice in UserProfile.ROLE_CHOICES]
            if role not in allowed_roles:
                role = "buyer"

            profile = UserProfile.objects.create(
                user=user,
                name=user.username,
                email=user.email,  # Also save the email in the profile
                role=role,
                store_name=(
                    request.POST.get("store_name", "") if role == "seller" else ""
                ),
            )

            if role == "seller":
                group, _ = Group.objects.get_or_create(name="Sellers")
            else:
                group, _ = Group.objects.get_or_create(name="Buyers")
            user.groups.add(group)

            auth_login(request, user)
            return redirect(safe_redirect_url(request, "store:store_panel"))
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def change_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
            return redirect(safe_redirect_url(request, "store:store_panel"))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})


# ========== Password reset views with a custom form ==========

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(self.request, 'لینک بازنشانی رمز عبور برای شما ارسال شد.')
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'