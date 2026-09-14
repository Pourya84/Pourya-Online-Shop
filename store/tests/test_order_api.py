# store/tests/test_order_api.py
from rest_framework import status
from store.models import Order, Product
from .base_api import BaseApiTest

class OrderApiTests(BaseApiTest):
    """
    تست کامل OrderViewSet
    پوشش List, Retrieve, Owner Permissions و دسترسی غیرمجاز
    """

    def setUp(self):
        super().setUp()

        # یک سفارش برای خریدار
        self.order = Order.objects.create(customer=self.buyer_profile)

        # یک محصول برای اضافه کردن به سفارش
        self.product = Product.objects.create(
            seller=self.seller_profile,
            name="Phone",
            price=100,
            digital=False
        )

    # ==================================================
    # LIST
    # ==================================================
    def test_order_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_list_unauthenticated(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================================================
    # RETRIEVE
    # ==================================================
    def test_order_retrieve_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)

    def test_order_retrieve_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_retrieve_anonymous(self):
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)