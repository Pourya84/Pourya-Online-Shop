from rest_framework import viewsets, permissions
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiResponse,
)
from .models import Product, Order, UserProfile
from .serializers import ProductSerializer, OrderSerializer, UserProfileSerializer
from .permissions import IsOwner, IsSellerOrReadOnly, IsProductOwner


@extend_schema_view(
    list=extend_schema(
        summary="List Products", description="Return all available products."
    ),
    retrieve=extend_schema(
        summary="Get Product", description="Return details of a specific product."
    ),
    create=extend_schema(
        summary="Create Product",
        description="Seller creates a new product.",
        request=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="Permission denied"),
        },
        examples=[
            OpenApiExample(
                "Sample Create",
                value={
                    "name": "iPhone 15",
                    "price": 1200,
                    "digital": False,
                    "description": "Smartphone Apple",
                    "categories": [1, 2],
                },
                response_only=False,
            )
        ],
    ),
    update=extend_schema(
        summary="Update Product",
        description="Update an existing product.",
        request=ProductSerializer,
        examples=[
            OpenApiExample(
                "Sample Update",
                value={
                    "name": "Updated Product Name",
                    "price": 1300,
                    "digital": False,
                    "description": "Updated description",
                    "categories": [1, 3],
                },
                response_only=False,
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partial Update Product",
        description="Update one or more fields.",
        request=ProductSerializer,
    ),
    destroy=extend_schema(
        summary="Delete Product", description="Delete a product owned by seller."
    ),
)

# Product CRUD API


class ProductViewSet(viewsets.ModelViewSet):
    queryset = (
        Product.objects.filter(is_available=True)
        .select_related("seller")
        .prefetch_related("categories")
        .order_by('-date_added')
    )
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly, IsProductOwner]
    filterset_fields = ["digital", "categories"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "date_added"]

    
    # Automatically assign current seller to created product

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.profile)


@extend_schema_view(
    list=extend_schema(
        summary="List Orders", description="Return current user's orders."
    ),
    retrieve=extend_schema(summary="Get Order", description="Return order details."),
)


# Read-only API for current user's orders


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return (
            Order.objects.select_related("customer")
            .prefetch_related("orderitem_set", "orderitem_set__product")
            .filter(customer=self.request.user.profile)
        )


@extend_schema_view(
    list=extend_schema(
        summary="Current User Profile", description="Return authenticated user profile."
    ),
    retrieve=extend_schema(
        summary="Profile Details", description="Return profile details."
    ),
)

# Read-only API for authenticated user's profile


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.profile.id)
