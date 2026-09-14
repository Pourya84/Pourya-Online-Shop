from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from store.models import UserProfile, Category
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore

class BaseApiTest(APITestCase):
    def setUp(self):
        # کاربران
        self.buyer_user = User.objects.create_user(username="buyer", password="12345")
        self.seller_user = User.objects.create_user(username="seller", password="12345")
        
        # پروفایل‌ها
        self.buyer_profile = UserProfile.objects.create(
            user=self.buyer_user, role="buyer", name="Buyer"
        )
        self.seller_profile = UserProfile.objects.create(
            user=self.seller_user, role="seller", name="Seller", is_approved=True
        )
        
        # دسته‌بندی‌ها
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Books")
        
        # JWT Tokens
        self.buyer_token = str(RefreshToken.for_user(self.buyer_user).access_token)
        self.seller_token = str(RefreshToken.for_user(self.seller_user).access_token)