import pytest
from django.core.exceptions import ValidationError
from store.models import Category, Product, UserProfile, Order, OrderItem
from store.validators import validate_product_price

@pytest.mark.unit
class TestCategory:
    def test_category_str(self, create_category):
        category = create_category("Electronics")
        assert str(category) == "Electronics"

    def test_category_unique_name(self, create_category):
        create_category("UniqueCat")
        with pytest.raises(Exception):
            create_category("UniqueCat")

@pytest.mark.unit
class TestUserProfile:
    def test_profile_creation(self, create_user):
        user, profile = create_user(username="alireza", email="ali@example.com", role="seller")
        assert profile.role == "seller"
        assert str(profile) == "alireza"

    def test_profile_str_with_name(self, create_user):
        user, profile = create_user(username="testuser")
        profile.name = "Ali Reza"
        profile.save()
        assert str(profile) == "Ali Reza"

@pytest.mark.unit
class TestProduct:
    def test_product_creation(self, create_product):
        product = create_product(name="Laptop", price=1500.00)
        assert product.name == "Laptop"
        assert product.price == 1500.00
        assert product.is_available is True

    def test_product_image_url_empty(self, create_product):
        product = create_product()
        product.image = None
        assert product.imageURL == ""

    def test_product_str(self, create_product):
        product = create_product(name="Smartphone")
        assert str(product) == "Smartphone"

    def test_product_price_validator(self):
        with pytest.raises(ValidationError):
            validate_product_price(0)

        try:
            validate_product_price(100)
        except ValidationError:
            pytest.fail("validate_product_price raised ValidationError for positive price")

@pytest.mark.unit
class TestOrder:
    def test_order_total_price(self, create_user, create_product):
        user, profile = create_user(username="orderuser")
        order = Order.objects.create(customer=profile)
        product1 = create_product(name="Item1", price=100)
        product2 = create_product(name="Item2", price=50)
        OrderItem.objects.create(product=product1, order=order, quantity=2, price_at_purchase=100)
        OrderItem.objects.create(product=product2, order=order, quantity=1, price_at_purchase=50)
        assert order.get_total_price == 250

    def test_order_total_items(self, create_user, create_product):
        user, profile = create_user(username="orderuser2")
        order = Order.objects.create(customer=profile)
        product1 = create_product(name="TestProduct1")
        product2 = create_product(name="TestProduct2")
        OrderItem.objects.create(product=product1, order=order, quantity=3, price_at_purchase=100)
        OrderItem.objects.create(product=product2, order=order, quantity=2, price_at_purchase=100)
        assert order.get_total_items == 5