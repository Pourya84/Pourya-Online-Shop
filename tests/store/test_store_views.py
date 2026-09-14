# tests/store/test_store_views.py
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
import io
from store.models import Product


@pytest.mark.integration
class TestStoreViews:
    def test_homepage_public(self, client, create_product):
        create_product(name="Product1")
        create_product(name="Product2")
        create_product(name="Product3")

        response = client.get(reverse("store:homepage"))
        assert response.status_code == 200
        assert "new_products" in response.context
        assert "most_liked_products" in response.context
        assert len(response.context["new_products"]) > 0

    def test_store_panel_authenticated(self, authenticated_client, create_product):
        create_product(name="Product1")
        create_product(name="Product2")
        response = authenticated_client.get(reverse("store:store_panel"))
        assert response.status_code == 200
        assert len(response.context["products"]) > 0

    def test_cart_empty(self, client):
        response = client.get(reverse("store:cart"))
        assert response.status_code == 200

    def test_cart_authenticated(self, authenticated_client):
        response = authenticated_client.get(reverse("store:cart"))
        assert response.status_code == 200
        assert "order" in response.context

    def test_seller_panel_requires_seller(self, client):
        response = client.get(reverse("store:seller_panel"))
        assert response.status_code == 302

    def test_seller_panel_access_seller(self, seller_client):
        response = seller_client.get(reverse("store:seller_panel"))
        assert response.status_code == 200
        assert "form" in response.context
        assert "products" in response.context

    def test_like_product_authenticated(self, authenticated_client, create_product):
        product = create_product()
        response = authenticated_client.post(reverse("store:like_product", args=[product.id]))
        assert response.status_code == 302
        assert Product.objects.get(id=product.id).productlike_set.count() == 1
        response = authenticated_client.post(reverse("store:like_product", args=[product.id]))
        assert Product.objects.get(id=product.id).productlike_set.count() == 0

    def test_store_panel_without_authenticated_user(self, client, create_product):
        create_product()
        response = client.get(reverse("store:store_panel"))
        assert response.status_code == 200
        assert "order" not in response.context

    
    def test_seller_panel_post_invalid_product(self, seller_client):
        data = {"name": ""}
        response = seller_client.post(reverse("store:seller_panel"), data)
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors