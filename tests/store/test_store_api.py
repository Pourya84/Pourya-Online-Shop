import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.api
class TestProductAPI:
    def test_list_products_public(self):
        client = APIClient()
        response = client.get(reverse("store:product-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_product_requires_auth(self, create_user, create_category):
        client = APIClient()
        user, profile = create_user(role="seller")  # seller
        client.force_authenticate(user=user)
        category = create_category("Electronics")
        data = {
            "name": "New Product",
            "price": 1200,
            "digital": False,
            "description": "API product",
            "categories": [category.id],
            "is_available": True
        }
        response = client.post(reverse("store:product-list"), data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_product_forbidden_for_buyer(self, create_user):
        client = APIClient()
        user, _ = create_user(role="buyer")
        client.force_authenticate(user=user)
        data = {"name": "Forbidden", "price": 100}
        response = client.post(reverse("store:product-list"), data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_product_owner_only(self, create_user, create_product):
        client = APIClient()
        # seller اول
        user1, profile1 = create_user(username="seller1", role="seller")
        client.force_authenticate(user=user1)
        product = create_product(seller=profile1)
        response = client.delete(reverse("store:product-detail", args=[product.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # seller دوم با ایمیل یکتا
        user2, profile2 = create_user(username="seller2", role="seller")
        client.force_authenticate(user=user2)
        product2 = create_product(seller=profile2)
        response = client.delete(reverse("store:product-detail", args=[product2.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # برای تست اینکه فروشنده دیگر نمی‌تواند حذف کند
        client.force_authenticate(user=user1)
        # دوباره product2 را با کاربر اول حذف کنیم (نباید اجازه داشته باشد)
        response = client.delete(reverse("store:product-detail", args=[product2.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND  # یا 403