from rest_framework import serializers
from .models import Product, Order, OrderItem, UserProfile, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.name", read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "digital",
            "description",
            "imageURL",
            "seller_name",
            "categories",
        ]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Product name must contain at least 3 characters."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "get_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source="orderitem_set", read_only=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "date_ordered",
            "complete",
            "transaction_id",
            "get_total_price",
            "items",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "name",
            "role",
            "store_name",
            "store_description",
            "is_approved",
        ]
