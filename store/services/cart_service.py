from store.models import Order, OrderItem


class CartService:

    @staticmethod
    def update_cart(profile, product, action):

        order, _ = Order.objects.get_or_create(customer=profile, complete=False)

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": 0, "price_at_purchase": product.price},
        )
        if action == "increase":

            order_item.quantity += 1

        elif action == "decrease":

            order_item.quantity -= 1

        if order_item.quantity <= 0:

            order_item.delete()

        else:
            order_item.save()
