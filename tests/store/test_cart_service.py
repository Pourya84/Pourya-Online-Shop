# tests/store/test_cart_service.py
import pytest
from store.services.cart_service import CartService
from store.models import Order


@pytest.mark.unit
def test_cart_service_add_new_item(create_user, create_product):
    user, profile = create_user()
    product = create_product()
    CartService.update_cart(profile, product, "increase")
    order = Order.objects.get(customer=profile, complete=False)
    item = order.orderitem_set.first()
    assert item.quantity == 1
    assert item.price_at_purchase == product.price


@pytest.mark.unit
def test_cart_service_increase_existing_item(create_user, create_product):
    user, profile = create_user()
    product = create_product()
    CartService.update_cart(profile, product, "increase")
    CartService.update_cart(profile, product, "increase")
    order = Order.objects.get(customer=profile, complete=False)
    item = order.orderitem_set.first()
    assert item.quantity == 2


@pytest.mark.unit
def test_cart_service_decrease_item(create_user, create_product):
    user, profile = create_user()
    product = create_product()
    CartService.update_cart(profile, product, "increase")
    CartService.update_cart(profile, product, "decrease")
    order = Order.objects.get(customer=profile, complete=False)
    assert order.orderitem_set.count() == 0