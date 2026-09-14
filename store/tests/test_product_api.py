# store/tests/test_product_api.py
from rest_framework import status
from store.models import Product, UserProfile
from .base_api import BaseApiTest
from django.contrib.auth.models import User


class ProductApiTests(BaseApiTest):
    """
    تست کامل ProductViewSet
    پوشش CRUD، Permissions و Validation
    """

    def setUp(self):
        super().setUp()

        # یک محصول اولیه برای تست
        self.product = Product.objects.create(
            seller=self.seller_profile,
            name="Phone",
            price=500,
            digital=False,
            description="Test product",
        )
        self.product.categories.add(self.category1)

    # ==================================================
    # LIST
    # ==================================================
    def test_product_list(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ==================================================
    # RETRIEVE
    # ==================================================
    def test_product_detail(self):
        response = self.client.get(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Phone")

    # ==================================================
    # CREATE
    # ==================================================
    def test_seller_can_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.post(
            "/api/products/",
            {
                "name": "Laptop",
                "price": 1000,
                "digital": False,
                "description": "Gaming Laptop",
                "categories": [self.category1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["seller_name"], "Seller")
        self.assertTrue(Product.objects.filter(name="Laptop").exists())

    def test_buyer_cannot_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        response = self.client.post(
            "/api/products/",
            {
                "name": "Laptop",
                "price": 1000,
                "digital": False,
                "categories": [self.category1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_create_product(self):
        response = self.client.post(
            "/api/products/",
            {
                "name": "Laptop",
                "price": 1000,
                "digital": False,
                "categories": [self.category1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_name_validation(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.post(
            "/api/products/",
            {
                "name": "aa",
                "price": 100,
                "digital": False,
                "categories": [self.category1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    # ==================================================
    # UPDATE
    # ==================================================
    def test_owner_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.patch(
            f"/api/products/{self.product.id}/", {"price": 999}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(float(self.product.price), 999.0)

    def test_partial_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.patch(
            f"/api/products/{self.product.id}/",
            {"description": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, "Updated")

    def test_seller_cannot_edit_other_product(self):
        other_user = User.objects.create_user(username="seller2", password="12345")
        other_profile = UserProfile.objects.create(
            user=other_user, role="seller", name="Seller2"
        )
        other_product = Product.objects.create(
            seller=other_profile, name="Other Product", price=100
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.patch(
            f"/api/products/{other_product.id}/", {"price": 999}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==================================================
    # DELETE
    # ==================================================
    def test_owner_can_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_buyer_cannot_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==================================================
    # AVAILABILITY FILTER
    # ==================================================
    def test_unavailable_product_not_listed(self):
        Product.objects.create(
            seller=self.seller_profile, name="Hidden", price=100, is_available=False
        )
        response = self.client.get("/api/products/")
        names = [p["name"] for p in response.data]
        self.assertNotIn("Hidden", names)
