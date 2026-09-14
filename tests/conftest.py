import pytest
from django.test import Client
from django.contrib.auth.models import User
from store.models import UserProfile, Category, Product

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def create_user(db):
    counter = 0
    def make_user(username=None, password="testpass123", email=None, role="buyer"):
        nonlocal counter
        if username is None:
            username = f"testuser_{counter}"
            counter += 1
        if email is None:
            email = f"{username}@example.com"
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        profile = UserProfile.objects.create(
            user=user,
            name=username,
            email=email,
            role=role,
            is_approved=True if role == "seller" else False
        )
        return user, profile
    return make_user

@pytest.fixture
def create_category(db):
    def make_category(name="Test Category"):
        return Category.objects.create(name=name)
    return make_category

@pytest.fixture
def create_product(db, create_user, create_category):
    # نگهداری یک فروشنده ثابت برای جلوگیری از تکرار نام کاربری
    seller_profile = None

    def make_product(
        name="Test Product",
        price=100.00,
        digital=False,
        description="Test description",
        is_available=True,
        seller=None,
        categories=None
    ):
        nonlocal seller_profile
        if seller is None:
            if seller_profile is None:
                _, seller_profile = create_user(username="fixed_seller", role="seller")
            profile = seller_profile
        else:
            profile = seller

        product = Product.objects.create(
            seller=profile,
            name=name,
            price=price,
            digital=digital,
            description=description,
            is_available=is_available
        )
        if categories:
            product.categories.set(categories)
        return product
    return make_product

# بقیه فیکسچرها بدون تغییر
@pytest.fixture
def authenticated_client(client, create_user):
    user, _ = create_user()
    client.force_login(user)
    return client

@pytest.fixture
def seller_client(client, create_user):
    user, _ = create_user(username="selleruser", role="seller")
    client.force_login(user)
    return client